from flask import make_response, jsonify, request
from flask_restx import Namespace, Resource

from models import Todo

ns = Namespace(
    name="Todo",
    description="TEST: Todo API",
)


@ns.route('/')
class TodoPost(Resource):
    def post(self):
        data = request.json.get('data')
        Todo.create(data)
        result = {'create': 'success'}
        return make_response(jsonify(result), 200)


@ns.route('/<int:todo_id>')
class TodoSimple(Resource):
    def get(self, todo_id):
        todo = Todo.get(todo_id)
        result = {'todo_id': todo[0], 'data': todo[1]}
        return make_response(jsonify(result), 200)
    
    def put(self, todo_id):
        data = request.args.get('data')
        Todo.update(todo_id, data)
        result = {'todo_id': todo_id, 'data': data}
        return make_response(jsonify(result), 200)
    
    def delete(self, todo_id):
        Todo.delete(todo_id)
        result = {'delete': 'success'}
        return make_response(jsonify(result), 200)
