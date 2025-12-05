import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=options
)
driver.get("http://localhost:4200/login")
assert "Sign in" in driver.title

login_elem = driver.find_element(By.CSS_SELECTOR, "input")
login_elem.send_keys("jusz22")

passwd_elem = driver.find_element(By.CLASS_NAME, "p-password-input")
passwd_elem.send_keys("abc")

signin_button = driver.find_element(By.CSS_SELECTOR, "button.p-button")
signin_button.click()

time.sleep(1)
token = driver.execute_script("return window.localStorage.getItem('token');")
assert token is not None
driver.close()
