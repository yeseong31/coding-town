import bcrypt
import jwt
from flask import request, make_response, jsonify
from flask_restx import Namespace, Resource, fields

ns = Namespace(
    name="Auth",
    description="Coding Town 사용자 인증 API",
)

user_fields = ns.model('User', {
    'name': fields.String(description='a User Name', required=True, example='name')
})

user_fields_auth = ns.inherit('User Auth', user_fields, {
    'password': fields.String(description='Password', required=True, example='password')
})

jwt_fields = ns.model('JWT', {
    'Authorization': fields.String(description='Authorization which you must inclued in header',
                                   required=True, example="eyJ0e----------")
})

users = {}


@ns.route('/register')
class AuthRegister(Resource):
    @ns.expect(user_fields_auth)
    @ns.doc(responses={200: 'Success', 500: 'Register Failed'})
    def post(self):
        name = request.json.get('name')
        password = request.json.get('password')

        if name in users:
            return make_response({'message': 'Register Failed'}, 500)

        users[name] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        data = {'Authorization': jwt.encode({'name': name}, 'secret', algorithm='HS256')}
        return make_response(jsonify(data), 200)


@ns.route('/login')
class AuthLogin(Resource):
    @ns.expect(user_fields_auth)
    @ns.doc(responses={200: 'Success', 404: 'Not Found', 500: 'Auth Failed'})
    def post(self):
        name = request.json.get('name')
        password = request.json.get('password')

        if name not in users:
            data = {'message': 'User Not Found'}
            status_code = 404
        elif not bcrypt.checkpw(password.encode('utf-8'), users[name].encode('utf-8')):
            data = {'message': 'Auth Failed'}
            status_code = 500
        else:
            data = {'Authorization': jwt.encode({'name': name}, 'secret', algorithm='HS256')}
            status_code = 200

        return make_response(jsonify(data), status_code)


@ns.route('/get')
class AuthGet(Resource):
    @ns.doc(responses={200: 'Success', 404: 'Login Failed'})
    def post(self):
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음

        if header is None:
            return {'message': 'Please Login'}, 404

        data = jwt.decode(header, 'secret', algorithms='HS256')
        return make_response(jsonify(data), 200)
