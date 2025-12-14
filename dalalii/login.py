"""
dalalii.login

This module automates the login process for the Dalalii system.
It uses Selenium for browser automation and BeautifulSoup for
HTML parsing and verification.
"""

import time
import logging
from typing import Optional

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


# -------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------
LOGIN_URL = "https://example.com/login"   # replace with real URL
USERNAME = "your_username"
PASSWORD = "your_password"

WAIT_TIME = 15


# -------------------------------------------------------------------
# LOGGING SETUP
# -------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------
# DRIVER INITIALIZATION
# -------------------------------------------------------------------
def initialize_driver() -> webdriver.Chrome:
    """
    Initialize and return a configured Selenium WebDriver instance.
    """
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("useAutomationExtension", False)

    try:
        driver = webdriver.Chrome(options=options)
        logger.info("Chrome WebDriver initialized successfully")
        return driver
    except WebDriverException as e:
        logger.error("Failed to initialize WebDriver", exc_info=True)
        raise e


# -------------------------------------------------------------------
# LOGIN AUTOMATION
# -------------------------------------------------------------------
def login(driver: webdriver.Chrome) -> None:
    """
    Open the login page and perform login.
    """
    logger.info("Opening login page")
    driver.get(LOGIN_URL)

    try:
        wait = WebDriverWait(driver, WAIT_TIME)

        username_input = wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_input = wait.until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        login_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )

        username_input.clear()
        username_input.send_keys(USERNAME)

        password_input.clear()
        password_input.send_keys(PASSWORD)

        login_button.click()
        logger.info("Login form submitted")

    except TimeoutException:
        logger.error("Login elements not found within timeout", exc_info=True)
        raise


# -------------------------------------------------------------------
# PAGE VERIFICATION USING BEAUTIFULSOUP
# -------------------------------------------------------------------
def verify_login(driver: webdriver.Chrome) -> bool:
    """
    Verify successful login using BeautifulSoup.
    """
    time.sleep(3)  # allow page to load after login
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, "html.parser")

    # Example check – adjust according to real dashboard content
    dashboard_marker = soup.find("div", class_="dashboard")

    if dashboard_marker:
        logger.info("Login verified successfully")
        return True

    logger.warning("Login verification failed")
    return False


# -------------------------------------------------------------------
# OPTIONAL: REQUESTS SESSION (API / COOKIE BASED)
# -------------------------------------------------------------------
def create_requests_session(driver: webdriver.Chrome) -> requests.Session:
    """
    Transfer Selenium cookies to a requests session.
    Useful for API calls after login.
    """
    session = requests.Session()

    for cookie in driver.get_cookies():
        session.cookies.set(cookie["name"], cookie["value"])

    logger.info("Requests session created from Selenium cookies")
    return session


# -------------------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------------------
def main() -> None:
    driver: Optional[webdriver.Chrome] = None

    try:
        driver = initialize_driver()
        login(driver)

        if verify_login(driver):
            logger.info("Automation completed successfully")
        else:
            logger.error("Automation completed but login failed")

    except Exception as e:
        logger.critical("Automation failed", exc_info=True)

    finally:
        if driver:
            driver.quit()
            logger.info("Browser closed")


# -------------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------------
if __name__ == "__main__":
    main()
