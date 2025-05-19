from handlers.instagram_handler import (
    create_driver,
    login,
    open_profile,
    extract_profile_data_from_header,
    send_message_from_profile,
    follow_user_from_profile
)
from handlers.file_handler import read_usernames_from_file
from handlers.gpt_handler import generate_message
from handlers.time_handler import human_sleep
import os
import sys
import random  # ✅ Importado para gerar delays

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    print()
    use_gpt = os.getenv("USE_GPT", "false").lower() == "true"
    send = os.getenv("SEND_MESSAGES", "false").lower() == "true"

    print(f"🔧 GPT ativado: {use_gpt}")
    print(f"📤 Envio ativado: {send}")
    print()

    base_path = get_base_path()
    profiles_path = os.path.join(base_path, "profiles.txt")

    usernames = read_usernames_from_file("profiles.txt")

    driver = create_driver()
    try:
        login(driver)

        for username in usernames:
            print(f"🔍 Acessando perfil: {username}")
            header = open_profile(driver, username)
            if not header:
                continue

            profile = extract_profile_data_from_header(header, username)
            if profile.get("erro"):
                print(f"❌ Erro ao extrair perfil de {username}: {profile['erro']}")
                continue

            if use_gpt:
                message = generate_message(profile)
            else:
                message = "Esta é uma mensagem de teste para evitar o uso da API."
            
            print(f"✉️ Mensagem: {message}")

            follow_user_from_profile(driver)

            if send:
                send_message_from_profile(driver, message)

            # ✅ Delay real entre perfis com valor exato mostrado
            delay = random.randint(60, 90)
            print(f"⏳ Aguardando {delay} segundos antes de prosseguir para o próximo perfil...")
            human_sleep(delay, delay)
            print()
    finally:
        driver.quit()
