#!/usr/bin/python3
"""Creating a new view for city objects"""

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
import json


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def handle_review(review_id):
    """return places in json"""
    if request.method == 'GET':
        review = {}
        for re in storage.all('Review').values():
            if re.to_dict().get('id') == review_id:
                review = re.to_dict()
        if not review:
            abort(404)
        return jsonify(review)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def fetch_reviews(place_id):
    """fetch places for a state"""
    reviews = []
    for place in storage.all('Review').values():
        if place.to_dict().get('id') == place_id:
            for review in place.reviews:
                reviews.append(review.to_dict())
    if not reviews:
        abort(404)
    return jsonify(reviews)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def post_review(place_id):
    """function to post review"""
    place = storage.get("Review", review_id)
    if not review:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    review = request.get_json()
    if not review['text']:
        return jsonify({"error": "Missing text"}), 400
    elif not review['user_id']:
        return jsonify({"error": "Mising user_id"}), 400
    elif not storage.get('User', place['user_id']):
        abort(404)
    else:
        newInstance = Review(review)
        for j in review.keys():
            setattr(newInstance, j, review[j])
    storage.new(newInstance)
    storage.save()
    return jsonify(newInstance.to_dict()), 201



@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def put_review(review_id):
    """Function that update city"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    obj = storage.get("Review", review_id)
    if not obj:
        abort(404)
    requestObj = request.get_json()
    ignores = ("id", "user_id", "place_id", "created_at", "updated_at")
    for i in requestObj.keys():
        if i in ignores:
            pass
        else:
            setattr(obj, i, requestObj[i])
    obj.save()
    return jsonify(obj.to_dict()), 200


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """Function that delete review"""
    obj = storage.get("Review", review_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200
