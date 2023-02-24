import requests, jsonify, request
from flask import *
import re

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:passer1234@localhost/books'
app.app_context().push()
db = SQLAlchemy(app)

# Models
class Livre(db.Model):
    __tablename__='livres'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(80), unique=True, nullable=False)
    contenu = db.Column(db.Text, unique=True, nullable=False)
    auteur = db.Column(db.String(), unique=True)
    date_pub = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Livre {self.contenu}>'
#db.create_all()

db.session.commit()

@app.route('/',methods=['GET'])
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





if __name__ == '__main__':
    app.run()
