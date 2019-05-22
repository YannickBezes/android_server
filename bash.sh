#! /bin/bash
# Add users
curl -H "Content-Type: application/json" --request POST -d '{"city": "montpellier","email": "florian.chevalier@etu.umontpellier.fr","firstname": "Florian","gender": "Homme","height": 180,"lastname": "Chevalier","lat": "43.633153","lng": "3.863715","username": "flo","weight": 60,"password": "flo"}' http://bsy.ovh:5000/user
curl -H "Content-Type: application/json" --request POST -d '{"city": "montpellier","email": "yannick.bezes@etu.umontpellier.fr","firstname": "yannick","gender": "Homme","height": 173,"lastname": "Bezes","lat": "43.633153","lng": "3.863715","username": "yannick","weight": 53,"password": "yannick"}' http://bsy.ovh:5000/user

# Add a public network


# Add a private network


# With the user yannick ask a request for a private network

# Add post


# Add categories


# Add shops
