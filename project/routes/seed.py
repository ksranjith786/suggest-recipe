import csv
import os
from flask import Blueprint, redirect, url_for, current_app
from database.database import addRecipeToDB

seed_bp = Blueprint('seed', __name__, url_prefix='/seed')

def _recipes_csv_path():
    return os.path.join(current_app.root_path, 'static', 'csv', 'recipes.csv')

@seed_bp.route('/recipes', methods=['GET'])
def seedRecipes():
  csv_path = _recipes_csv_path()
  with open(csv_path, mode="r", encoding="utf-8") as file:
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
