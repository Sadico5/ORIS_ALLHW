from typing import Union, Any

from flask import (
    request, url_for,
    render_template, redirect,
    flash
)
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from werkzeug import Response

from forms import UserCreateForm, UserEditForm, UserDeleteForm
from models import User


class BaseView(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine


class MainView(BaseView):
    """Главная страница"""

    def get(self):
        return render_template('main.html')


class ErrorView(BaseView):
    """Страница ошибки"""

    def get(self):
        return render_template('error.html')


class UserList(BaseView):
    """Список пользователей"""

    def get(self):
        users: list[User] = self.engine.session.execute(User.query).scalars()
        return render_template('user/list.html', users=users)


class UserCreate(BaseView):
    """Создание пользователя"""

    def get(self):
        form = UserCreateForm()
        return render_template('user/create.html', form=form)

    def post(self):
        form = UserCreateForm(request.form)
        if form.validate():
            user = User(
                name=form.name.data,
                description=form.description.data
            )
            self.engine.session.add(user)
            self.engine.session.commit()
            flash("Успешно!", category='success')
            return redirect(url_for('user.list'))

        flash("Произошла ошибка при создании", category='error')
        return redirect(url_for('error'))


class BaseUserView(BaseView):

    def get_user(self, user_id: str) -> Union[Response, Any]:
        user = self.engine.session.execute(User.query.where(User.id == user_id)).scalar()
        if not user:
            flash("Пользователь не найден.", category='error')
            return redirect(url_for('error'))
        return user


class UserView(BaseUserView):
    """Просмотр пользователя"""

    def get(self, user_id: str):
        user = self.get_user(user_id)
        return render_template('user/view.html', user=user)


class UserEdit(BaseUserView):
    """Редактирование пользователя"""

    def get(self, user_id: str):
        user = self.get_user(user_id)
        form = UserEditForm(obj=user)
        return render_template('user/edit.html', user=user, form=form)

    def post(self, user_id: str):
        user = self.get_user(user_id)
        form = UserEditForm(request.form)
        if form.validate():
            user.name = form.name.data
            user.description = form.description.data
            self.engine.session.commit()
            flash("Данные обновлены!", category='success')
        else:
            flash("Ошибка валидации!", category='error')

        return redirect(url_for('user.list'))


class UserDelete(BaseUserView):
    """Удаление пользователя"""

    def get(self, user_id: str):
        user = self.get_user(user_id)
        form = UserDeleteForm(obj=user)
        return render_template('user/delete.html', user=user, form=form)

    def post(self, user_id: str):
        user = self.get_user(user_id)
        form = UserDeleteForm(obj=user)
        if form.validate():
            self.engine.session.delete(user)
            self.engine.session.commit()
            flash("Пользователь удалён!", category='success')

        return redirect(url_for('user.list'))
