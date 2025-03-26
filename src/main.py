from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import time
import os
from selenium.webdriver.chrome.options import Options

load_dotenv()
chrome_options = Options()
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
)
chrome_options.add_argument("--window-size=1920,1080")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

INSTAGRAM_USER = os.getenv("INSTAGRAM_USER")
INSTAGRAM_PASS = os.getenv("INSTAGRAM_PASS")
TARGET_USER = os.getenv("TARGET_USER")
MESSAGE = "Olá! Essa é uma mensagem automática."

driver.get("https://www.instagram.com/")
time.sleep(5)

username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")

username_input.send_keys(INSTAGRAM_USER)
password_input.send_keys(INSTAGRAM_PASS)
password_input.send_keys(Keys.ENTER)

time.sleep(10)

driver.get(f"https://www.instagram.com/{TARGET_USER}/")
time.sleep(5)

message_button = driver.find_element(By.XPATH, "//div[text()='Message']")
message_button.click()
time.sleep(5)

wait = WebDriverWait(driver, 10)
message_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']")))

message_box.send_keys(MESSAGE)
message_box.send_keys(Keys.ENTER)

time.sleep(5)
driver.quit()
