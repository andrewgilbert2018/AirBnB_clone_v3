#!/usr/bin/python3
"""Creating a new view for state objects"""

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
import json


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def handle_states():
    """return states in json"""
    if request.method == 'GET':
        states = []
        for state in storage.all('State').values():
            states.append(state.to_dict())
        return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def fetch_single_state(state_id):
    """fetch a single state"""
    state = {}
    for st in storage.all('State').values():
        if st.to_dict().get('id') == state_id:
            state = st.to_dict()
    if not state:
        abort(404)
    return jsonify(state)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    """function to post state"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    state = request.get_json()
    if not state['name']:
        return jsonify({"error": "Missing name"}), 400
    newInstance = State(state)
    newInstance.name = state.get("name")
    storage.new(newInstance)
    storage.save()
    return jsonify(newInstance.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_state(state_id):
    """Function that update state"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    obj = storage.get("State", state_id)
    if not obj:
        abort(404)
    requestObj = request.get_json()
    obj.name = requestObj["name"]
    obj.save()
    return jsonify(obj.to_dict()), 200


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """Function that delete state"""
    obj = storage.get("State", state_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200
