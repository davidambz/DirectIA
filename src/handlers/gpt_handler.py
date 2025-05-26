import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_message(profile: dict) -> str:
    system_prompt = os.getenv("GPT_SYSTEM_PROMPT")
    user_context = os.getenv("GPT_USER_PROMPT")

    user_prompt = (
        f"{user_context}\n\n"
        f"Com base no perfil abaixo, escreva uma mensagem personalizada, simpática e com até 300 caracteres. "
        f"A mensagem deve ter apenas um parágrafo, parecer uma conversa natural e caber numa única mensagem de Instagram Direct. "
        f"Evite emojis, linguagem robótica, reticências ou símbolos como ✨, ❤️ ou similares. "
        f"Você pode usar informações do perfil para deixar a abordagem mais pessoal, "
        f"mas a pergunta no final deve estar alinhada ao meu objetivo descrito acima, mantendo o assunto principal da conversa de acordo com meu contexto.\n\n"
        f"Nome: {profile['nome']}\n"
        f"Username: {profile['username']}\n"
        f"Bio: {profile['bio']}\n"
        f"Link: {profile['link']}"
    )

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=120,
        temperature=0.6
    )

    return response.choices[0].message.content.strip()
