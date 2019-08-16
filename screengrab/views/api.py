from flask import Blueprint, render_template, request, redirect, send_file, jsonify, flash
import requests
import re
import os
import json
from datetime import datetime
from screengrab.extensions import db
from screengrab.models import Screenshot


api = Blueprint('api', __name__)

@api.route('/upload', methods=['GET', 'POST'])
def upload_screenshot():

    if request.method == 'POST':
       
        def download_file(source_url):

            def save_binary_file(url, image_name):
                view = open(image_name, 'wb')
                view.write(requests.get(url).content)
                view.close()

            basedir = os.path.dirname(api.root_path)
            uploads = os.path.join(basedir, 'static/uploads/')
            if not os.path.isdir(uploads):
                os.mkdir(uploads)
            
            thum_url = "https://image.thum.io/get/wait/15/png/"

            desktop_url = "{}{}".format(thum_url,source_url)
            mobile_url = "{}viewportWidth/800/{}".format(thum_url,source_url)

            now = datetime.now()
            timestamp = now.strftime('%d-%m-%Y %H:%M:%S')
            
            img_name = re.sub('^https?:\/\/', '', source_url)

            desktop_image_name = '{}{}-desktop-{}.png'.format(uploads,img_name,timestamp)
            mobile_image_name = '{}{}-mobile-{}.png'.format(uploads,img_name,timestamp)

            save_binary_file(desktop_url, desktop_image_name)
            save_binary_file(mobile_url, mobile_image_name)

            screenshot = Screenshot(source_url=source_url, created_on=now, desktop_view=desktop_image_name, mobile_view=mobile_image_name)
            db.session.add(screenshot)
 
            message = "Screenshots of {} have been uploaded to {}".format(source_url,desktop_image_name)
            flash(message)

        source_url = request.form["source_url"]

        check_response = requests.get(source_url)
        if not check_response:
            return "<h1>URL NOT FOUND</h1>"
        else:
            download_file(source_url)

        db.session.commit()

    return render_template("request.html")


@api.route('/screenshots', methods=['GET'])
def get_screenshots():

    screenshots = [screenshot.to_json() for screenshot in Screenshot.query.all()]
    # screenshots = json.dumps(screenshots, sort_keys=False, indent=2)
    return render_template("screenshots.html", screenshots=screenshots)

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
