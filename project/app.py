from flask import Flask, Blueprint, render_template
from os import environ

from config.config import app_config

# Blueprints
from routes.home import home_bp
from routes.ingredients import ingredients_bp
from routes.recipes import recipes_bp
from routes.management import management_bp

blueprints = (home_bp, ingredients_bp, recipes_bp, management_bp)

def create_app():
    app = Flask(__name__)

    get_config(app)

    register_blueprint(app, blueprints)

    return app
# end create_app

def get_config(app):
    config_name = environ.get('FLASK_ENV')
    app.config.from_object(app_config[config_name])
    #app.config.from_pyfile('config.py')
    
# end get_config

def register_blueprint(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    # Configure explicit url routes to home blueprint
    app.add_url_rule('/', endpoint='index')
    app.add_url_rule('/home', endpoint='home')
    
# end register_blueprint

if __name__ == '__main__':
    app = create_app()
    app.run()
# end main()