import os 

SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-only-set-SECRET_KEY-in-production'
#SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
#SQLALCHEMY_TRACK_MODIFICATIONS = False
