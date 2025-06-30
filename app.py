import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from api import ma, ItemResource, ItemListResource
from models import db, create_table
from views import (
    UserView, UserList, MainView, UserCreate, 
    ErrorView, UserEdit, UserDelete
)

migrate = Migrate()
api = Api()


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example_.db'
    app.config['SECRET_KEY'] = os.urandom(24)

    db.init_app(app)
    create_table(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    api.add_resource(ItemListResource, "/api/items")
    print("ItemListResource подключён")
    api.add_resource(ItemResource, "/api/items/<int:item_id>")
    print("Все зарегистрированные маршруты:")

    api.init_app(app)
    print("api.py загружен")

    # Регистрация маршрутов
    app.add_url_rule('/', view_func=MainView.as_view('main', engine=db))
    app.add_url_rule('/error', view_func=ErrorView.as_view('error', engine=db))
    app.add_url_rule('/users', view_func=UserList.as_view('user.list', engine=db))
    app.add_url_rule('/users/<string:user_id>/', view_func=UserView.as_view('user.view', engine=db))
    app.add_url_rule('/user/create/', view_func=UserCreate.as_view('user.create', engine=db))
    app.add_url_rule('/user/<string:user_id>/edit', view_func=UserEdit.as_view('user.edit', engine=db))
    app.add_url_rule('/user/<string:user_id>/delete', view_func=UserDelete.as_view('user.delete', engine=db))

    print("Все маршруты после фикса:")
    for rule in app.url_map.iter_rules():
        print(rule)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
