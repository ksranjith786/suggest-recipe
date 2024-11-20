# Suggest Recipe
This is a Recipe Suggester for the available ingredients available in User's Kitchen that can be provided as inputs. Where the application does processes the given ingredients and find the best suitable recipe(s) available. The Output window does show the no.of Ingredients that are matched from your input with the Recipe's. A View Recipe button is provided for further detail view.
I have built its backend using Python, Flask, BeautifulSoup and HTML.
It is deployed on Heroku cloud platform.

## LIVE on

https://suggest-recipe.onrender.com

Please click [here](https://suggest-recipe.onrender.com) to view the LIVE app.

## Credit To
The idea was proposed by Madhuri and Suresh.

## Source checkout
```
git clone https://github.com/ksranjith786/suggest-recipe.git
cd suggest-recipe
```
### Creates a virtual env
```
python -m venv venv
```
Note: _If virtual environment **venv** not available then install it using **python -m pip install virtualenv**_

### Switch/Activate to venv
```
source venv/Scripts/activate
```

### Install the Python modules
```
pip install -r requirements.txt
```

## Execution Steps
```
export FLASK_ENV=development
export DATABASE_URL=sqlite:///database.db
python project/app.py
```
You can now view on http://127.0.0.1:5000/

## Initial Steps
The below are the steps I have done when I initially started creating this project.
```
python -m venv venv
source venv/Scripts/activate

python -m pip install flask
python -m pip install beautifulsoup4
python -m pip install requests
python -m pip install gunicorn
python -m pip install psycopg2
python -m pip freeze > requirements.txt
```
