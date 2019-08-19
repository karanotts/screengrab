from flask import Blueprint, render_template, request, redirect, send_file, jsonify, flash
import requests
import re
import os
import json
from datetime import datetime
from screengrab.extensions import db
from screengrab.models import Screenshot
from screengrab.views.main import download_file 


api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def get_api():

    return render_template("api.html")


@api.route('/screenshots', methods=['POST'])
def post_screenshots():

    source_url = request.json['source_url']

    try:
        check_response = requests.get(source_url)
    except requests.exceptions.ConnectionError:
        raise Exception(
            "Failed to establish connection to {}".format(source_url)
        )

    download_file(source_url)

    db.session.commit()

    return jsonify(source_url), 201

@api.route('/screenshots/<int:id>', methods=['GET'])
def get_screenshot(id):

    screenshot = Screenshot.query.get_or_404(id)
    screenshot = json.dumps(screenshot.to_json())

    return screenshot, 200


@api.route('/screenshots', methods=['GET'])
def get_screenshots():

    screenshots = db.session.query(Screenshot).order_by(Screenshot.created_on.desc())

    screenshots = json.dumps([screenshot.to_json() for screenshot in screenshots])

    return screenshots, 200
