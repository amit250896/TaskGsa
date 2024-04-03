from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

@app.route('/api/todo', methods=['GET'])
@jwt_required()
def get_todo_items():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    user_id = get_jwt_identity()
    todo_items = TodoItem.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)
    items = []
    for item in todo_items.items:
        items.append({'id': item.id, 'description': item.description, 'completed': item.completed})
    return jsonify({
        'items': items,
        'total_items': todo_items.total,
        'total_pages': todo_items.pages,
        'current_page': todo_items.page
    }), 200

@app.route('/api/todo', methods=['POST'])
@jwt_required()
def create_todo_item():
    data = request.get_json()
    description = data.get('description')
    if not description:
        return jsonify({'message': 'Missing description'}), 400
    user_id = get_jwt_identity()
    todo_item = TodoItem(user_id=user_id, description=description)
    db.session.add(todo_item)
    db.session.commit()
    return jsonify({'message': 'Todo item created successfully'}), 201

@app.route('/api/todo/<int:id>', methods=['GET'])
@jwt_required()
def get_todo_item(id):
    user_id = get_jwt_identity()
    todo_item = TodoItem.query.filter_by(id=id, user_id=user_id).first()
    if not todo_item:
        return jsonify({'message': 'Todo item not found'}), 404
    return jsonify({'id': todo_item.id, 'description': todo_item.description, 'completed': todo_item.completed}), 200

@app.route('/api/todo/<int:id>', methods=['PUT'])
@jwt_required()
def update_todo_item(id):
    data = request.get_json()
    description = data.get('description')
    completed = data.get('completed')
    user_id = get_jwt_identity()
    todo_item = TodoItem.query.filter_by(id=id, user_id=user_id).first()
    if not todo_item:
        return jsonify({'message': 'Todo item not found'}), 404
    if description:
        todo_item.description = description
    if completed is not None:
        todo_item.completed = completed
    db.session.commit()
    return jsonify({'message': 'Todo item updated successfully'}), 200

@app.route('/api/todo/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo_item(id):
    user_id = get_jwt_identity()
    todo_item = TodoItem.query.filter_by(id=id, user_id=user_id).first()
    if not todo_item:
        return jsonify({'message': 'Todo item not found'}), 404
    db.session.delete(todo_item)
    db.session.commit()
    return jsonify({'message': 'Todo item deleted successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
