from flask import Blueprint

api = Blueprint('api', __name__)

@api.route('/item', methods=['GET', 'POST'])
def post_screenshot():
    return "<h1>Item</h1>"

@api.route('/items', methods=['GET'])
def get_screenshots():
    return "<h1>Items</h1>"