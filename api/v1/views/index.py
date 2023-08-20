#!/usr/bin/python3
"""
The index flask app
routes:
       /status: display "status": "OK"
       /stats: display count of all classes
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def showStatus():
    """a function thatcShow status of the flask app"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def showStats():
    """ a function that show the count for the classes"""
    jsonOut = {"amenities": storage.count('Amenity'),
               "cities": storage.count('City'),
               "places": storage.count('Place'),
               "reviews": storage.count('Review'),
               "states": storage.count('State'),
               "users": storage.count('User'),
               }
    return jsonify(jsonOut)
