from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
#from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import time
import os
#import pickle  # To save and load cookies
import pytest  # For assertion
from test_01_login_course import domain, user_name, password

@pytest.fixture
def driver():
    options = Options()
    #options.add_argument('--headless')  # Uncomment if you want to run headless
    options.add_argument('--no-sandbox')  # Required in Docker/WSL environments
    options.add_argument('--disable-dev-shm-usage')  # Fix for limited /dev/shm space in Docker
    options.add_argument('--disable-gpu')  # Disable GPU acceleration if not needed
    options.add_argument('--window-size=1920,1080')  # Set window size

    # Initialize Gecko driver for Firefox
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_login(driver):
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

        #Retrieve course id from course_id.txt
        with open("course_id.txt", "r") as file:
            course_id = file.read().strip()
        print(f"Course ID '{course_id}' loaded successfully")

	# Adding activities
	# add_observation(driver, course_id)
	# add_hot_question(driver, course_id)
	# add_external_tool(driver, course_id)
	# add_turnitin(driver, course_id)
	# add_interactive_content(driver, course_id)
	# add_database(driver, course_id)
	# add_scorm(driver, course_id)
	# add_choice(driver, course_id)
	# add_custom_certificate(driver, course_id)
        add_assignment(driver, course_id)
        add_book(driver, course_id)
        add_file(driver, course_id)
        add_quiz(driver, course_id)
        add_forum(driver, course_id)
        add_lesson(driver, course_id)
        add_url(driver, course_id)
        add_text_and_media(driver, course_id)
        add_glossary(driver, course_id)
        add_feedback(driver, course_id)
        add_facetoface(driver, course_id)
        add_survey(driver, course_id)
        add_wiki(driver, course_id)
        add_page(driver, course_id)
        add_reengagement(driver, course_id)


    except Exception as e:
        pytest.fail(f"Login failed: {e}")

   #ASSIGNMENT ACTIVITY
def add_assignment(driver, course_id, assignment_name="Test Assignment"):
    print(f"Adding Assignment '{assignment_name}'...")
    driver.get(f"{domain}/course/modedit.php?add=assign&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)
    assignment_name_input = driver.find_element(By.ID, "id_name")
    assignment_name_input.clear()
    assignment_name_input.send_keys(assignment_name)
    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)
    assert assignment_name in driver.page_source, f"Assignment '{assignment_name}' was not added successfully"

    #ADD BOOK ACTIVITY
def add_book(driver, course_id, book_name="Test Book"):
    print(f"Adding Book '{book_name}'...")
    driver.get(f"{domain}/course/modedit.php?add=book&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)
    book_name_input = driver.find_element(By.ID, "id_name")
    book_name_input.clear()
    book_name_input.send_keys(book_name)
    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)
    assert book_name in driver.page_source, "Book was failed to add"

    #ADD CHAT ACTIVITY
def add_chat (driver, course_id, chat_name='Test Chat'):
    print(f"Adding Chat '{chat_name}'...")
    driver.get(f"{domain}/course/modedit.php?add=chat&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)
    chat_name_input = driver.find_element(By.ID, "id_name")
    chat_name_input.clear()
    chat_name_input.send_keys(chat_name)
    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)
    print(f"Chat Activity '{chat_name}' successfully added")
    assert chat_name in driver.page_source, "Chat activity failed to add"


def add_file(driver, course_id, file_name='Test File'):
    print(f"Adding File '{file_name}'")
    driver.get(f"{domain}/course/modedit.php?add=resource&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)
    file_name_input = driver.find_element(By.ID, "id_name")
    file_name_input.clear()
    file_name_input.send_keys(file_name)

    # Scroll to the "Select files" area
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Find the file manager area for uploading the file
    file_picker_button = driver.find_element(By.CLASS_NAME, "fp-btn-add")
    driver.execute_script("arguments[0].scrollIntoView(true);", file_picker_button)
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

    driver.switch_to.default_content()

    # Now find the "Save and display" button (or "Save and return to course")
    save_and_display_button = driver.find_element(By.ID, "id_submitbutton2")
    save_and_display_button.click()  # Click the "Save and display" button
    time.sleep(5)

    print(f"File activity '{file_name}' successfully added")

    assert file_name in driver.page_source, "File was failed to add"

# ADD quiz activity
def add_quiz(driver, course_id, quiz_name="Test Quiz"):
    print(f"Adding Quiz '{quiz_name}'...")
    driver.get(f"{domain}/course/modedit.php?add=quiz&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)

    quiz_name_input = driver.find_element(By.ID, "id_name")
    quiz_name_input.clear()
    quiz_name_input.send_keys(quiz_name)

    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)

    print(f"Quiz activity '{quiz_name}' successfully added")
    assert quiz_name in driver.page_source, f"Quiz '{quiz_name}' was not added successfully"

# ADD forum activity
def add_forum(driver, course_id, forum_name="Test Forum"):
    print(f"Adding Forum '{forum_name}'...")
    driver.get(f"{domain}/course/modedit.php?add=forum&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)

    forum_name_input = driver.find_element(By.ID, "id_name")
    forum_name_input.clear()
    forum_name_input.send_keys(forum_name)

    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)

    print(f"Forum activity '{forum_name}' successfully added")
    assert forum_name in driver.page_source, f"Forum '{forum_name}' was not added successfully"

# ADD lesson activity
def add_lesson(driver, course_id, lesson_name="Test Lesson"):
    print(f"Adding Lesson '{lesson_name}'...")
    driver.get(f"{domain}/course/modedit.php?add=lesson&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)

    lesson_name_input = driver.find_element(By.ID, "id_name")
    lesson_name_input.clear()
    lesson_name_input.send_keys(lesson_name)

    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)

    print(f"Lesson activity '{lesson_name}' successfully added")
    assert lesson_name in driver.page_source, f"Lesson '{lesson_name}' was not added successfully"

# ADD URL activity
def add_url(driver, course_id, url_name="Test URL"):
    print(f"Adding URL ...")
    driver.get(f"{domain}/course/modedit.php?add=url&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)

    url_name_input = driver.find_element(By.ID, "id_name")
    url_name_input.clear()
    url_name_input.send_keys(url_name)

    url_input = driver.find_element(By.ID, "id_externalurl")
    url_input.clear()
    url_input.send_keys("https://www.google.com")

    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)

    print(f"URL activity '{url_name}' successfully added")
    assert url_name in driver.page_source, f"URL '{url_name}' was not added successfully"


    # ADD text and media activity (Label)
def add_text_and_media(driver, course_id, label_name="Test Label"):
    print(f"Adding Text and Media '{label_name}'...")
    driver.get(f"{domain}/course/modedit.php?add=label&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)

    label_name_input = driver.find_element(By.ID, "id_introeditoreditable")
    label_name_input.clear()
    label_name_input.send_keys(label_name)

    driver.find_element(By.ID, "id_submitbutton2").click()
    time.sleep(5)

    print(f"Text and Media activity '{label_name}' successfully added")
    assert label_name in driver.page_source, f"Text and Media '{label_name}' was not added successfully"

# ADD glossary activity
def add_glossary(driver, course_id, glossary_name="Test Glossary"):
    print(f"Adding Glossary '{glossary_name}'...")
    driver.get(f"{domain}/course/modedit.php?add=glossary&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)

    glossary_name_input = driver.find_element(By.ID, "id_name")
    glossary_name_input.clear()
    glossary_name_input.send_keys(glossary_name)

    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)

    print(f"Glossary activity '{glossary_name}' successfully added")
    assert glossary_name in driver.page_source, f"Glossary '{glossary_name}' was not added successfully"

# ADD feedback activity
def add_feedback(driver, course_id, feedback_name="Test Feedback"):
    print(f"Adding Feedback '{feedback_name}'...")
    driver.get(f"{domain}/course/modedit.php?add=feedback&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)

    feedback_name_input = driver.find_element(By.ID, "id_name")
    feedback_name_input.clear()
    feedback_name_input.send_keys(feedback_name)

    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)

    print(f"Feedback activity '{feedback_name}' successfully added")
    assert feedback_name in driver.page_source, f"Feedback '{feedback_name}' was not added successfully"

# ADD facetoface activity
def add_facetoface(driver, course_id, facetoface_name="Test Face-to-Face"):
    print(f"Adding Face-to-Face '{facetoface_name}'...")
    driver.get(f"{domain}/course/modedit.php?add=facetoface&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)

    facetoface_name_input = driver.find_element(By.ID, "id_name")
    facetoface_name_input.clear()
    facetoface_name_input.send_keys(facetoface_name)

    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)

    print(f"Face-to-Face activity '{facetoface_name}' successfully added")
    assert facetoface_name in driver.page_source, f"Face-to-Face '{facetoface_name}' was not added successfully"


# ADD survey
def add_survey(driver, course_id, survey_name="Test Survey", survey_type="COLLES (Preferred and Actual)"):
    print(f"Adding Survey '{survey_name}' with survey type '{survey_type}'...")
    driver.get(f"{domain}/course/modedit.php?add=survey&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)
    survey_name_input = driver.find_element(By.ID, "id_name")
    survey_name_input.clear()
    survey_name_input.send_keys(survey_name)
    survey_type_dropdown = Select(driver.find_element(By.ID, "id_template"))
    survey_type_dropdown.select_by_visible_text(survey_type)
    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)
    assert survey_name in driver.page_source, f"Survey '{survey_name}' was not added successfully"

# ADD wiki
def add_wiki(driver, course_id, wiki_name="Test Wiki"):
    print(f"Adding Wiki '{wiki_name}'...")
    driver.get(f"{domain}/course/modedit.php?add=wiki&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)

    wiki_name_input = driver.find_element(By.ID, "id_name")
    wiki_name_input.clear()
    wiki_name_input.send_keys(wiki_name)

    wiki_firstpage_input = driver.find_element(By.ID, "id_firstpagetitle")
    wiki_firstpage_input.clear()
    wiki_firstpage_input.send_keys("Test First Page")

    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)

    print(f"Wiki activity '{wiki_name}' successfully added")
    assert wiki_name in driver.page_source, f"Wiki '{wiki_name}' was not added successfully"

# ADD WORKSHOP
def add_workshop(driver, course_id, workshop_name="Test Workshop"):
    print(f"Adding Workshop '{workshop_name}'...")
    driver.get(f"{domain}/course/modedit.php?add=workshop&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)

    workshop_name_input = driver.find_element(By.ID, "id_name")
    workshop_name_input.clear()
    workshop_name_input.send_keys(workshop_name)

    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)

    print(f"Workshop activity '{workshop_name}' successfully added")
    assert workshop_name in driver.page_source, f"Workshop '{workshop_name}' was not added successfully"

# ADD PAGE
def add_page(driver, course_id, page_name="Test Page", page_content="This is the content of the page"):
    print(f"Adding Page '{page_name}'...")
    driver.get(f"{domain}/course/modedit.php?add=page&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)

    # page name
    page_name_input = driver.find_element(By.ID, "id_name")
    page_name_input.clear()
    page_name_input.send_keys(page_name)

    # page content
    page_content_input = driver.find_element(By.ID, "id_pageeditable")
    page_content_input.clear()
    page_content_input.send_keys(page_content)

    # Submit the form
    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)

    print(f"Page activity '{page_name}' successfully added")
    assert page_name in driver.page_source, f"Page '{page_name}' was not added successfully"


# ADD Reengagement
def add_reengagement(driver, course_id, reengagement_name = "Test Reengagement"):
    print ("Adding Reengagement '{reengagement_name}'...")
    driver.get(f"{domain}/course/modedit.php?add=reengagement&type=&course={course_id}&section=0&return=0&sr=0")
    time.sleep(2)

    page_name_input = driver.find_element (By.ID, "id_name")
    page_name_input.clear()
    page_name_input.send_keys(reengagement_name)

    # Scroll to the "Select files" area
    submit = driver.find_element(By.ID, "id_submitbutton")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit)
    driver.find_element(By.ID, "id_submitbutton").click()
    time.sleep(5)

    print(f"Page activity '{reengagement_name}' successfully added")
    assert reengagement_name in driver.page_source, f"Page '{reengagement_name}' was not added successfully"

# @pytest.mark.usefixtures("driver")
# def test_add_activities(driver):
#     driver.get("http://localhost:8082")
#     with open("cookies.pkl", "rb") as f:
#         cookies = pickle.load(f)
#         for cookie in cookies:
#             driver.add_cookie(cookie)
#     print("Cookies loaded successfully")

