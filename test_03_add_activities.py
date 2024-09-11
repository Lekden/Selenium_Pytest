import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pickle
import os


@pytest.fixture
def driver():
    options = Options()
    #options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()


def add_assignment(driver, course_id, assignment_name="Test Assignment"):
    print(f"Adding Assignment '{assignment_name}'...")

    # Navigate to the add assignment page
    driver.get(f"http://localhost:8082/course/modedit.php?add=assign&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)

    # Fill the assignment name input field
    assignment_name_input = driver.find_element(By.ID, "id_name")
    assignment_name_input.clear()
    assignment_name_input.send_keys(assignment_name)

    # Submit the form to add the assignment
    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)

    # Print success message with assignment name
    print(f"Assignment activity '{assignment_name}' successfully added")

    # Verify the assignment was added by checking the page source
    assert assignment_name in driver.page_source, f"Assignment '{assignment_name}' was not added successfully"



def add_book(driver, course_id, book_name="Test Book"):
    print(f"Adding Book '{book_name}'...")
    driver.get(f"http://localhost:8082/course/modedit.php?add=book&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)
    book_name_input = driver.find_element(By.ID, "id_name")
    book_name_input.clear()
    book_name_input.send_keys("Test Book")
    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)
    print(f"Booking activity '{book_name}' successfully added")
    assert "Test Book" in driver.page_source, "Book was not added successfully"


def add_file(driver, course_id, file_name='Test file'):
    print(f"Adding File '{file_name}'")
    driver.get(f"http://localhost:8082/course/modedit.php?add=resource&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)
    file_name_input = driver.find_element(By.ID, "id_name")
    file_name_input.clear()
    file_name_input.send_keys("Test File")

    # Scroll to the "Select files" area
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Find the file manager area for uploading the file
    file_picker_button = driver.find_element(By.CLASS_NAME, "fp-btn-add")
    file_picker_button.click()
    time.sleep(2)

    # Provide the file path
    upload_input = driver.find_element(By.NAME, "repo_upload_file")
    absolute_path = os.path.abspath("/home/lekden/projects/tests/testfile/testfile.txt")
    upload_input.send_keys(absolute_path)

    # Click the "Upload this file" button
    upload_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Upload this file')]")
    upload_button.click()
    time.sleep(5)

    # After uploading, switch back to the main content if necessary
    driver.switch_to.default_content()

    # Now find the "Save and display" button (or "Save and return to course")
    save_and_display_button = driver.find_element(By.ID, "id_submitbutton2")
    save_and_display_button.click()  # Click the "Save and display" button
    time.sleep(5)

    print(f"File activity '{file_name}' successfully added")

    assert "Test File" in driver.page_source, "File was not added successfully"


@pytest.mark.usefixtures("driver")
def test_add_activities(driver):
    # Load cookies to reuse the session
    driver.get("http://localhost:8082")  # Open any page to set the domain
    with open("cookies.pkl", "rb") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
    print("Cookies loaded successfully")

    # Load the saved course ID
    with open("course_id.txt", "r") as file:
        course_id = file.read().strip()
    print(f"Course ID '{course_id}' loaded successfully")

    # Adding activities
    add_assignment(driver, course_id)
    add_book(driver, course_id)
    add_file(driver, course_id)
