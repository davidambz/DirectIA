from handlers.file_handler import read_usernames_from_file
from handlers.instagram_handler import (
    create_driver,
    login,
    open_profile,
    extract_profile_data_from_header,
    send_message_from_profile,
    follow_user_from_profile
)
from handlers.gpt_handler import generate_message
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# ⚙️ Flags de controle via .env
use_gpt = os.getenv("USE_GPT", "false").lower() == "true"
send = os.getenv("SEND_MESSAGES", "false").lower() == "true"

if __name__ == "__main__":
    usernames = read_usernames_from_file("src/data/profiles.txt")

    print(f"\n🔧 GPT ativado: {use_gpt}")
    print(f"📤 Envio ativado: {send}")

    driver = create_driver()
    try:
        login(driver)
        for username in usernames:
            print(f"\n🔍 Acessando perfil: {username}")
            header = open_profile(driver, username)
            if not header:
                print(f"❌ Não foi possível carregar o perfil de {username}")
                continue

            profile = extract_profile_data_from_header(header, username)
            if profile.get("erro"):
                print(f"❌ Erro ao extrair dados de {username}: {profile['erro']}")
                continue

            print("✅ Dados extraídos:")
            for k, v in profile.items():
                print(f"{k}: {v}")

            # Seguir o perfil se necessário
            follow_user_from_profile(driver)

            # Geração da mensagem
            if use_gpt:
                print("\n🤖 Gerando mensagem personalizada com GPT...")
                message = generate_message(profile)
            else:
                print("\n💬 Usando mensagem padrão para testes (API desativada)")
                message = "Olá! Essa é uma mensagem padrão enviada para teste, sem uso da API do ChatGPT."

            print(f"\n✉️ Mensagem gerada:\n{message}")

            # Envio da mensagem
            if send:
                print("📤 Enviando mensagem...")
                send_message_from_profile(driver, message)
            else:
                print("🚫 Envio desativado (SEND_MESSAGES = false)")

    finally:
        driver.quit()
