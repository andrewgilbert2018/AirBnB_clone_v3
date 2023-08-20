#!/usr/bin/python3
"""Creating a new view for Amenity objects"""

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity
import json


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def handle_amenities():
    """return amenities in json"""
    if request.method == 'GET':
        amenities = []
        for amenity in storage.all('Amenity').values():
            amenities.append(amenity.to_dict())
        return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def fetch_single_amenity(amenity_id):
    """fetch single amenity"""
    amenity = {}
    for am in storage.all('Amenity').values():
        if am.to_dict().get('id') == amenity_id:
            amenity = am.to_dict()
    if not amenity:
        abort(404)
    return jsonify(amenity)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def post_amenity():
    """function to post amenity"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    amenity = request.get_json()
    if not amenity['name']:
        return jsonify({"error": "Missing name"}), 400
    newInstance = Amenity(amenity)
    newInstance.name = amenity.get("name")
    storage.new(newInstance)
    storage.save()
    return jsonify(newInstance.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def put_amenity(amenity_id):
    """Function that update amenity"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    obj = storage.get("Amenity", amenity_id)
    if not obj:
        abort(404)
    requestObj = request.get_json()
    obj.name = requestObj["name"]
    obj.save()
    return jsonify(obj.to_dict()), 200


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    """Function that delete amenity"""
    obj = storage.get("Amenity", amenity_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200
