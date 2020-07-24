from flask import Blueprint, render_template, request
from sites.soup.ingredients import IngredientsExtractor
from database.database import queryIngredientsFromDB
import random

recipes_bp = Blueprint('recipes', __name__, url_prefix='/recipes')

@recipes_bp.route('', methods=['GET', 'POST']) # The URL could be either .../details or .../details/; But if '' instead of '/' is used then .../details only works
def recipes():
    mealType = request.form.get("meal", default = "breakfast", type = str)
    combination = request.form.get("combination", default = "all", type = str)
    ingredients = request.form.getlist('ingredient')

    # When the list of ingredient(s) is empty
    if len(ingredients) == 0:
        return "Please select any ingredient!"

    ingredientString = ""
    for ingredient in ingredients:
        ingredientString += ingredient + ";"
    ingredientString = ingredientString[:len(ingredientString) - 1]
    #print(mealType, ingredientString)
    
    rs = queryIngredientsFromDB(ingredientString, combination)
    if rs is None:
        msg = "No such Ingredients to fetch recipe(s)"
        if combination == "all":
            msg = "No such combination of Ingredients to fetch recipe(s). Try with [Any] combination instead of all;"
        return msg
    
    #colors = ["SpringGreen", "SaddleBrown", "LightGrey", "OldLace", "Azure", "LightGreen", "GhostWhite", "Chartreuse", "Teal", "PaleTurquoise", "LightSteelBlue", "MediumBlue", "Cornsilk", "NavajoWhite"]
    colors = ["Salmon","Red","DarkGreen","DarkCyan","HotPink","DarkOliveGreen","DarkOrange","DarkTurquoise","DarkSlateGray","Indigo","Goldenrod","LightCoral","LightSeaGreen","Magenta","SlateBlue","DimGrey"]
    recipes = []
    for result in rs:
        recipe = dict()
        recipe['id'] = result.id
        recipe['name'] = result.name.strip().lower().replace('recipe', '').capitalize()
        recipe['url'] = result.url
        recipe['type'] = result.type.capitalize()
        recipe['ingredients'] = result.ingredients
        recipe['imageURL'] = result.imageURL
        recipe['provider'] = result.provider
        recipe['color1'] = colors[random.randint(0, len(colors)/2)]
        recipe['color2'] = colors[random.randint(len(colors)/2, len(colors)- 1)]

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
