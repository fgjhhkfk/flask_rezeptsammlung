from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class RezeptForm(FlaskForm):
    titel = StringField('Titel', validators=[DataRequired()])
    zutaten = TextAreaField('Zutaten', validators=[DataRequired()])
    zubereitung = TextAreaField('Zubereitung', validators=[DataRequired()])
    # kategorie = StringField('Kategorie', validators=[DataRequired()])
    kategorie = SelectField(u'Kategorie', choices=[('Main', 'Main'), ('Dolce', 'Dolce'), ('Saucen', 'Saucen'), ('Beilagen', 'Beilagen')])
    tags = StringField('Tags')
    bild = FileField('Bild', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Hochladen')
