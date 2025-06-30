from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для моделей SQLAlchemy"""
    pass


db = SQLAlchemy(model_class=Base)

class Item(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    description: Mapped[str] = mapped_column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Item(name={self.name})>"


class User(db.Model):
    """Модель пользователя"""
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50), nullable=False)
    description: Mapped[str] = mapped_column(db.String(200), default="")

    def __repr__(self):
        return f'<Пользователь {self.name}>'


def create_table(app: Flask):
    with app.app_context():
        db.create_all()

