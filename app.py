from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/rezept.html')
def rezept():
    return render_template('rezept.html')

@app.route('/main.html')
def main():
    return render_template('main.html')

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
