from flask import Blueprint, render_template, request, redirect, send_file, jsonify, flash
import requests
import re
import os
import json
from datetime import datetime
from screengrab.extensions import db
from screengrab.models import Screenshot

def download_file(source_url):

    def save_binary_file(url, image_name):
        view = open(image_name, 'wb')
        view.write(requests.get(url).content)
        view.close()

    basedir = os.path.dirname(main.root_path)
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

    return True

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def upload_screenshot():

    if request.method == 'POST':
       
        source_url = request.form["source_url"]

        check_response = requests.get(source_url)
        if not check_response:
            return "<h1>URL NOT FOUND</h1>"
        else:
            download_file(source_url)

        db.session.commit()

    return render_template("request.html")