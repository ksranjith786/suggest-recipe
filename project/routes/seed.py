import csv
from flask import Blueprint, redirect, url_for
from database.database import addRecipeToDB

seed_bp = Blueprint('seed', __name__, url_prefix='/seed')

@seed_bp.route('/recipes', methods=['GET'])
def seedRecipes():
  with open("static/csv/recipes.csv", mode="r") as file:
    recipes = csv.DictReader(file)
    for recipe in recipes:
      retVal = addRecipeToDB(
              name = recipe["name"],
              url = recipe["url"],
              type = recipe["type"],
              imageURL = recipe["imageURL"],
              ingredients = str(recipe["ingredients"]), # Converting list to string
              provider = recipe["provider"]
          )
      if retVal == False:
          print("Exception caught while adding recipe details to Database")
          return {"message": "Failed"}
      
  return redirect(url_for('ingredients.ingredients'))
