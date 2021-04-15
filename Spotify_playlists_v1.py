# I have essentially used this https://towardsdatascience.com/how-to-create-large-music-datasets-using-spotipy-40e7242cc6a6 

import csv
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'xxxx'
client_secret = 'xxxx'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def analyze_playlist(creator, playlist_id):

    # Create empty dataframe
    playlist_features_list = ["artist",
        "album",
        "track_name",
        "track_id",
        "acousticness",
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "duration_ms",
        "time_signature"]

    playlist_df = pd.DataFrame(columns = playlist_features_list)

    # Loop through every track in the playlist, extract features and append the features to the playlist df

    playlist = sp.user_playlist_tracks(creator, playlist_id, limit=50)["items"]
    for track in playlist:
        # Create empty dict
        playlist_features = {}
        # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]

        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]

        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index = [0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)

    return playlist_df

def analyze_playlist_dict(playlist_dict):

    # Loop through every playlist in the dict and analyze it
    for i, (key, val) in enumerate(playlist_dict.items()):
        playlist_df = analyze_playlist(*val)
        # Add a playlist column so that we can see which playlist a track belongs to
        playlist_df["playlist"] = key
        # Create or concat df
        if i == 0:
            playlist_dict_df = playlist_df
        else:
            playlist_dict_df = pd.concat([playlist_dict_df, playlist_df], ignore_index = True)

    return playlist_dict_df

# Dictionaries of playlist manually collected from search results, 'name' : ('creator', 'playlist_id'). I have separated my three categories, but these 
# could of course be compiled in one dict instead.
sleep_playlists_dict = {
    'Sleep' : ('Spotify', '37i9dQZF1DWZd79rJ6a7lp'),
    'Deep Sleep' : ('Spotify', '37i9dQZF1DWYcDQ1hSjOpY'),
    'Sleep Piano Music' : ('Pryve', '7xhcF9ddiyF8Skbd1tenro'),
    
    # etc.
}

relaxing_playlists_dict = {
    'Relax & Unwind' : ('Spotify', '37i9dQZF1DWU0ScTcjJBdj'),
    'Relaxing Classical' : ('Filtr UK', '1ZJpJahEFst7u8njXeGFyv'),
    'lofi hip hop music beats to relax/study to' : ('ChilledCow', '0vvXsWCC9xrXsKd4FyS8kM'),
    
    # etc.
}

energising_playlists_dict = {
    'Energising music' : ('louisep!', '76YdW0YY1aEYUwAUQPv2kr'),
    'Dance Hits' : ('Spotify', '37i9dQZF1DX0BcQWzuB7ZO'),
    'Workout Music 2020' : ('BLACK DOT', '190wZ2oVo7MTrBvNlPiub2'),
    
    # etc.
}

# Run main function on each playlist dictionary
sleep_playlists_df = analyze_playlist_dict(sleep_playlists_dict)
relaxing_playlists_df = analyze_playlist_dict(relaxing_playlists_dict)
energising_playlists_df = analyze_playlist_dict(energising_playlists_dict)

# Export results to .csv files
sleep_playlists_df.to_csv('sleep_playlists.csv')
relaxing_playlists_df.to_csv('relaxing_playlists.csv')
energising_playlists_df.to_csv('energising_playlists.csv')
