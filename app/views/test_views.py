from flask import request, make_response, jsonify
from flask_restx import Namespace, Resource, fields

ns = Namespace(
    name="Test",
    description="Test Playground",
)

test_fields = ns.model(
    'Test',
    {'data': fields.String(description='Test!!', required=True, example='require test data')}
)


@ns.route('/')
@ns.doc(responses={202: 'Success', 500: 'Failed'})
class TestClass(Resource):
    @ns.expect(test_fields)
    def post(self):
        data = request.json.get('data')
        return make_response(jsonify(data), 200)
