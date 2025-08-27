from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI()

# Меняем модель одной строчкой здесь:
HF_MODEL = os.environ.get("HF_MODEL", "facebook/bart-large-cnn")  # по умолчанию bart-large-cnn
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

class GenerateRequest(BaseModel):
    character: str
    topic: str
    length: int = 150  

@app.post("/generate")
async def generate_text(req: GenerateRequest):
    prompt = (
        f"Персонаж: '{req.character}'\n"
        f"Тема: '{req.topic}'\n"
        "Инструкция: Напиши короткий сценарий для вертикального видео "
        "(hook, 2-3 шага, call-to-action)."
    )

    payload = {"inputs": prompt}

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return {"error": f"Hugging Face API error: {response.text}"}

    data = response.json()

    if isinstance(data, list) and "summary_text" in data[0]:
        result_text = data[0]["summary_text"]
    else:
        result_text = str(data)

    return JSONResponse(content={"result": result_text},
                        media_type="application/json; charset=utf-8")
