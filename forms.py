from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class BaseUserForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=3, max=50)])
    description = StringField('О себе', validators=[Length(max=200)])

    def validate_name(self, field):
        if "админ" in field.data.lower():
            raise ValidationError('"админ" не может быть использовано в качестве имени')


class UserCreateForm(BaseUserForm):
    submit = SubmitField('Создать')


class UserEditForm(BaseUserForm):
    submit = SubmitField('Изменить')


class UserDeleteForm(FlaskForm):
    submit = SubmitField('Удалить')

