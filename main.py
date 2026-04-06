# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import ollama
import json
import re

app = FastAPI(title="AI Stock Screener MOEX")

# -----------------------
# Модель запроса
# -----------------------
class StockRequest(BaseModel):
    ticker: str

# -----------------------
# Функция для получения данных с MOEX
# -----------------------
def get_moex_metrics(ticker: str):
    url = f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}.json"
    
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        raise HTTPException(status_code=500, detail="Ошибка подключения к MOEX API")

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=f"Тикер {ticker} не найден на MOEX")
    
    data = response.json()
    market_data = data.get('marketdata', {}).get('data', [])
    columns = data.get('marketdata', {}).get('columns', [])
    
    if not market_data:
        raise HTTPException(status_code=404, detail=f"Нет рыночных данных по тикеру {ticker}")
    
    df_row = dict(zip(columns, market_data[0]))
    
    def safe_float(value):
        try:
            return float(value)
        except:
            return 0.0
    
    return {
        "pe": safe_float(df_row.get('P/E')),
        "roe": safe_float(df_row.get('ROE')),
        "div_yield": safe_float(df_row.get('DIVIDEND'))
    }

# -----------------------
# Функция очистки ответа Ollama
# -----------------------
def parse_ollama_response(text: str):
    text = text.strip().replace("```json", "").replace("```", "")
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)
    try:
        data = json.loads(text)
        for key in ["strengths", "risks"]:
            if key in data and isinstance(data[key], list):
                data[key] = " ".join(data[key])
        return data
    except json.JSONDecodeError:
        return {
            "strengths": "Ошибка парсинга",
            "risks": text,
            "conclusion": "Не удалось разобрать JSON"
        }

# -----------------------
# Основная функция анализа
# -----------------------
def analyze_stock(ticker: str, metrics: dict):
    prompt = f"""
    Ты профессиональный инвестиционный аналитик российского фондового рынка.

    Пиши кратко, по делу, на русском языке.

    Используй конкретные цифры из входных данных.

    Отвечай ТОЛЬКО в JSON формате.

    Формат:
    {{
      "strengths": "2-3 конкретных факта",
      "risks": "2-3 конкретных риска",
      "conclusion": "чёткий вывод: интересно / нейтрально / рискованно"
    }}

    Данные:
    Акция: {ticker}
    P/E: {metrics['pe']}
    ROE: {metrics['roe']}
    Дивидендная доходность: {metrics['div_yield']}
    """

    response = ollama.chat(
        model='mistral',
        messages=[{'role': 'user', 'content': prompt}],
        options={"temperature": 0.7}
    )

    raw_text = response['message']['content']
    return parse_ollama_response(raw_text)

# -----------------------
# Endpoint FastAPI
# -----------------------
@app.post("/analyze")
async def analyze(req: StockRequest):
    metrics = get_moex_metrics(req.ticker)
    result = analyze_stock(req.ticker, metrics)
    return result