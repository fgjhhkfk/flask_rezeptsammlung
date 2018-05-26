from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rezepte.sqlite'
app.config['WHOOSH_BASE'] = 'whoosh'

db = SQLAlchemy(app)

class Rezepte(db.Model):
    __searchable__ = ['titel', 'zutaten', 'zubereitung']
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(64))
    link = db.Column(db.String(64))
    bild = db.Column(db.String(64))
    thumbnail = db.Column(db.String(64))
    zutaten = db.Column(db.String(64))
    zubereitung = db.Column(db.String(64))

wa.whoosh_index(app, Rezepte)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/rezept.html')
def rezept():
    return render_template('rezept.html')

@app.route('/main.html', methods=['GET','POST'])
def main():
    rezepte = Rezepte.query.all()
    return render_template('main.html', rezepte=rezepte)

@app.route('/search')
def search():
    rezepte = Rezepte.query.whoosh_search(request.args.get('query')).all()
    return render_template('main.html', rezepte=rezepte)

@app.route('/dolce.html')
def dolce():
    return render_template('dolce.html')

@app.route('/saucen.html')
def saucen():
    return render_template('saucen.html')

@app.route('/beilagen.html')
def beilagen():
    return render_template('beilagen.html')

if __name__ == '__main__':
    app.run(debug=True)
