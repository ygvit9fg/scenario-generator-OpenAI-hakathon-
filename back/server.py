from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

HF_API_TOKEN = os.environ.get("HF_API_TOKEN")  # токен из переменных окружения
HF_MODEL = os.environ.get("HF_MODEL", "facebook/bart-large-cnn")


headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

class GenerateRequest(BaseModel):
    character: str
    topic: str
    length: int = 150  # по умолчанию

@app.post("/generate")
async def generate_text(req: GenerateRequest):
    # формируем промпт
    prompt = (
        f"Персонаж: '{req.character}'\n"
        f"Тема: '{req.topic}'\n"
        "Инструкция: Напиши короткий сценарий для вертикального видео "
        "(hook, 2-3 шага, call-to-action)."
    )

    # формируем payload с параметрами
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
        headers={"Authorization": f"Bearer {HF_API_TOKEN}"},
        json=payload  # <--- вот здесь исправил
)


    if response.status_code != 200:
        return {"error": f"Hugging Face API error: {response.text}"}

    data = response.json()
    print("DEBUG RESPONSE:", data)  # полезно для отладки

    if isinstance(data, list) and "generated_text" in data[0]:
        generated_text = data[0]["generated_text"]
    elif isinstance(data, dict) and "generated_text" in data:
        generated_text = data["generated_text"]
    else:
        generated_text = str(data)

    return {"result": generated_text}

