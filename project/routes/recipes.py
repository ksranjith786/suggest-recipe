from flask import Blueprint, render_template
from sites.soup.ingredients import IngredientsExtractor

recipes_bp = Blueprint('recipes', __name__, url_prefix='/recipes')

@recipes_bp.route('', methods=['GET', 'POST']) # The URL could be either .../details or .../details/; But if '' instead of '/' is used then .../details only works
def recipes():
    URL = 'https://hebbarskitchen.com/plain-dosa/'
    ingredientsExt = IngredientsExtractor(URL)
    title = ingredientsExt.getTitle()
    imageURL = ingredientsExt.getImageUrl()
    recipesList = ingredientsExt.getIngredients()
    #print(ingredientsExt)

    return render_template('recipes.html', rName = title, rList = recipesList, rLink = URL, rImageURL = imageURL)
# end estimate
