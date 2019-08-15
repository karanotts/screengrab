from flask import Blueprint, render_template

api = Blueprint('api', __name__)

@api.route('/item', methods=['GET', 'POST'])
def post_screenshot():
    return render_template("request.html")

@api.route('/items', methods=['GET'])
def get_screenshots():
    return render_template("screenshot.html")