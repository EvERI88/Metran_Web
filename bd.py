from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS  # Импорт CORS

app = Flask(__name__)
CORS(app)  # Разрешить CORS для всех маршрутов

# Подключение к базе данных SQLite
def connect_db():
    conn = sqlite3.connect('database.db')
    return conn

# Инициализация базы данных
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            co TEXT NOT NULL,
            coitem TEXT NOT NULL,
            item_details TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# API для добавления новых данных (первый метод)
@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()  # Получаем данные в формате JSON
    co = data.get('co')
    coitem = data.get('coitem')
    item_details = data.get('item_details')

    # Сохранение данных в БД
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (co, coitem, item_details) VALUES (?, ?, ?)',
                   (co, coitem, item_details))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Item added successfully'}), 201

# API для получения данных по идентификатору (второй метод)
@app.route('/api/items/<int:id>', methods=['GET'])
def get_item(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE id = ?', (id,))
    item = cursor.fetchone()
    conn.close()
    
    if item:
        return jsonify({
            'id': item[0],
            'co': item[1],
            'coitem': item[2],
            'item_details': item[3]
        })
    else:
        return jsonify({'message': 'Item not found'}), 404

# API для получения всех данных (третий метод)
@app.route('/api/items', methods=['GET'])
def get_all_items():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    
    # Преобразуем данные в список словарей
    result = []
    for item in items:
        result.append({
            'id': item[0],
            'co': item[1],
            'coitem': item[2],
            'item_details': item[3]
        })
    
    return jsonify(result)  # Вернём все данные в формате JSON

# Инициализация БД перед запуском
if __name__ == '__main__':
    init_db()  # Инициализация базы данных
    app.run(debug=True)
