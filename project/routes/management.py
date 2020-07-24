from flask import Blueprint, render_template, render_template_string
from database.database import createRecipeDB, addRecipeToDB, queryRecipeFromDB, queryIngredientsFromDB, deleteRecipeFromDB
from sites.soup.findSites import run

management_bp = Blueprint('management', __name__, url_prefix='/management')

@management_bp.route('/data/scrape/<string:provider>', methods=['GET'])
def scrapeSite(provider: str):
    url = "https://hebbarskitchen.com"
    retVal = run(url, provider)
    msg = "Scraping Data from " + provider + " is successful"
    if retVal is False:
        return "Failed to scrape Data from " + provider

    return msg
# end scrapeSite

@management_bp.route('/createdb', methods=['GET'])
def createDB():
    createRecipeDB()
    return "Created a Database"
#end createDB

@management_bp.route('/recipe', methods=['GET']) # The URL could be either .../details or .../details/; But if '' instead of '/' is used then .../details only works
def addRecipe():
    ret = addRecipeToDB(name="akki roti recipe | masala akki rotti recipe | rice flour roti", url="https://hebbarskitchen.com/akki-roti-recipe-masala-akki-rotti/", type="Breakfast", ingredients="['2 cup rice flour', '1 onion, finely chopped', '2 tbsp dill leaves / sabbasige sopp tbsp, curry leaves, finely chopped', '1 iu', '2 tbsp coriander, finely chopped', '2 tbsp, curry leaves, finely chopped', '1 inch ginger, grated', '2 chilli, finely chopped', '1 tsp cumin', '1 tsp salt', 'water, as required', 'oil, for roasting']", imageURL="https://hebbarskitchen.com/wp-content/uploads/2020/07/akki-roti-recipe-masala-akki-rotti-recipe-rice-flour-roti-1-200x300.jpg", provider="Hebbar's Kitchen")
    msg = "Failed to add recipe"
    if ret == True:
        msg = "Added recipe successfully"
    
    return msg
# end addRecipe

#(akki roti recipe | masala akki rotti recipe | rice flour roti, https://hebbarskitchen.com/wp-content/uploads/2020/07/akki-roti-recipe-masala-akki-rotti-recip7/akki-roti-recipe-masala-akki-rotti-recipe-rice-flour-roti-1-200x300.jpg, ['2 cup rice flour', '1 onion, finely chopped', '2 tbsp dill leaves / sabbasige sopp tbsp, curry leaves, finely chopped', '1 iu', '2 tbsp coriander, finely chopped', '2 tbsp, curry leaves, finely chopped', '1 inch ginger, grated', '2 chilli, finely chopped', '1 tsp cumin', '1 tsp salt', 'water, as required', 'oil, for roasting'])
@management_bp.route('/recipe/<string:name>', methods=['GET'])
def queryRecipe(name: str):
    rs = queryRecipeFromDB(name)
    if rs is None:
        return "No such recipe to fetch! or No such recipe table/rows exists"
    
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

@management_bp.route('/recipe/delete/<int:id>', methods=['GET'])
def deleteRecipe(id: int):
    retVal = deleteRecipeFromDB(id)
    if retVal is False:
        return "Failed to delete recipe"
    
    return "Deleted recipe"
# end deleteReceipe
