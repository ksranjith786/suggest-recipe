import csv
from flask import Blueprint, request
from database.database import addRecipeToDB

seed_bp = Blueprint('seed', __name__, url_prefix='/seed')

@seed_bp.route('/recipes', methods=['GET'])
def seedRecipes():
  with open("recipes.csv", mode="r") as file:
        data = csv.DictReader(file)
        retVal = addRecipeToDB(
                name = name,
                url = url,
                type = type,
                imageURL = imageURL,
                ingredients = str(ingredients), # Converting list to string
                provider = provider
            )
        if retVal == False:
            print("Exception caught while adding recipe details to Database")
            return False
