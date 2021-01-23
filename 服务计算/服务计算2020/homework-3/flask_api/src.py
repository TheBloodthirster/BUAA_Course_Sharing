import json
from random import randint

import flask
from flask import request, abort, jsonify

app = flask.Flask(__name__)
KEYS = ("Ci6P9El8Pd", "5WDXCXnIVR", "fVs7DCyCER")


@app.route('/map/<int:n>', methods=['GET'])
def get_map(n):
    dst_map = {'n': n, 'dst_map': [[randint(0, 0xFFFF) if i != j else 0 for j in range(n)] for i in range(n)]}
    return jsonify(dst_map)


@app.route('/tasks', methods=['POST'])
def create_task():
    data = json.loads(request.data)
    if data.get('api_key') not in KEYS:
        abort(403)
    try:
        assert 1 <= int(data['map_size']) <= 25
    except (AssertionError, KeyError, ValueError):
        abort(400)
    return request.data, 201


app.run()
