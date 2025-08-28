from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Разрешаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ["http://localhost:5173"] если хочешь ограничить
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель по умолчанию (если не задана в переменных окружения)
HF_MODEL = os.environ.get("HF_MODEL", "tiiuae/falcon-7b-instruct")
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
    # Формируем улучшенный промпт
    prompt = (
        f"Создай сценарий для короткого вертикального видео.\n\n"
        f"Персонаж: {req.character}\n"
        f"Тема: {req.topic}\n\n"
        f"Формат:\n"
        f"Hook → 2-3 шага → Call-to-action\n\n"
        f"Сценарий:"
    )

    payload = {"inputs": prompt}

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json=payload,
            timeout=60
        )
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

    if response.status_code != 200:
        return {"error": f"Hugging Face API error: {response.text}"}

    data = response.json()
    print("DEBUG RESPONSE:", data)  # лог для отладки

    result_text = None
    if isinstance(data, list):
        if "generated_text" in data[0]:
            result_text = data[0]["generated_text"]
        elif "summary_text" in data[0]:
            result_text = data[0]["summary_text"]
    else:
        result_text = str(data)

    if not result_text:
        result_text = "⚠️ Модель не смогла сгенерировать текст. Попробуйте снова."

    return JSONResponse(content={"result": result_text},
                        media_type="application/json; charset=utf-8")
