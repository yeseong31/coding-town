from flask import make_response, jsonify, request
from flask_restx import Namespace, Resource, fields

from models import Todo

ns = Namespace(
    name="Todo",
    description="TEST: Todo API",
)
todo_fields = ns.model(
    'Todo',
    {'data': fields.String(description='a Todo', required=True, example='what to do')}
)
todo_fields_with_id = ns.inherit(
    'Todo With ID', todo_fields,
    {'todo_id': fields.Integer(description='a Todo ID')}
)


@ns.route('/')
class TodoPost(Resource):
    @ns.expect(todo_fields)
    @ns.response(201, 'Success', todo_fields_with_id)
    def post(self):
        """To do 리스트에 할 일을 등록하는 함수"""
        data = request.json.get('data')
        Todo.create(data)
        result = {'create': 'success'}
        return make_response(jsonify(result), 200)


@ns.route('/<int:todo_id>')
@ns.doc(params={'todo_id': 'To Do List의 ID'})
class TodoSimple(Resource):
    @ns.doc(responses={202: 'Success'})
    @ns.doc(responses={500: 'Failed'})
    def get(self, todo_id):
        """To do 리스트에 todo_id와 일치하는 ID의 할 일을 조회하는 함수"""
        todo = Todo.get(todo_id)
        result = {'todo_id': todo[0], 'data': todo[1]}
        return make_response(jsonify(result), 200)

    @ns.doc(responses={202: 'Success'})
    @ns.doc(responses={500: 'Failed'})
    def put(self, todo_id):
        """To do 리스트에 todo_id와 일치하는 ID의 할 일을 수정하는 함수"""
        data = request.args.get('data')
        Todo.update(todo_id, data)
        result = {'todo_id': todo_id, 'data': data}
        return make_response(jsonify(result), 200)

    @ns.doc(responses={202: 'Success'})
    @ns.doc(responses={500: 'Failed'})
    def delete(self, todo_id):
        """To do 리스트에 todo_id와 일치하는 ID의 할 일을 삭제하는 함수"""
        Todo.delete(todo_id)
        result = {'delete': 'success'}
        return make_response(jsonify(result), 200)
