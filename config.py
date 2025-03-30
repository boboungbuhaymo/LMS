import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_MAX_TOKENS = 150

# NLP Configuration
SIMILARITY_THRESHOLD = 0.75  # Minimum confidence score for answer matching

# Web Automation Configuration
WEBDRIVER_PATH = "./chromedriver"  # Path to ChromeDriver
LOGIN_URL = "https://bcpeducollege.elearningcommons.com/login"
MAX_WAIT_TIME = 10  # seconds for Selenium waits