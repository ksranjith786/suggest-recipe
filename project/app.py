from flask import Flask, Blueprint, render_template
from os import environ

# Blueprints
from routes.home import home_bp
from routes.ingredients import ingredients_bp
from routes.recipes import recipes_bp
from routes.management import management_bp
from routes.fetch import fetch_bp
from routes.seed import seed_bp

from database.database import createRecipeDB

blueprints = (home_bp, ingredients_bp, recipes_bp, management_bp, fetch_bp, seed_bp)

def create_app():
    app = Flask(__name__)

    get_config(app)
    harden_app(app)

    create_db()

    register_blueprint(app, blueprints)

    return app
# end create_app

def get_config(app):
    app.config.from_pyfile('config.py', silent=True)

    envFLASK = environ.get('FLASK_ENV')
    if envFLASK == 'development':
        app.debug = True
    else:
        app.debug = False

    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=envFLASK != 'development',
    )
# end get_config

def harden_app(app):
    @app.after_request
    def add_security_headers(response):
        response.headers.setdefault('X-Content-Type-Options', 'nosniff')
        response.headers.setdefault('X-Frame-Options', 'DENY')
        response.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
        response.headers.setdefault('Permissions-Policy', 'geolocation=(), microphone=(), camera=()')
        response.headers.setdefault(
            'Content-Security-Policy',
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' https://fonts.googleapis.com 'unsafe-inline'; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' https: data:; "
            "connect-src 'self'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none';"
        )
        return response
# end harden_app

def create_db():
    databaseURL = environ.get('DATABASE_URL')
    createRecipeDB(databaseURL)
# end create_db

def register_blueprint(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    # Configure explicit url routes to home blueprint
    app.add_url_rule('/', endpoint='index')
    app.add_url_rule('/home', endpoint='home')
    
# end register_blueprint
app = create_app()

if __name__ == '__main__':
    app.run()
# end main()
