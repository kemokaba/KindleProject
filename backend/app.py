from operator import or_
import requests, jsonify, request
from flask import *
import re
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cors = CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:passer1234@localhost/books'
app.app_context().push()
db = SQLAlchemy(app)


# Models
class Livre(db.Model):
    __tablename__='livres'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(),nullable=False)
    contenu = db.Column(db.Text,  nullable=False)
    auteur = db.Column(db.String())
    date_pub = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Livre {self.id}>'

#db.create_all()

aj_livres = [
                Livre(id= 1513, titre="Romeo and Juliet", contenu="https://www.gutenberg.org/files/1513/1513-0.txt",auteur="William Shakespeare"),
                Livre(id=1514, titre="A Midsummer Night's Dream", contenu="https://www.gutenberg.org/files/1514/1514-0.txt",auteur="William Shakespeare"),
                Livre(id=1515, titre="The Merchant of Venice", contenu="https://www.gutenberg.org/files/1515/1515-0.txt",auteur="William Shakespeare"),
                Livre(id=1516, titre="King Henry IV, the First Part", contenu="https://www.gutenberg.org/files/1516/1516-0.txt",auteur="William Shakespeare"),
                Livre(id=1517, titre="The Merry Wives of Windsor", contenu="https://www.gutenberg.org/files/1517/1517-0.txt",auteur="William Shakespeare"),
                Livre(id=1617, titre="The Wind in the Rose-Bush, and Other Stories of the Supernatura", contenu="https://www.gutenberg.org/files/1617/1617-0.txt",auteur="Freeman, Mary Eleanor Wilkins"),
                Livre(id=1618, titre="In the Shadow of the Glen", contenu="https://www.gutenberg.org/files/1618/1618-0.txt",auteur="Synge, J. M. (John Millington)"),
                Livre(id=1619, titre="La Celestina", contenu="https://www.gutenberg.org/files/1619/1619-0.txt",auteur="Rojas, Fernando de"),
                Livre(id=1620, titre="The Lion and the Unicorn", contenu="https://www.gutenberg.org/files/1620/1620-0.txt",auteur="Davis, Richard Harding"),
                Livre(id=1621, titre="Miss or Mrs.?", contenu="https://www.gutenberg.org/files/1621/1621-0.txt",auteur="Collins, Wilkie"),

            ]
#db.session.bulk_save_objects(aj_livres)

books1 = []
for i in range(100, 110):
    response = requests.get(f'http://gutendex.com/books/?page={i}')
    if response.status_code == 200:
        books1 += response.json()['results']

for book in books1:
    book_id = book['id']
    book_titre = book['title']
    book_auteur = book['authors'][0]['name'] if book['authors'] else 'Unknown'
    book_contenu = "https://www.gutenberg.org/files/"+str(book_id)+"/"+str(book_id)+"-0.txt"
    # Ajout des données à la table d'index
    index_entry = Livre(id=book_id,titre=book_titre, auteur=book_auteur,contenu=book_contenu)
    #db.session.add(index_entry)
db.session.commit()


@app.route('/',methods=['GET'])
@cross_origin()

def index():
    books = []
    #if 'book' in request.args:
        #mot_rechercher = request.args.get('book')
        #reponse = requests.get("https://gutendex.com/books/?search=" + mot_rechercher)
        #data = json.loads(reponse.content)
        #books = data['results']
    #return render_template('acceuil.html', books=books)

    # Récupération de la recherche de l'utilisateur
    book = request.args.get('book')
    # Recherche des livres par mot clé
    results = []
    books1 = Livre.query.filter(
        or_(Livre.titre.ilike(f'%{book}%'), Livre.auteur.ilike(f'%{book}%'))).all()
    for b1 in books1:
        results.append({'auteur': b1.auteur, 'contenu':b1.contenu, 'titre': b1.titre, 'id': b1.id})
    #print(results)
    return jsonify(results)
@app.route('/book/searchRegex',methods=['GET'])
def searchRegex():

    regex = request.args.get('regex', '')
    regex_results = []
    if re.match(regex, str(regex)):
            books2 = Livre.query.all()
            for b2 in books2:
                if re.search(regex, b2.contenu) or (regex, b2.titre) or (regex, b2.auteur)or (regex, b2.id):
                    regex_results.append({'auteur': b2.auteur,
                                          'contenu':b2.contenu,
                                          'titre': b2.titre,
                                          'id': b2.id})
    #print(regex_results)
    return jsonify(regex_results)


# Recherche avec Jaccard



if __name__ == '__main__':
    app.run()
