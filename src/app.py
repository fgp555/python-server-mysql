# src/app.py

from flask import Flask, jsonify, request
import mysql.connector
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la conexión a MySQL desde .env
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# Inicializar la app Flask
app = Flask(__name__, static_folder='../static', static_url_path='/static')

# Función para obtener la conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Route for the index page
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Obtener todas las tareas
@app.route('/api/todo', methods=['GET'])
def get_all_todos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(todos)

# Obtener una tarea por ID
@app.route('/api/todo/<int:id>', methods=['GET'])
def get_todo_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM todos WHERE id = %s", (id,))
    todo = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(todo) if todo else (jsonify({"error": "Todo not found"}), 404)

# Agregar una nueva tarea
@app.route('/api/todo/create', methods=['POST'])
def add_todo():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (todo, done) VALUES (%s, %s)", (data['todo'], data.get('done', False)))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": new_id, "todo": data['todo'], "done": data.get('done', False)}), 201

# Actualizar una tarea por ID
@app.route('/api/todo/update/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET todo = %s, done = %s WHERE id = %s", (data['todo'], data['done'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"id": id, "todo": data['todo'], "done": data['done']}), 200

# Eliminar una tarea por ID
@app.route('/api/todo/delete/<int:id>', methods=['DELETE'])
def delete_todo(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Todo deleted"}), 200

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
