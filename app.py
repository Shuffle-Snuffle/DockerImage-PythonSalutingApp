from flask import Flask, request
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "/data/visits.json"

def load_data():
    if os.path.exists(DATA_FILE):
        # Явно указываем кодировку utf-8 при чтении
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    return {"date": str(datetime.now().date()), "visits": {}}

def save_data(data):
    # Явно указываем кодировку utf-8 при записи
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

@app.route('/')
def hello():
    ip = request.remote_addr
    today = str(datetime.now().date())
    
    data = load_data()
    
    # Если наступил новый день, сбрасываем счетчики
    if data.get("date") != today:
        data = {"date": today, "visits": {}}
        
    # Увеличиваем счетчик для текущего IP
    count = data["visits"].get(ip, 0) + 1
    data["visits"][ip] = count
    
    save_data(data)
    
    # Выбираем фразу в зависимости от количества
    if count == 1:
        phrase = "Привет! Вижу вас впервые. Добро пожаловать!"
    elif count <= 5:
        phrase = f"С возвращением! Вы заходите уже {count}-й раз за сегодня."
    else:
        phrase = f"Ого, {count} раз за день! Вы тут почти живёте!"
        
    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>User Saluting App</title>
    </head>
    <body>
        <div style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1>User Saluting App</h1>
            <p>Ваш IP: <b>{ip}</b></p>
            <p>Посещений сегодня: <b>{count}</b></p>
            <h2 style="color: #2E86C1;">{phrase}</h2>
            <p style="color: gray; font-size: 12px;">Дата: {today}</p>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)