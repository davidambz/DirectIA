import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_message(profile: dict) -> str:
    system_prompt = os.getenv("GPT_SYSTEM_PROMPT") or "Você é um especialista em abordagens humanas para prospecção de clientes."
    user_context = os.getenv("GPT_USER_PROMPT")

    user_prompt = (
        f"{user_context}\n\n"
        f"Crie uma mensagem curta, natural e personalizada com base no perfil abaixo.\n\n"
        f"Nome: {profile['nome']}\n"
        f"Username: {profile['username']}\n"
        f"Bio: {profile['bio']}\n"
        f"Link: {profile['link']}\n\n"
        f"A mensagem deve ser simpática e parecer uma conversa comum, mas com a intenção de descobrir se a pessoa tem interesse em vender o carro que possui ou já teve. "
        f"Evite linguagem robótica ou clichês de vendas. Use uma abordagem humana e contextualize com base na bio, se possível."
    )

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=100,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
