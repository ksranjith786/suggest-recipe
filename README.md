# Suggest Recipe
This is a Recipe Suggester for the available ingredients with an User which can be provided from a Form. I have used Recommendation Engine on Machine Learning. Which processes the given ingredients and find the best suitable recipe can be prepared.
I have built its backend using Python, Flask and REST API.
It is deployed on Heroku cloud platform.

## LIVE on

https://suggest-recipe.herokuapp.com

Please click [here](https://suggest-recipe.herokuapp.com) to view the LIVE app.

## Credit To
The idea was proposed by Madhuri and Suresh.

## Source checkout
```
git clone https://github.com/ksranjith786/suggest-recipe.git
cd suggest-recipe
```

## Recipe Websites
* Hebbar's Kitchen

## Compilation Steps

### Creates a virtual env
```
python -m venv venv
```
Note: _If virutal environment **venv** not available then install it using **python -m pip venv**_

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
export FLASK_APP=project
export FLASK_ENV=development
flask run
```

## Initial Steps
```
python -m venv venv
source venv/Scripts/activate
python -m pip install flask
python -m pip install beautifulsoup4
python -m pip install requests
python -m pip install gunicorn
python -m pip freeze > requirements.txt
```