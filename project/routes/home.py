from flask import Blueprint, redirect, url_for

home_bp = Blueprint('home', __name__) # ignored url_prefix

@home_bp.route('/')
def index():
    return redirect(url_for('ingredients.ingredients'))

@home_bp.route('/home/') # Trialing / is important
def home():
    return "Hello, World Home!"
# end home
