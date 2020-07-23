from flask import Blueprint, render_template

ingredients_bp = Blueprint('ingredients', __name__, url_prefix='/ingredients')

@ingredients_bp.route('/', methods=['GET', 'POST']) # The URL could be either .../details or .../details/; But if '' instead of '/' is used then .../details only works
def ingredients():
    return render_template('ingredients.html')
# end ingredients
