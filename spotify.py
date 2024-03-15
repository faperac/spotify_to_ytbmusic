import os
import json  # Ajout de l'importation du module json
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer les identifiants client à partir des variables d'environnement
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = 'http://localhost/3000'  # URL de redirection que vous avez spécifiée lors de la création de l'application Spotify

# Créer une instance de l'objet SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope="user-library-read"))

# Récupérer les chansons aimées de l'utilisateur
results = sp.current_user_saved_tracks()

# Créer une liste pour stocker les résultats
spotify_results = []

# Parcourir les résultats et stocker les informations sur chaque piste
for idx, item in enumerate(results['items']):
    track = item['track']
    spotify_results.append({
        "artist": track['artists'][0]['name'],
        "name": track['name']
    })

# Si vous avez plus de 20 chansons aimées, vous devrez parcourir les pages suivantes de résultats
while results['next']:
    results = sp.next(results)
    for idx, item in enumerate(results['items']):
        track = item['track']
        spotify_results.append({
            "artist": track['artists'][0]['name'],
            "name": track['name']
        })

# Enregistrer les résultats dans un fichier JSON
with open('spotify_results.json', 'w') as f:
    json.dump(spotify_results, f)
