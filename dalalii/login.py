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
LOGIN_URL = "https://dalalii.co.tz/authentication/sign-in"   
USERNAME = "784090148"
PASSWORD = ""

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
        time.sleep(2)
        return driver
    except WebDriverException as e:
        logger.error("Failed to initialize WebDriver", exc_info=True)
        raise e


