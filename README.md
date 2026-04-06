# AI Stock Screener (MOEX)

Прототип API-сервиса для анализа акций Московской биржи с использованием локальной LLM (Ollama + Mistral).

## Функционал
- Получение данных по акциям с MOEX ISS API
- Расчет базовых метрик (P/E, ROE, дивиденды)
- Генерация анализа через локальную LLM
- Возврат структурированного JSON

## Установка

1. Клонировать репозиторий
```bash
git clone <repo_url>
cd project

2. Установить зависимости
pip install -r requirements.txt

3. Установить Ollama
Запустить модель:

ollama pull mistral
ollama serve

4. Запустить сервер
python -m uvicorn main:app --reload

5. Открыть Swagger
http://127.0.0.1:8000/docs

Пример запроса:
{
  "ticker": "SBER"
}

Пример ответа:
{
  "strengths": "...",
  "risks": "...",
  "conclusion": "..."
}