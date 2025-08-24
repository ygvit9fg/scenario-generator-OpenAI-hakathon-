from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Твой Hugging Face API токен (создай на https://huggingface.co/settings/tokens)
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")  # безопасно хранить в переменных окружения
HF_MODEL = "OpenAssistant/gpt-oss-7b"  # пример модели OSS на Hugging Face

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

class GenerateRequest(BaseModel):
    character: str
    topic: str
    length: int = 150  # максимальное количество токенов

@app.post("/generate")
async def generate_text(req: GenerateRequest):
    # Формируем prompt для персонажа
    prompt = (
        f"Персонаж: '{req.character}'\n"
        f"Тема: '{req.topic}'\n"
        "Инструкция: Напиши короткий сценарий для вертикального видео "
        "(hook, 2-3 шага, call-to-action)."
    )

    # Запрос к Hugging Face Inference API
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": req.length,
            "do_sample": True,
            "temperature": 0.8,
            "top_p": 0.95
        }
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return {"error": f"Hugging Face API error: {response.text}"}

    generated_text = response.json()[0]["generated_text"]

    return {"result": generated_text}