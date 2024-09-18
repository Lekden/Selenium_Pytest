from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import time
import pickle  # To save and load cookies
import pytest  # For assertion

# CHANGE DOMAIN URL HERE
domain = "http://localhost:8082"
user_name = "admin"
password =  "Admin_password1"
student = "user_test"

def test_login_and_create_course():
    options = Options()
    #options.add_argument('--headless')  # Uncomment if you want to run headless
    options.add_argument('--no-sandbox')  # Required in Docker/WSL environments
    options.add_argument('--disable-dev-shm-usage')  # Fix for limited /dev/shm space in Docker
    options.add_argument('--disable-gpu')  # Disable GPU acceleration if not needed
    options.add_argument('--window-size=1920,1080')  # Set window size

    # Initialize Gecko driver for Firefox
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    try:
        # Step 1: Login to Moodle as Admin
        driver.get(domain + "/login/index.php")
        time.sleep(2)

        # Enter admin credentials and log in
        username_input = driver.find_element(By.ID, "username")
        username_input.clear()
        username_input.send_keys(user_name)

        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        # Check if login was successful by looking for a post-login element (e.g., profile link)
        profile_link = driver.find_element(By.CLASS_NAME, "avatars")  # Replace with a known post-login element
        assert profile_link is not None, "Login unsuccessful, profile link not found"
        print("Login Successful!!!")

        # Step 2: Navigate to course creation page
        driver.get(domain + "/course/edit.php?category=1&returnto=catmanage")
        time.sleep(2)

        # Step 3: Fill in course details
        course_fullname_input = driver.find_element(By.ID, "id_fullname")
        course_fullname_input.clear()
        course_fullname_input.send_keys("Selenium Course")

        course_shortname_input = driver.find_element(By.ID, "id_shortname")
        course_shortname_input.clear()
        course_shortname_input.send_keys("SEL101")

        # Save and return to course
        save_button = driver.find_element(By.ID, "id_saveanddisplay")
        assert save_button is not None, "Save and Display button not found"
        save_button.click()
        time.sleep(5)

        # Step 4: Capture the course ID from the URL
        current_url = driver.current_url
        assert "id=" in current_url, "Failed to capture course ID from the URL"
        course_id = current_url.split("id=")[1]

        # Step 5: Save the course ID to a file for reuse
        with open("course_id.txt", "w") as file:
            file.write(course_id)

        # Print success message
        print(f"Course with ID {course_id} successfully created!")

    except Exception as e:
        pytest.fail(f"An error occurred during course creation: {e}")

    finally:
        # Close the browser
        driver.quit()

# Run the merged test
if __name__ == "__main__":
    test_login_and_create_course()
