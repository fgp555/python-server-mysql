from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory database to store todos
todos = [
    {"id": 1, "todo": "Buy groceries", "done": True},
    {"id": 2, "todo": "Walk the dog", "done": False},
]

# Route for the index page
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Get all todos
@app.route('/api/todo', methods=['GET'])
def get_all_todos():
    return jsonify(todos)

# Get a specific todo by ID
@app.route('/api/todo/<int:id>', methods=['GET'])
def get_todo_by_id(id):
    todo = next((todo for todo in todos if todo["id"] == id), None)
    if todo:
        return jsonify(todo)
    return jsonify({"error": "Todo not found"}), 404

# Add a new todo
@app.route('/api/todo/create', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_todo = {
        "id": len(todos) + 1,  # Simple ID generation
        "todo": data['todo'],
        "done": data.get('done', False)
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201

# Update a specific todo by ID
@app.route('/api/todo/update/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    todo = next((todo for todo in todos if todo["id"] == id), None)
    if todo:
        todo['todo'] = data['todo']
        todo['done'] = data['done']
        return jsonify(todo)
    return jsonify({"error": "Todo not found"}), 404

# Delete a todo by ID
@app.route('/api/todo/delete/<int:id>', methods=['DELETE'])
def delete_todo(id):
    global todos
    todos = [todo for todo in todos if todo["id"] != id]
    return jsonify({"message": "Todo deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)