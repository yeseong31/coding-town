from flask import Blueprint, make_response, jsonify, request
from flask_restx import Namespace

from models import Todo

bp = Blueprint('todo', __name__, url_prefix='/todo')
Todos = Namespace(
    name="Todo",
    description="TEST: Todo API",
)


@bp.route('/', methods=('POST',))
def todo_post():
    data = request.json.get('data')
    Todo.create(data)
    result = {'create': 'success'}
    return make_response(jsonify(result), 200)


@bp.route('/<int:todo_id>', methods=('GET', 'PUT', 'DELETE'))
def todo_simple(todo_id):
    if request.method == 'GET':
        todo = Todo.get(todo_id)
        result = {'todo_id': todo[0], 'data': todo[1]}
        return make_response(jsonify(result), 200)

    elif request.method == 'PUT':
        data = request.args.get('data')
        Todo.update(todo_id, data)
        result = {'todo_id': todo_id, 'data': data}
        return make_response(jsonify(result), 200)

    elif request.method == 'DELETE':
        Todo.delete(todo_id)
        result = {'delete': 'success'}
        return make_response(jsonify(result), 200)
