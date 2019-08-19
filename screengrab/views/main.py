from flask import Blueprint, render_template, request, redirect, send_file, jsonify, flash, current_app, url_for
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

    uploads = '../static/uploads'
    
    thum_url = 'https://image.thum.io/get/wait/15/png/'

    desktop_url = '{}{}'.format(thum_url,source_url)
    mobile_url = '{}viewportWidth/800/{}'.format(thum_url,source_url)

    now = datetime.now()
    timestamp = now.strftime('%d-%m-%Y %H:%M:%S')
    
    img_name = re.sub('^https?:\/\/', '', source_url)

    desktop_image_name = '{}-desktop-{}.png'.format(img_name,timestamp)
    mobile_image_name = '{}-mobile-{}.png'.format(img_name,timestamp)

    desktop_image_location = '{}{}-desktop-{}.png'.format(uploads,img_name,timestamp)
    mobile_image_location = '{}{}-mobile-{}.png'.format(uploads,img_name,timestamp)

    save_binary_file(desktop_url, desktop_image_location)
    save_binary_file(mobile_url, mobile_image_location)

    screenshot = Screenshot(source_url=source_url, created_on=now, desktop_view=desktop_image_name, mobile_view=mobile_image_name)
    db.session.add(screenshot)

    message = 'Screenshots of {} have been uploaded'.format(source_url)
    flash(message)

    return True

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def upload_screenshot():

    if request.method == 'POST':
       
        source_url = request.form['source_url']

        try:
            check_response = requests.get(source_url)
        except requests.exceptions.ConnectionError:
            message = 'Could not access {}, please check if you submitted correct URL'.format(source_url)
            flash(message)
            return render_template('index.html')
        
        download_file(source_url)

        db.session.commit()

        desktop = db.session.query(Screenshot.desktop_view).order_by(Screenshot.id.desc()).first()
        mobile = db.session.query(Screenshot.mobile_view).order_by(Screenshot.id.desc()).first()
        
        desktop = desktop[0]
        mobile = mobile[0]

        return render_template('request.html', desktop=desktop, mobile=mobile)
    
    return render_template('index.html')

@main.route('/screenshots/<int:id>', methods=['GET'])
def get_screenshot(id):

    screenshot = Screenshot.query.get_or_404(id)
    desktop = screenshot.desktop_view
    mobile = screenshot.mobile_view

    return render_template("screenshot.html", screenshot=screenshot.to_json(), desktop=desktop, mobile=mobile)
