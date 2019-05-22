import requests
import json
import time

base_url = "localhost"

SUCCESS = '\033[92m'
BOLD = '\033[1m'
FAIL = '\033[91m'
ENDC = '\033[0m'

# Add users
res = requests.post(url="http://{}:5000/user".format(base_url), json={"city": "Montpellier", "email": "florian.chevalier@etu.umontpellier.fr", "firstname": "Florian", "gender": "male", "height": 180, "lastname": "Chevalier", "lat": 43.633153, "lng": 3.863715, "username": "flo", "weight": 60, "password": "flo"})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add user " + BOLD + "flo" + ENDC
print(msg)
token_flo = res.json()['token']

res = requests.post(url="http://{}:5000/user".format(base_url), json={"city": "Montpellier", "email": "yannick.bezes@etu.umontpellier.fr", "firstname": "Yannick", "gender": "male", "height": 173, "lastname": "Bezes", "lat": 43.633153, "lng": 3.863715, "username": "yannick", "weight": 53, "password": "yannick"})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add user yannick" + ENDC
print(msg)
token_yannick = res.json()['token']

res = requests.post(url="http://{}:5000/user".format(base_url), json={"city": "Agde", "email": "jean.paul@gmail.com", "firstname": "Jean", "gender": "male", "height": 181, "lastname": "Paul", "lat": 43.308744, "lng": 3.476735, "username": "jean", "weight": 80, "password": "jean"})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add user jean" + ENDC
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



# Ask a sub request from yannick to the group 'amis'
res = requests.put(url="http://{}:5000/network/amis/request".format(base_url), headers={"x-access-token": token_yannick})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Request amis for yannick" + ENDC
print(msg)



# Add all user to the group Montpellier network
res = requests.put(url="http://{}:5000/network/Montpellier network/jean".format(base_url), headers={"x-access-token": token_jean})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Subscribe " + BOLD + "jean to Montpellier network" + ENDC
print(msg)

res = requests.put(url="http://{}:5000/network/Montpellier network/flo".format(base_url), headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Subscribe " + BOLD + "flo to Montpellier network" + ENDC
print(msg)



# Add posts
res = requests.post(url="http://{}:5000/network/amis".format(base_url), json={"content": "Bonjour et bienvenue"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Post message " + BOLD + "flo to amis" + ENDC
print(msg)

res = requests.post(url="http://{}:5000/network/Montpellier network".format(base_url), json={"content": "Bonjour et bienvenue"}, headers={"x-access-token": token_yannick})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Post message " + BOLD + "yannick to Montpellier network" + ENDC
print(msg)

res = requests.post(url="http://{}:5000/network/Montpellier network".format(base_url), json={"content": "Bonjour, je suis nouveau"}, headers={"x-access-token": token_jean})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Post message " + BOLD + "jean to Montpellier network" + ENDC
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
res = requests.post(url="http://{}:5000/shop".format(base_url), json={"name": "Decathlon Odysseum", "lat": 43.605403, "lng": 3.923821, "city": "Montpellier", "category": "Sport"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add shop " + BOLD + "Decathlon Odysseum" + ENDC
print(msg)

res = requests.post(url="http://{}:5000/shop".format(base_url), json={"name": "Chauss34", "lat": 43.650982, "lng": 3.846524, "city": " Saint-Clement-de-Riviere", "category": "Mode"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add shop " + BOLD + "Chauss34" + ENDC
print(msg)

res = requests.post(url="http://{}:5000/shop".format(base_url), json={"name": "Decathlon Saint Jean De Vedas", "lat": 43.571359, "lng": 3.845273, "city": "Saint-Jean-de-Vedas", "category": "Sport"}, headers={"x-access-token": token_flo})
msg = SUCCESS if res.json()['success'] else FAIL
msg += "Add shop " + BOLD + "Decathlon Saint Jean De Vedas" + ENDC
print(msg)