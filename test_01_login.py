from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle  # To save and load cookies
import pytest  # For assertion

def test_login_and_save_session():
    options = Options()
    #options.add_argument('--headless')  # Uncomment to run headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialize Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Login to Moodle as Admin
        driver.get("http://localhost:8082/login/index.php")
        time.sleep(2)

        # Enter admin credentials
        username_input = driver.find_element(By.ID, "username")
        username_input.clear()
        username_input.send_keys("admin")

        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys("Admin_password1")
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        # Check if login was successful by looking for a known post-login element (e.g., Profile or Logout)
        try:
            profile_link = driver.find_element(By.LINK_TEXT, "Hi, Admin!")  # Replace 'Profile' with actual post-login element
            assert profile_link is not None, "Login unsuccessful, profile link not found"
            print("Login Successful!!!")
        except:
            pytest.fail("Login unsuccessful, could not find profile link.")

        # Save cookies to a file after successful login
        with open("cookies.pkl", "wb") as f:
            pickle.dump(driver.get_cookies(), f)

        print("Session saved successfully!")

    finally:
        # Close the browser
        driver.quit()

# Run the login function to save the session
if __name__ == "__main__":
    test_login_and_save_session()
#Line test for git
