import requests
import json
import time

base_url = "localhost"

SUCCESS = '\033[92m'
BOLD = '\033[1m'
FAIL = '\033[91m'
ENDC = '\033[0m'

# Add users
res = requests.post(url="http://{}:5000/user".format(base_url), json={"city": "Montpellier", "email": "florian.chevalier@etu.umontpellier.fr", "firstname": "Florian", "gender": "male", "height": 180, "lastname": "Chevalier", "lat": 43.633153, "lng": 3.863715, "username": "Flo", "weight": 60, "password": "flo", "interest": "sport"})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add user " + BOLD + "Flo" + ENDC
print(msg)
token_flo = res.json()['token']

res = requests.post(url="http://{}:5000/user".format(base_url), json={"city": "Montpellier", "email": "yannick.bezes@etu.umontpellier.fr", "firstname": "Yannick", "gender": "male", "height": 173, "lastname": "Bezes", "lat": 43.633153, "lng": 3.863715, "username": "Yannick", "weight": 53, "password": "yannick", "interest": "programmation,sport"})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add user " + BOLD + "Yannick" + ENDC
print(msg)
token_yannick = res.json()['token']

res = requests.post(url="http://{}:5000/user".format(base_url), json={"city": "Agde", "email": "jean.paul@gmail.com", "firstname": "Jean", "gender": "male", "height": 181, "lastname": "Paul", "lat": 43.308744, "lng": 3.476735, "username": "Jean", "weight": 80, "password": "jean", "interest": "mode,marche"})
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
msg += "Add category" + BOLD + "Sport" + ENDC
print(msg)

res = requests.post(url="http://{}:5000/category".format(base_url), json={"name": "Mode"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add category" + BOLD + "Mode" + ENDC
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