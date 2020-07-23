from flask import Blueprint, render_template, request
from sites.soup.ingredients import IngredientsExtractor
from database.database import queryIngredientsFromDB

recipes_bp = Blueprint('recipes', __name__, url_prefix='/recipes')

@recipes_bp.route('', methods=['GET', 'POST']) # The URL could be either .../details or .../details/; But if '' instead of '/' is used then .../details only works
def recipes():
    mealType = request.form.get("meal", default = "breakfast", type = str)
    combination = request.form.get("combination", default = "all", type = str)
    ingredients = request.form.getlist('ingredient')
    ingredientString = ""
    for ingredient in ingredients:
        ingredientString += ingredient + ";"
    ingredientString = ingredientString[:len(ingredientString) - 1]
    #print(mealType, ingredientString)
    
    rs = queryIngredientsFromDB(ingredientString, combination)
    if rs is None:
        return "No such Ingredients for recipe(s)"
    
    recipes = []
    for result in rs:
        recipe = dict()
        recipe['id'] = result.id
        recipe['name'] = result.name
        recipe['url'] = result.url
        recipe['type'] = result.type
        recipe['ingredients'] = result.ingredients
        recipe['imageURL'] = result.imageURL
        recipe['provider'] = result.provider

        recipes.append(recipe)
    
    #print(recipes)
    return render_template('recipes.html',
        recipes = recipes
    )
    """
    URL = 'https://hebbarskitchen.com/plain-dosa/'
    ingredientsExt = IngredientsExtractor(URL)
    title = ingredientsExt.getTitle()
    imageURL = ingredientsExt.getImageUrl()
    recipesList = ingredientsExt.getIngredients()
    #print(ingredientsExt)
    
    return render_template('recipes.html', rName = title, rList = recipesList, rLink = URL, rImageURL = imageURL)
    """
# end recipes
