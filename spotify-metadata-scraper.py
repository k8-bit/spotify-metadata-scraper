# Import libraries
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Credentials from Spotify for developers
cid = 'your client id here'
secret = 'your client secret here'

# Authentication
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Create dataframe
artist_data = []

# Define artist ID from Spotify profile; this URI is for The Nocturnal Broadcast
artist_uri = 'spotify:artist:6t0WjFRLm8nYasSkwNQQtV'

# Create list of albums
results = sp.artist_albums(artist_uri, album_type='album')
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

# Store unique album names and IDs
names = []
album_ids = []
for album in albums:
    name = album['name'].lower()
    if name not in names:
        names.append(name)
        album_ids.append(album['id'])

# Retrieve track-specific details
for album_id in album_ids:
    results = sp.album_tracks(album_id)
    album_info = sp.album(album_id)
    tracks = results['items']
    
    # Results from Spotify API come back in pages
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    for track in tracks:
        track_row = {
            'spotify_id': track['id'],
            'spotify_uri': track['uri'],
            'album': album_info['name'],
            'name': track['name'],
            'release_date': album_info['release_date'],
            'track_number': track['track_number'],
            'popularity': sp.track(track['id'])['popularity']
        }

        # Get track features
        features = sp.audio_features(track['id'])[0]
        track_row.update({
            'danceability': features['danceability'],
            'energy': features['energy'],
            'key': features['key'],
            'loudness': features['loudness'],
            'mode': features['mode'],
            'speechiness': features['speechiness'],
            'acousticness': features['acousticness'],
            'instrumentalness': features['instrumentalness'],
            'liveness': features['liveness'],
            'valence': features['valence'],
            'tempo': features['tempo'],
            'duration_ms': features['duration_ms'],
            'time_signature': features['time_signature']
        })

        artist_data.append(track_row)

# Define columns for dataframe
cols = ['spotify_id', 'spotify_uri', 'album', 'name', 'popularity', 'release_date', 'track_number', 
        'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 
        'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

# Create dataframe
artist_dataframe = pd.DataFrame(artist_data, columns=cols)

# Export dataframe to CSV
artist_dataframe.to_csv('thenocturnalbroadcast.csv', index=False)