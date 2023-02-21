import requests
from flask import *

app = Flask('mars_discovery')


@app.route('/')
def index():
    books = []
    if 'book' in request.args:
        mot_rechercher = request.args.get('book')
        reponse = requests.get("https://gutendex.com/books/?search=" + mot_rechercher)
        data = json.loads(reponse.content)
        books = data['results']
    return render_template('acceuil.html', books=books)


@app.route('/home')
def home():
    return render_template('acceuil.html')


app.run(debug=True)
