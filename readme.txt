# AI Stock Screener — MOEX

Прототип сервиса для анализа акций на Московской бирже с использованием локальной LLM.

## Функции
- Сбор данных по акциям с MOEX (ISS API, AlgoPack)
- Расчет фундаментальных показателей (P/E, ROE, Dividend Yield и др.)
- Анализ и генерация отчета с помощью локальной LLM (Mistral через Ollama)
- Интерфейс: FastAPI API + тест через Swagger `/docs`

## Структура проекта
ai-stock-screener/
├── src/
│ ├── data/
│ │ ├── moex_client.py
│ │ ├── algopack_client.py
│ │ └── models.py
│ ├── metrics/
│ │ ├── fundamentals.py
│ │ └── scoring.py
│ ├── ai/
│ │ ├── analyzer.py
│ │ └── prompts.py
│ └── interface/
│ └── main.py
├── data/
│ ├── sample.db
│ └── cache/
├── requirements.txt
├── .gitignore
└── README.md