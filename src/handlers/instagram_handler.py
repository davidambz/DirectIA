import os
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
from handlers.time_handler import human_sleep
from handlers.gpt_handler import generate_message

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
    human_sleep(5, 10)

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(INSTAGRAM_USER)
    password_input.send_keys(INSTAGRAM_PASS)
    password_input.send_keys(Keys.ENTER)

    human_sleep(10, 20)

def open_profile(driver, username: str):
    driver.get(f"https://www.instagram.com/{username}/")
    human_sleep(5, 10)
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
        try:
            name_element = header.find_element(By.XPATH, ".//h1 | .//h2")
            name = name_element.text.strip()
        except:
            name = ""

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

def send_message_from_profile(driver, profile):
    try:
        use_gpt = os.getenv("USE_GPT", "false").lower() == "true"
        send = os.getenv("SEND_MESSAGES", "false").lower() == "true"

        message_buttons = driver.find_elements(
            By.XPATH,
            "//div[text()='Message' or text()='Enviar mensagem']"
        )
        if not message_buttons:
            print("⚠️ Perfil não permite envio de mensagens ou está bloqueado. Pulando...")
            return

        if use_gpt:
            message = generate_message(profile)
        else:
            message = "Esta é uma mensagem de teste para evitar o uso da API."

        print(f"✉️ Mensagem: {message}")

        if not send:
            print("📭 Modo de envio desativado. Mensagem não enviada.")
            return

        message_buttons[0].click()
        human_sleep(5, 10)

        wait = WebDriverWait(driver, 10)
        message_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']")))

        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)
        human_sleep(5, 10)
        print("✅ Mensagem enviada com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao tentar enviar mensagem: {e}")

def follow_user_from_profile(driver):
    try:
        header = driver.find_element(By.TAG_NAME, "header")
        buttons = header.find_elements(By.TAG_NAME, "button")

        for btn in buttons:
            texto = btn.text.strip()
            if texto in ["Seguir", "Seguir de volta", "Follow", "Follow back"]:
                btn.click()
                human_sleep(2, 4)
                print("👤 Seguido com sucesso.")
                return

        print("✅ Já está seguindo ou botão de seguir não encontrado.")
    except Exception as e:
        print(f"❌ Erro ao tentar seguir: {e}")
