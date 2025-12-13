from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()

# ===========================
# Remove headless so browser is visible
# ===========================
# options.add_argument("--headless")  # Comment this out or remove it
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")  # optional

# Selenium will auto-detect ChromeDriver
driver = webdriver.Chrome(options=options)

driver.get("https://jiji.co.tz/")
print(driver.title)

# Pause so you can see the browser before it closes
input("Press Enter to close the browser...")

driver.quit()
