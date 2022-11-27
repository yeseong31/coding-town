from flask import Blueprint, render_template, make_response, jsonify

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
def home():
    data = {'test': 200}
    return make_response(jsonify(data), 200)
