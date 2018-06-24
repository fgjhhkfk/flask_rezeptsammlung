from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class RezeptForm(FlaskForm):
    titel = StringField('Titel', validators=[DataRequired()])
    zutaten = TextAreaField('Zutaten', validators=[DataRequired()])
    zubereitung = TextAreaField('Zubereitung', validators=[DataRequired()])
    kategorie = StringField('Kategorie', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    bild = FileField('Bild', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Hochladen')
