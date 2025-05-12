import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_message(profile: dict) -> str:
    system_prompt = os.getenv("GPT_SYSTEM_PROMPT") or "Você é um especialista em mensagens personalizadas para prospecção de clientes."
    user_context = os.getenv("GPT_USER_PROMPT") or "Sou vendedor de carros usados e estou fazendo um primeiro contato com possíveis clientes."

    user_prompt = (
        f"{user_context}\n\n"
        f"Com base no perfil abaixo, escreva uma mensagem personalizada e simpática com até 300 caracteres. "
        f"A mensagem deve ter apenas um parágrafo, parecer uma conversa natural e caber numa única mensagem de Instagram Direct. "
        f"Finalize a mensagem com uma saudação amigável como 'Abraço!', 'Até mais!' ou algo similar. "
        f"Evite finalizar com reticências.\n\n"
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
        max_tokens=80,
        temperature=0.7
    )

    raw_message = response.choices[0].message.content.strip()

    # Trunca com segurança para no máximo 300 caracteres, sem cortar palavras
    max_length = 300
    if len(raw_message) > max_length:
        last_space = raw_message.rfind(" ", 0, max_length)
        raw_message = raw_message[:last_space].rstrip() + "..."

    return raw_message
