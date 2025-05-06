import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_message() -> str:
    system_prompt = os.getenv("GPT_SYSTEM_PROMPT")
    user_prompt = os.getenv("GPT_USER_PROMPT")

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=30,
        temperature=0.5
    )

    return response.choices[0].message.content.strip()
