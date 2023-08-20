#!/usr/bin/python3
"""A Python Script for flask app file"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from os import getenv


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_storage(exception):
    """a func that closes the storage session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """a func that hanfles the not found error page"""
    return jsonify(
        {
            'error': 'Not found'
        }
    ), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
