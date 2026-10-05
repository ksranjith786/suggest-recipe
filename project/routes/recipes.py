import ast
from urllib.parse import urlparse

from flask import Blueprint, jsonify, render_template, request, session

from database.database import queryIngredientsFromDB

recipes_bp = Blueprint('recipes', __name__, url_prefix='/recipes')

RECIPES_PAGE_SIZE = 25
MAX_RECIPES_PAGE = 100
ALLOWED_MEALS = {'breakfast', 'lunch', 'snacks', 'dinner'}
ALLOWED_COMBINATIONS = {'any', 'all'}
ALLOWED_INGREDIENTS = {
    'millet', 'oats', 'rice', 'idli rice', 'dosa rice', 'wheat flour', 'maida',
    'rice flour', 'ragi flour', 'corn flour', 'besan', 'bread', 'rava',
    'sooji', 'vermicelli', 'noodles', 'sabudana', 'poha',
    'moong dal', 'chana dal', 'toor dal', 'urad dal',
    'curd', 'milk', 'ghee', 'butter', 'cheese', 'cream', 'paneer',
    'tomato', 'onion', 'potato', 'carrot', 'capsicum', 'peas', 'beans',
    'cabbage', 'cauliflower', 'palak', 'spinach', 'methi', 'mushroom', 'corn',
    'badam', 'cashew', 'pumpkin seeds', 'peanut', 'sesame', 'coconut',
    'jaggery', 'tamarind', 'soy', 'oil',
}


def _normalize_image_url(value):
    if value is None:
        return ''
    url = str(value).strip()
    if not url or url.lower() in ('none', 'null', 'nan'):
        return ''
    if not url.lower().startswith(('http://', 'https://')):
        return ''
    return url


def _safe_url(value):
    if value is None:
        return ''
    url = str(value).strip()
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https') or not parsed.netloc:
        return ''
    return url


def _clean_request_values(meal, combination, ingredients):
    clean_meal = meal if meal in ALLOWED_MEALS else 'breakfast'
    clean_combination = combination if combination in ALLOWED_COMBINATIONS else 'any'
    clean_ingredients = []

    for ingredient in ingredients:
        value = str(ingredient).strip().lower()
        if value in ALLOWED_INGREDIENTS and value not in clean_ingredients:
            clean_ingredients.append(value)

    return clean_meal, clean_combination, clean_ingredients


def _result_to_recipe(result, pantry_ingredient_count):
    names_list = result.name.lower().replace('recipe', '').split('|')
    names_list = [name.strip().capitalize() for name in names_list]
    try:
        ingredients_list = ast.literal_eval(result.ingredients)
    except (SyntaxError, ValueError):
        ingredients_list = []

    return {
        'id': result.id,
        'name': names_list,
        'url': _safe_url(result.url),
        'type': result.type.capitalize() if result.type else '',
        'ingredients': result.ingredients,
        'imageURL': _normalize_image_url(result.imageURL),
        'provider': result.provider,
        'givenIngredientsCount': pantry_ingredient_count,
        'ingredientsCount': len(ingredients_list),
    }


def _fetch_sorted_recipes(ingredient_string, combination, pantry_ingredients):
    rs = queryIngredientsFromDB(ingredient_string, combination)
    if rs is None:
        return None

    pantry_count = len(pantry_ingredients)
    recipes = [_result_to_recipe(result, pantry_count) for result in rs]

    recipes.sort(
        key=lambda r: (
            r['givenIngredientsCount'] / r['ingredientsCount']
            if r.get('ingredientsCount')
            else 0
        ),
        reverse=True,
    )
    return recipes


def _page_slice(recipes, page):
    start = (page - 1) * RECIPES_PAGE_SIZE
    end = start + RECIPES_PAGE_SIZE
    return recipes[start:end], start, end


def _store_search_session(meal, combination, ingredients):
    session['recipe_search_meta'] = {
        'meal': meal,
        'combination': combination,
        'ingredients': ingredients,
    }


@recipes_bp.route('', methods=['GET', 'POST'])
def recipes():
    if request.method == 'GET':
        return render_template(
            'error.html',
            title='Start from your pantry',
            message='Select ingredients on the pantry page to discover vegetarian recipes.',
        ), 400

    meal_type = request.form.get('meal', default='breakfast', type=str)
    combination = request.form.get('combination', default='all', type=str)
    meal_type, combination, ingredients = _clean_request_values(
        meal_type,
        combination,
        request.form.getlist('ingredient'),
    )

    if len(ingredients) == 0:
        return render_template(
            'error.html',
            title='No ingredients selected',
            message='Choose at least one item from your pantry, then try again.',
        ), 400

    ingredient_string = ';'.join(ingredients)

    all_recipes = _fetch_sorted_recipes(ingredient_string, combination, ingredients)
    if all_recipes is None:
        msg = 'No such Ingredients to fetch recipe(s)'
        if combination == 'all':
            msg = (
                'No recipes use every ingredient you selected. '
                'Try match mode “Any” or remove an item.'
            )
        return render_template('error.html', title='No recipes found', message=msg), 404

    _store_search_session(meal_type, combination, ingredients)
    page_recipes, _, _ = _page_slice(all_recipes, 1)
    total = len(all_recipes)

    return render_template(
        'recipes.html',
        recipes=page_recipes,
        total=total,
        page_size=RECIPES_PAGE_SIZE,
        has_more=total > RECIPES_PAGE_SIZE,
        next_page=2 if total > RECIPES_PAGE_SIZE else None,
    )


@recipes_bp.route('/more', methods=['GET'])
def recipes_more():
    search_meta = session.get('recipe_search_meta') or {}
    ingredients = search_meta.get('ingredients') or []
    meal_type, combination, ingredients = _clean_request_values(
        search_meta.get('meal', 'breakfast'),
        search_meta.get('combination', 'any'),
        ingredients,
    )

    if not ingredients:
        return jsonify({'error': 'Session expired. Search again from the pantry.'}), 410

    page = request.args.get('page', default=1, type=int)
    if page < 2:
        page = 1
    if page > MAX_RECIPES_PAGE:
        return jsonify({'error': 'Invalid page.'}), 400

    all_recipes = _fetch_sorted_recipes(';'.join(ingredients), combination, ingredients)
    if all_recipes is None:
        return jsonify({'error': 'No recipes found.'}), 404

    page_recipes, start, end = _page_slice(all_recipes, page)
    total = len(all_recipes)

    if start >= total:
        return jsonify({
            'html': '',
            'has_more': False,
            'next_page': None,
            'loaded': total,
            'total': total,
        })

    html = render_template('partials/recipe_cards.html', recipes=page_recipes)

    return jsonify({
        'html': html,
        'has_more': end < total,
        'next_page': page + 1 if end < total else None,
        'loaded': min(end, total),
        'total': total,
    })
