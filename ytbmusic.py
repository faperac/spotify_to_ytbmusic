import ytmusicapi
import json

# Lire les en-têtes à partir du fichier browser_headers.txt
with open('browser_headers.txt', 'r') as f:
    headers_raw = f.read()

# Configurer l'authentification avec les en-têtes copiés
ytmusicapi.setup(filepath="oauth.json", headers_raw=headers_raw)

# Créer une instance de l'API YouTube Music avec l'authentification configurée
ytmusic = ytmusicapi.YTMusic("oauth.json")

# Charger les résultats de Spotify depuis le fichier JSON
with open('spotify_results.json', 'r') as f:
    spotify_results = json.load(f)

# Créer une playlist sur YouTube Music
playlist_name = "Ma Playlist Spotify"
playlist_description = "Playlist basée sur mes chansons aimées sur Spotify"
playlist_id = ytmusic.create_playlist(playlist_name, playlist_description)

not_found_songs = []

# for track in spotify_results:
#     # Rechercher la chanson sur YouTube Music
#     search_results = ytmusic.search(f"{track['artist']} {track['name']}")
#     if search_results:
#         # Filtrer les résultats pour ne récupérer que les chansons
#         songs = [result for result in search_results if result['resultType'] == 'song']
#         if songs:
#             # Ajouter la première chanson trouvée à la playlist
#             ytmusic.add_playlist_items(playlist_id, [songs[0]['videoId']])
#             print(f"La chanson {songs[0]['title']} a été ajoutée à la playlist.")
#         else:
#             print(f"Aucune chanson trouvée pour {track['name']} de {track['artist']}.")
#             not_found_songs.append(f"{track['name']} de {track['artist']}")
#     else:
#         print(f"Impossible de trouver la chanson {track['name']} de {track['artist']} sur YouTube Music.")
#         not_found_songs.append(f"{track['name']} de {track['artist']}")

for track in spotify_results:
    # Search for the song on YouTube Music
    search_results = ytmusic.search(f"{track['artist']} {track['name']}")
    if search_results:
        try:
            # Add the first found song to the playlist
            ytmusic.add_playlist_items(playlist_id, [search_results[0]['videoId']])
            print(f"The song {track['name']} by {track['artist']} has been added to the playlist.")
        except Exception as e:
            print(f"Error adding the song {track['name']} by {track['artist']}: {e}")
            not_found_songs.append(f"{track['name']} de {track['artist']}")
    else:
        print(f"Unable to find the song {track['name']} by {track['artist']} on YouTube Music.")
        not_found_songs.append(f"{track['name']} de {track['artist']}")

# Enregistrer les chansons non trouvées dans un fichier texte
with open("songs_not_found.txt", "w") as file:
    for song in not_found_songs:
        file.write(song + "\n")


