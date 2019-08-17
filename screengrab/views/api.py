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

@api.route('/screenshots', methods=['GET'])
def get_screenshots():

    screenshots = [screenshot.to_json() for screenshot in Screenshot.query.all()]

    return render_template("screenshots.html", screenshots=screenshots)


@api.route('/screenshots', methods=['POST'])
def post_screenshots():

    source_url = request.json['source_url']

    check_response = requests.get(source_url)
    if not check_response:
        return "<h1>URL NOT FOUND</h1>"
    else:
        download_file(source_url)

    db.session.commit()

    return source_url #render_template("screenshots.html", screenshots=screenshots)


@api.route('/screenshots/<int:id>', methods=['GET'])
def get_screenshot(id):

    screenshot = Screenshot.query.get_or_404(id)

    return render_template("screenshot.html", screenshot=screenshot.to_json())


@api.route('/', methods=['GET'])
def get_api():

    return """
    <!DOCTYPE html>
    <html>
        <head><title>SCREENGRAB API</title></head>
    <body>
        <h1>Screengrab API</h1>
        <p>Documentation required.</p>
    </body>
    </html>
    """
