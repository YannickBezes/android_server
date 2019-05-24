import requests
import json
import time

base_url = "localhost"

SUCCESS = '\033[92m'
BOLD = '\033[1m'
FAIL = '\033[91m'
ENDC = '\033[0m'

# Add users
res = requests.post(url="http://{}:5000/user".format(base_url), json={"city": "Montpellier", "email": "florian.chevalier@etu.umontpellier.fr", "firstname": "Florian", "gender": "Homme", "height": 180, "lastname": "Chevalier", "lat": 43.633153, "lng": 3.863715, "username": "Flo", "weight": 60, "password": "flo", "interest": "sport,informatique"})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add user " + BOLD + "Flo" + ENDC
print(msg)
token_flo = res.json()['token']

res = requests.post(url="http://{}:5000/user".format(base_url), json={"city": "Montpellier", "email": "yannick.bezes@etu.umontpellier.fr", "firstname": "Yannick", "gender": "Homme", "height": 173, "lastname": "Bezes", "lat": 43.633153, "lng": 3.863715, "username": "Yannick", "weight": 53, "password": "yannick", "interest": "programmation,sport,musique"})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add user " + BOLD + "Yannick" + ENDC
print(msg)
token_yannick = res.json()['token']

res = requests.post(url="http://{}:5000/user".format(base_url), json={"city": "Agde", "email": "jean.paul@gmail.com", "firstname": "Jean", "gender": "Homme", "height": 181, "lastname": "Paul", "lat": 43.308744, "lng": 3.476735, "username": "Jean", "weight": 80, "password": "jean", "interest": "mode,marche,cinema"})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add user " + BOLD + "Jean" + ENDC
print(msg)
token_jean = res.json()['token']



# Add networks
res = requests.post(url="http://{}:5000/network".format(base_url), json={"name": "amis", "public": False}, headers={"x-access-token": token_flo})
msg = SUCCESS  if res.json()['success'] else FAIL
msg += "Add network " + BOLD + "amis" + ENDC
print(msg)

res = requests.post(url="http://{}:5000/network".format(base_url), json={"name": "Montpellier network", "public": True}, headers={"x-access-token": token_yannick})
msg = SUCCESS if res.json()['success'] else FAIL
msg +="Add network " + BOLD + "Montpellier network" + ENDC
print(msg)



# Ask a sub request from Yannick to the group 'amis'
res = requests.put(url="http://{}:5000/network/amis/request".format(base_url), headers={"x-access-token": token_yannick})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Request amis for Yannick" + ENDC
print(msg)



# Add all user to the group Montpellier network
res = requests.put(url="http://{}:5000/network/Montpellier network/Jean".format(base_url), headers={"x-access-token": token_jean})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Subscribe " + BOLD + "Jean to Montpellier network" + ENDC
print(msg)

res = requests.put(url="http://{}:5000/network/Montpellier network/Flo".format(base_url), headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Subscribe " + BOLD + "Flo to Montpellier network" + ENDC
print(msg)



# Add posts
res = requests.post(url="http://{}:5000/network/amis".format(base_url), json={"content": "Bonjour et bienvenue"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Post message " + BOLD + "Flo to amis" + ENDC
print(msg)

res = requests.post(url="http://{}:5000/network/Montpellier network".format(base_url), json={"content": "Bonjour et bienvenue"}, headers={"x-access-token": token_yannick})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Post message " + BOLD + "Yannick to Montpellier network" + ENDC
print(msg)

res = requests.post(url="http://{}:5000/network/Montpellier network".format(base_url), json={"content": "Bonjour, je suis nouveau"}, headers={"x-access-token": token_jean})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Post message " + BOLD + "Jean to Montpellier network" + ENDC
print(msg)



# Add categories
res = requests.post(url="http://{}:5000/category".format(base_url), json={"name": "Sport"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add category " + BOLD + "Sport" + ENDC
print(msg)

res = requests.post(url="http://{}:5000/category".format(base_url), json={"name": "Mode"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add category " + BOLD + "Mode" + ENDC
print(msg)



# Add shops
res = requests.post(url="http://{}:5000/shop".format(base_url), json={"name": "Decathlon Odysseum", "lat": 43.605403, "lng": 3.923821, "city": "Montpellier", "category": "Sport", "address": "1072 Rue Georges Melies, 34000 Montpellier", "keywords": "marche,sport"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add shop " + BOLD + "Decathlon Odysseum" + ENDC
print(msg)

res = requests.post(url="http://{}:5000/shop".format(base_url), json={"name": "Chauss34", "lat": 43.650982, "lng": 3.846524, "city": "Saint-Clement-de-Riviere", "category": "Mode", "address": "6 Rue des Genets, 34980 Saint-Clement-de-Riviere", "keywords": "mode,chausure"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add shop " + BOLD + "Chauss34" + ENDC
print(msg)

res = requests.post(url="http://{}:5000/shop".format(base_url), json={"name": "Decathlon Saint Jean De Vedas", "lat": 43.571359, "lng": 3.845273, "city": "Saint-Jean-de-Vedas", "category": "Sport", "address": "Zac Deves De La Condamine, 34430 Saint-Jean-de-Vedas", "keywords": "sport,tennis"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add shop " + BOLD + "Decathlon Saint Jean De Vedas" + ENDC
print(msg)

res = requests.post(url="http://{}:5000/shop".format(base_url), json={"name": "LDLC Montpellier Lattes", "lat": 43.583160, "lng": 3.923690, "city": "Lattes", "category": "Informatique", "address": "le Centre Commercial Le Solis La, Avenue Georges Freche, 34970 Lattes", "keywords": "informatique"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add shop " + BOLD + "LDLC Montpellier Lattes" + ENDC
print(msg)


# Add favorite shop
res = requests.put(url="http://{}:5000/user/shop/Decathlon Odysseum".format(base_url), headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add favorite shop " + BOLD + "Decathlon Odysseum to Flo" + ENDC
print(msg)

res = requests.put(url="http://{}:5000/user/shop/Decathlon Saint Jean De Vedas".format(base_url), headers={"x-access-token": token_yannick})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add favorite shop " + BOLD + "Decathlon Saint Jean De Vedas to Yannick" + ENDC
print(msg)


res = requests.put(url="http://{}:5000/user/shop/Chauss34".format(base_url), headers={"x-access-token": token_jean})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add favorite shop " + BOLD + "Chauss34 to Jean" + ENDC
print(msg)


# Create pubs
res = requests.post(url="http://{}:5000/pub".format(base_url), json={"name": "musique_1", "image": "http://montpellier.aujourdhui.fr/uploads/assets/evenements/recto_flyer/2019/06/2023572_fete-musique-ecole-municipale-de-musique-juvignac.jpg?fbclid=IwAR01eAzXNVUqI5rE0WFx_WwuXLclvz3zcXx2w9ESM09s-KOeaV0C4n1egTE", "keywords": "musique"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add pub " + BOLD + "musique_1" + ENDC
print(msg)

res = requests.post(url="http://{}:5000/pub".format(base_url), json={"name": "musique_cinema_2", "image": "http://montpellier.megarama.fr/public/contenu/images/2019-05-28-avp-rocketman.jpg?fbclid=IwAR3mLADoJc2Ry0PxiFNHKkrZ8uyIgWI6HSXHk9uALJ_u2NT1-_GLR5iWkl8", "keywords": "musique,cinema"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add pub " + BOLD + "musique_cinema_2" + ENDC
print(msg)

res = requests.post(url="http://{}:5000/pub".format(base_url), json={"name": "musique_sport_3", "image": "https://www.ffgym.fr/media/1557308963-content_details-1557308957-Affiche%20Dany%20Cup-min.jpg?fbclid=IwAR3BSf45dQmpXTvqC527hxfNlxj3s0ViTk6DCQVt6G_mFjl1yuzhJJWusME", "keywords": "musique,sport"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add pub " + BOLD + "musique_sport_3" + ENDC
print(msg)

res = requests.post(url="http://{}:5000/pub".format(base_url), json={"name": "sport_1", "image": "https://www.montpellier3m.fr/sites/default/files/fwwc2019_hcp_montpellier_no_logos_fr.jpg?fbclid=IwAR2pVhOPxoLAo2ILHjxuCDun7Tzq8k9IfkyVzPG34PRHWKzKQpLEWFSIAw8", "keywords": "sport"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add pub " + BOLD + "sport_1" + ENDC
print(msg)