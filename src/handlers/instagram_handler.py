import os
import time
import re
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    )
    chrome_options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def login(driver):
    INSTAGRAM_USER = os.getenv("INSTAGRAM_USER")
    INSTAGRAM_PASS = os.getenv("INSTAGRAM_PASS")

    driver.get("https://www.instagram.com/")
    time.sleep(5)

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(INSTAGRAM_USER)
    password_input.send_keys(INSTAGRAM_PASS)
    password_input.send_keys(Keys.ENTER)

    time.sleep(10)

def open_profile(driver, username: str):
    driver.get(f"https://www.instagram.com/{username}/")
    time.sleep(5)
    try:
        header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "header"))
        )
        return header
    except Exception as e:
        print(f"Erro ao carregar perfil de {username}: {e}")
        return None

def extract_profile_data_from_header(header, username: str) -> dict:
    try:
        # Extrai nome
        try:
            name_element = header.find_element(By.XPATH, ".//h1 | .//h2")
            name = name_element.text.strip()
        except:
            name = ""

        # Extrai bio e link
        sections = header.find_elements(By.TAG_NAME, "section")
        bio, link = "", ""

        if len(sections) >= 4:
            lines = sections[3].text.strip().split("\n")
            lines = [line for line in lines if not line.lower().startswith("followed by")]
            if lines and re.match(r"(https?:\/\/|beacons\.|linktr\.|bio\.link)", lines[-1]):
                link = lines.pop()
            bio = "\n".join(lines)

        return {
            "username": username,
            "nome": name,
            "bio": bio,
            "link": link
        }

    except Exception as e:
        return {
            "username": username,
            "nome": "",
            "bio": "",
            "link": "",
            "erro": str(e)
        }

def send_message_from_profile(driver, message):
    try:
        message_buttons = driver.find_elements(By.XPATH, "//div[text()='Message']")
        if not message_buttons:
            print("⚠️ Perfil não permite envio de mensagens ou está bloqueado. Pulando...")
            return

        message_buttons[0].click()
        time.sleep(5)

        wait = WebDriverWait(driver, 10)
        message_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']")))

        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)
        time.sleep(5)
        print("✅ Mensagem enviada com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao tentar enviar mensagem: {e}")

def follow_user_from_profile(driver):
    try:
        follow_buttons = driver.find_elements(By.XPATH, "//div[text()='Follow' or text()='Seguir']")
        if follow_buttons:
            follow_buttons[0].click()
            time.sleep(2)
            print("👤 Seguido com sucesso.")
        else:
            print("✅ Já está seguindo ou botão de seguir não encontrado.")
    except Exception as e:
        print(f"❌ Erro ao tentar seguir: {e}")