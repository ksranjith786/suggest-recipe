from flask import Blueprint, redirect, url_for
from database.database import queryIngredientsFromDB

home_bp = Blueprint('home', __name__) # ignored url_prefix

@home_bp.route('/')
def index():
    # Webserver do not load db everytime when we deploy. so we does this hack to load data from csv
    rs = queryIngredientsFromDB("oil;", "any")
    ids = []
    for result in rs:
        ids.append(result.id)
    
    if len(ids) == 0:
        return redirect(url_for('seed.seedRecipes'))
    
    return redirect(url_for('ingredients.ingredients'))

@home_bp.route('/home/') # Trialing / is important
def home():
    return "Hello, World Home!"
# end home
