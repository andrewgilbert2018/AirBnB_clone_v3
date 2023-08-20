#!/usr/bin/python3
"""Creating a new view for city objects"""

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City
import json


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def handle_city(city_id):
    """return states in json"""
    if request.method == 'GET':
        city = {}
        for ci in storage.all('City').values():
            if ci.to_dict().get('id') == city_id:
                city = ci.to_dict()
        if not city:
            abort(404)
        return jsonify(city)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def fetch_cities(state_id):
    """fetch cities for a state"""
    cities = []
    for state in storage.all('State').values():
        if state.to_dict().get('id') == state_id:
            for city in state.cities:
                cities.append(city.to_dict())
    if not cities:
        abort(404)
    return jsonify(cities)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def post_city(state_id):
    """function to post state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    city = request.get_json()
    if not city['name']:
        return jsonify({"error": "Missing name"}), 400
    newInstance = City(city)
    newInstance.name = city.get("name")
    newInstance.state_id = state_id
    storage.new(newInstance)
    storage.save()
    return jsonify(newInstance.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_city(city_id):
    """Function that update city"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    obj = storage.get("City", city_id)
    if not obj:
        abort(404)
    requestObj = request.get_json()
    obj.name = requestObj["name"]
    obj.save()
    return jsonify(obj.to_dict()), 200


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """Function that delete state"""
    obj = storage.get("City", city_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200
