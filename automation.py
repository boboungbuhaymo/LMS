from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import WEBDRIVER_PATH, LOGIN_URL, MAX_WAIT_TIME
import time

class QuizAutomator:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.driver = None

    def initialize_driver(self):
        """Initialize Chrome WebDriver with options"""
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(executable_path=WEBDRIVER_PATH, options=options)
        self.driver.implicitly_wait(MAX_WAIT_TIME)

    def login(self):
        """Login to the e-learning platform"""
        try:
            self.driver.get(LOGIN_URL)
            
            # Fill login form
            username_field = WebDriverWait(self.driver, MAX_WAIT_TIME).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys(self.username)
            
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            
            login_button = self.driver.find_element(By.ID, "loginbtn")
            login_button.click()
            
            # Wait for login to complete
            WebDriverWait(self.driver, MAX_WAIT_TIME).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
            )
            return True
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Login failed: {str(e)}")
            return False

    def submit_quiz(self, quiz_url: str, answers: dict):
        """Submit answers to a quiz"""
        try:
            self.driver.get(quiz_url)
            
            # Wait for quiz to load
            WebDriverWait(self.driver, MAX_WAIT_TIME).until(
                EC.presence_of_element_located((By.CLASS_NAME, "que"))
            )
            
            # Process each question
            questions = self.driver.find_elements(By.CLASS_NAME, "que")
            for i, question in enumerate(questions):
                question_id = question.get_attribute("id")
                
                if question_id in answers:
                    self._answer_question(question, answers[question_id])
            
            # Submit quiz
            submit_button = WebDriverWait(self.driver, MAX_WAIT_TIME).until(
                EC.element_to_be_clickable((By.NAME, "submit"))
            )
            submit_button.click()
            
            # Confirm submission
            confirm_button = WebDriverWait(self.driver, MAX_WAIT_TIME).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Submit all and finish']"))
            )
            confirm_button.click()
            
            return True
        except Exception as e:
            print(f"Quiz submission failed: {str(e)}")
            return False

    def _answer_question(self, question_element, answer):
        """Answer a single question based on its type"""
        question_type = question_element.get_attribute("class").split()[1]
        
        if question_type == "multichoice":
            self._answer_multichoice(question_element, answer)
        elif question_type == "shortanswer":
            self._answer_shortanswer(question_element, answer)
        # Add more question types as needed

    def _answer_multichoice(self, question_element, answer):
        """Answer multiple choice question"""
        options = question_element.find_elements(By.CLASS_NAME, "answer")
        for option in options:
            input_element = option.find_element(By.TAG_NAME, "input")
            if input_element.get_attribute("value") == answer:
                input_element.click()
                break

    def _answer_shortanswer(self, question_element, answer):
        """Answer short answer question"""
        textarea = question_element.find_element(By.TAG_NAME, "textarea")
        textarea.send_keys(answer)

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    print("Quiz Automator module loaded. Import and use the QuizAutomator class.")