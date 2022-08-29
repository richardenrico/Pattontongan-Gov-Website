from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired("Username diperlukan")])
    name = StringField("Name", validators=[DataRequired("Nama diperlukan")])
    password = PasswordField("Password", validators=[DataRequired("Password diperlukan")])