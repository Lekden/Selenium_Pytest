import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle

def test_create_course():
    options = Options()
    # options.add_argument('--headless')  # Uncomment if you want to run headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Load cookies to reuse the session
        driver.get("http://localhost:8082")  # Open any page to set the domain
        with open("cookies.pkl", "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)

        # Refresh to apply the cookies and load the session
        driver.refresh()

        # Navigate to course creation page
        driver.get("http://localhost:8082/course/edit.php?category=1&returnto=catmanage")
        time.sleep(2)

        # Fill in course details
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

        # Step 1: Capture the course ID from the URL
        current_url = driver.current_url
        assert "id=" in current_url, "Failed to capture course ID from the URL"
        course_id = current_url.split("id=")[1]

        # Step 2: Save the course ID to a file for reuse
        with open("course_id.txt", "w") as file:
            file.write(course_id)

        # Step 3: Print success message
        print(f"Course with ID {course_id} successfully created!")

    except Exception as e:
        pytest.fail(f"An error occurred during course creation: {e}")

    finally:
        driver.quit()
