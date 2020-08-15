import os
import time
from PIL import Image
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RezeptForm, BlogEntryForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foobar.sqlite'
app.config['SECRET_KEY'] = '1243124312431243'

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
    kategorie = db.Column(db.String(64))
    tags = db.Column(db.String(64))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/main', methods=['GET', 'POST'])
def main():
    rezepte = Rezepte.query.filter(Rezepte.kategorie == 'Main')
    return render_template('main.html', rezepte=rezepte)


@app.route('/dolce')
def dolce():
    rezepte = Rezepte.query.filter(Rezepte.kategorie == 'Dolce')
    return render_template('dolce.html', rezepte=rezepte)


@app.route('/saucen')
def saucen():
    rezepte = Rezepte.query.filter(Rezepte.kategorie == 'Saucen')
    return render_template('saucen.html', rezepte=rezepte)


@app.route('/beilagen')
def beilagen():
    rezepte = Rezepte.query.filter(Rezepte.kategorie == 'Beilagen')
    return render_template('beilagen.html', rezepte=rezepte)


@app.route('/search')
def search():
    rezepte = Rezepte.query.filter(Rezepte.zutaten.like
                                   ("%" + request.args.get('query') + "%")
                                   | Rezepte.titel.like
                                   ("%" + request.args.get('query') + "%")
                                   | Rezepte.tags.like
                                   ("%" + request.args.get('query') + "%")
                                   )
    return render_template('main.html', rezepte=rezepte)


@app.route('/rezept/<int:id>/')
def rezept(id):
    rezept = Rezepte.query.get_or_404(id)
    return render_template('rezept.html', rezept=rezept)


def save_picture(form_picture):
    picture_fn = form_picture.filename
    picture_path = os.path.join(app.root_path, 'static/bilder', picture_fn)
    thumbnail_path = os.path.join(app.root_path, 'static/bilder/thumbnails', picture_fn)

    output_size = (800, 600)
    output_size_thumbnail = (200, 150)

    img = Image.open(form_picture)
    thmbnl = img

    img.thumbnail(output_size)
    img.save(picture_path)

    thmbnl.thumbnail(output_size_thumbnail)
    thmbnl.save(thumbnail_path)

    return picture_fn


def save_picture_blog(form_picture):
    picture_fn = form_picture.filename
    picture_path = os.path.join(app.root_path, 'static/bilder/reiseblog', picture_fn)
    thumbnail_fn = 'thumb_'+picture_fn
    thumbnail_path = os.path.join(app.root_path, 'static/bilder/reiseblog', thumbnail_fn)

    output_size = (800, 600)
    output_size_thumbnail = (200, 150)

    img = Image.open(form_picture)
    thmbnl = img

    img.thumbnail(output_size)
    img.save(picture_path)

    thmbnl.thumbnail(output_size_thumbnail)
    thmbnl.save(thumbnail_path)

    return picture_fn, thumbnail_fn

@app.route('/rezept/<int:id>/update', methods=['GET', 'POST'])
def rezept_update(id):
    rezept = Rezepte.query.get_or_404(id)
    form = RezeptForm()
    if form.validate_on_submit():
        if form.bild.data:
            picture_file = save_picture(form.bild.data)
            rezept.bild = picture_file
            rezept.thumbnail = picture_file
        elif rezept.bild:
            rezept.bild = rezept.bild
        else:
            rezept.bild = "Piraten.png"
            rezept.thumbnail = "Piraten.png"

        rezept.titel = form.titel.data
        rezept.zutaten = form.zutaten.data
        rezept.zubereitung = form.zubereitung.data
        rezept.kategorie = form.kategorie.data
        rezept.tags = form.tags.data
        db.session.commit()
        flash('Das Rezept wurde erfolgreich geaendert!')
        return redirect(url_for('rezept', id=rezept.id))
    elif request.method == 'GET':
        form.titel.data = rezept.titel
        form.zutaten.data = rezept.zutaten
        form.zubereitung.data = rezept.zubereitung
        form.kategorie.data = rezept.kategorie
        form.tags.data = rezept.tags
    return render_template('neues_rezept.html', rezept=rezept, form=form)


@app.route('/rezept/neu', methods=['GET', 'POST'])
def neues_rezept():
    form = RezeptForm()
    if form.validate_on_submit():
        rezept = Rezepte(titel=form.titel.data,
                         zutaten=form.zutaten.data,
                         zubereitung=form.zubereitung.data,
                         kategorie=form.kategorie.data,
                         tags=form.tags.data,
                         )
        if form.bild.data:
            picture_file = save_picture(form.bild.data)
            rezept.bild = picture_file
            rezept.thumbnail = picture_file
        else:
            rezept.bild = "Piraten.png"
            rezept.thumbnail = "Piraten.png"

        db.session.add(rezept)
        db.session.commit()
        flash('Rezept erfolgreich erstellt!')
        return redirect('/')
    return render_template('neues_rezept.html', form=form)

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/new_blog_entry', methods=['GET', 'POST'])
def new_blog_entry():
    form = BlogEntryForm()

    # Die Klasse ab hier neu machen!!!
    if form.validate_on_submit():
        with open('/home/pi/temp_blog.html', 'w') as f:
            print(form.text.data)
            f.write("\n<p>\n")
            f.write("<strong>")
            f.write(form.titel.data)
            f.write("</strong>")
            f.write("\n</p>\n")
            f.write("\n<p>\n")
            f.write(form.text.data)
            f.write("\n</p>\n")
            if form.bild1.data:
                picture_file, thumbnail_file = save_picture_blog(form.bild1.data)
                print(picture_file)
                print(thumbnail_file)
                f.write("<a href='/static/bilder/reiseblog/"+picture_file+"'>\n")
                f.write("<img src='/static/bilder/reiseblog/"+thumbnail_file+"'>\n")
                f.write("</a>\n")
            if form.bild2.data:
                picture_file, thumbnail_file = save_picture_blog(form.bild2.data)
                print(picture_file)
                print(thumbnail_file)
                f.write("<a href='/static/bilder/reiseblog/"+picture_file+"'>\n")
                f.write("<img src='/static/bilder/reiseblog/"+thumbnail_file+"'>\n")
                f.write("</a>\n")
            if form.bild3.data:
                picture_file, thumbnail_file = save_picture_blog(form.bild3.data)
                print(picture_file)
                print(thumbnail_file)
                f.write("<a href='/static/bilder/reiseblog/"+picture_file+"'>\n")
                f.write("<img src='/static/bilder/reiseblog/"+thumbnail_file+"'>\n")
                f.write("</a>\n")
            if form.bild4.data:
                picture_file, thumbnail_file = save_picture_blog(form.bild4.data)
                print(picture_file)
                print(thumbnail_file)
                f.write("<a href='/static/bilder/reiseblog/"+picture_file+"'>\n")
                f.write("<img src='/static/bilder/reiseblog/"+thumbnail_file+"'>\n")
                f.write("</a>\n")
        return redirect('blog')

    return render_template('new_blog_entry.html', form=form)

@app.route('/web_server_setup')
def web_server_setup():
    return render_template('web_server_setup.html')

@app.route('/arch_installation')
def arch_installation():
    return render_template('arch_installation.html')


if __name__ == '__main__':
    app.run(debug=True)
