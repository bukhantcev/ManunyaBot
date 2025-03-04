import os

import openai
from openai import OpenAI



OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)
def get_ai_response(user_input, role:str, messages:list):

    try:
        # Отправляем запрос к OpenAI API
        response = client.chat.completions.create(model="gpt-4o",  # Используемая модель
        messages=messages,
        max_tokens=10000,  # Максимальное количество токенов в ответе
        temperature=0.7)
        # Получаем текст ответа
        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:
        return f"Ошибка: {e}"


client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))