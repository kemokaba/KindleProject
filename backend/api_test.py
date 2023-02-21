import json
import requests

mots_cherche = 'one'
reponse = requests.get("https://gutendex.com/books/?search=" + mots_cherche)
data = json.loads(reponse.content)
print(data)

