from flask import Blueprint, render_template, render_template_string, request
from database.database import createRecipeDB, addRecipeToDB, queryRecipeFromDB, queryIngredientsFromDB, deleteRecipeFromDB
from sites.soup.findSites import run

fetch_bp = Blueprint('fetch', __name__, url_prefix='/fetch')

def getRecipesFromResult(rs):
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
    return recipes
# end getRecipesFromResult

@fetch_bp.route('/recipe/name/<string:_name>', methods=['GET'])
def queryRecipe(_name: str):
    rs = queryRecipeFromDB("name", _name)
    if rs is None:
        return "No such recipe to fetch! or No such recipe table/rows exists"
    
    recipes = getRecipesFromResult(rs)
    #print(recipes)
    return render_template('recipes_v0.html',
        recipes = recipes
    )
"""
    return render_template_string('''
        <ul>
        {% for recipe in recipes %}
            <li>{{ recipe.name }}</li>
            <li><a href="{{ recipe.url }}">Link</a></li>
            <li>{{ recipe.type }}</li>
            <li>{{ recipe.ingredients }}</li>
            <li>{{ recipe.imageURL }}</li>
            <li><img src="{{ recipe.imageURL }}"></img></li>
            <li>{{ recipe.provider }}</li>
        {% endfor %}
        </ul>
        ''', recipes=recipes
        )
"""
# end queryRecipe

@fetch_bp.route('/recipe/type/<string:_type>', methods=['GET'])
def queryType(_type: str):
    rs = queryRecipeFromDB("type", _type)
    if rs is None:
        return "No such recipe types to fetch! or No such recipe table/rows exists"
    
    recipes = getRecipesFromResult(rs)
    #print(recipes)
    return render_template('recipes_v0.html',
        recipes = recipes
    )
# end queryType

@fetch_bp.route('/recipe/delete/<int:id>', methods=['GET'])
def deleteRecipe(id: int):
    retVal = deleteRecipeFromDB(id)
    if retVal is False:
        return "Failed to delete recipe"
    
    return "Deleted recipe"
# end deleteReceipe
