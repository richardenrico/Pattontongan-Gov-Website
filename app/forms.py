from unicodedata import category
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired("Username diperlukan")])
    name = StringField("Name", validators=[DataRequired("Nama diperlukan")])
    password = PasswordField("Password", validators=[DataRequired("Password diperlukan")])

class NewsForm(FlaskForm):
    title = StringField('Judul', validators=[DataRequired("Judul diperlukan")])
    cover = StringField('Sampul')
    content = CKEditorField('Content', validators=[DataRequired("Konten berita diperlukan")])
    category = HiddenField("Kategory", default="berita")

class AnnouncementForm(FlaskForm):
    title = StringField('Judul', validators=[DataRequired("Judul diperlukan")])
    cover = StringField('Sampul')
    content = CKEditorField('Content', validators=[DataRequired("Konten berita diperlukan")])
    category = HiddenField("Kategory", default="pengumuman")

class TourismForm(FlaskForm):
    title = StringField('Judul', validators=[DataRequired("Judul diperlukan")])
    cover = StringField('Sampul')
    content = CKEditorField('Content', validators=[DataRequired("Konten berita diperlukan")])
    category = HiddenField("Kategory", default="wisata")
