from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'j6ubWTLbQQvgyvvSLTzwSdxk'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()
        #create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #tells Flask how we load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#If database isn't already created, creates it
def create_database(app):
    if not path.exists(f'flask_website/{DB_NAME}'):
        db.create_all(app=app)
        print('created database')
