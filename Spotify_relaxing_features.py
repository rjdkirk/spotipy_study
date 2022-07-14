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

    n = 0

    while len(sp.user_playlist_tracks(creator, playlist_id, limit=100, offset=n)["items"]) > 0:

        playlist = sp.user_playlist_tracks(creator, playlist_id, limit=100, offset=n)["items"]
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
            try:
                for feature in playlist_features_list[4:]:
                    playlist_features[feature] = audio_features[feature]
            except:
                pass

            # Concat the dfs
            track_df = pd.DataFrame(playlist_features, index = [0])
            playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)

        n += 100

    return playlist_df

def analyze_playlist_dict(playlist_dict):

    # Loop through every playlist in the dict and analyze it
    for i, (key, val) in enumerate(playlist_dict.items()):
        playlist_df = analyze_playlist(*val)
        # Add a playlist column so that we can see which playlist a track belongs too
        playlist_df["playlist"] = key
        # Create or concat df
        if i == 0:
            playlist_dict_df = playlist_df
        else:
            playlist_dict_df = pd.concat([playlist_dict_df, playlist_df], ignore_index = True)

    return playlist_dict_df

relaxing_playlists_dict = {
    'Relax & Unwind' : ('Spotify', '37i9dQZF1DWU0ScTcjJBdj'),
    'Relaxing Massage' : ('Spotify', '37i9dQZF1DXebxttQCq0zA'),
    'Relaxing Music 2020' : ('Lofi Infini', '0Ie5X3JS6BrLSWKrRm310H'),
    'Ambient Relaxation' : ('Spotify', '37i9dQZF1DX3Ogo9pFvBkY'),
    'Pop Relax' : ('Spotify', '37i9dQZF1DX3SQwW1JbaFt'),
    'Relaxing Classical' : ('Filtr UK', '1ZJpJahEFst7u8njXeGFyv'),
    'Relaxing Piano' : ('Double J Music', '0OOZzfr4olaGarfeaydGZf'),
    'Relaxing Piano soft & calming piano music for relaxation' : ('Dream Relaxation', '2ODMZHnO9zcajVJ54Rlhz7'),
    'lofi hip hop music beats to relax/study to' : ('ChilledCow', '0vvXsWCC9xrXsKd4FyS8kM'),
    'Jazz Relax' : ('Spotify', '37i9dQZF1DXbOVU4mpMJjh'),
    'Relaxing Guitar Music' : ('Florecilla Records', '6wFWKXnsBFQxWQjSug7ory'),
        # 2021 revisit - creator name change, was Augustín Amigó.
    'Relaxing Jazz Background Music' : ('jazz_jazz_jazz75', '71tQFRd9OWYWWSQdxLQccn'),
    'Hanging Out and Relaxing' : ('Spotify', '37i9dQZF1DXci7j0DJQgGp'),
    'Relax in the Bath' : ('Matt Johnson', '5sMfgeII8qGOwcgxfqqDaM'),
    'Relaxing Songs' : ('lyssastreiner', '4D3hxAbOjVu5jaC5Bnlmky'),
#    'Relax en casa' : ('Spotify', '37i9dQZF1DXcjpPPxCzYRE'),
        # this one above isn't working for some reason? have swapped it out and added another
        # playlist at the end of the list.
    'Soothing Relaxation' : ('Soothing Relaxation', '4AyG5SW1hu3toT9kd9PSXR'),
    'Relaxing Reading' : ('Spotify', '37i9dQZF1DX3DZBe6wPMXo'),
    'Relaxing acoustic' : ('samkeane-gb', '4rdl06oulIdgDNjJts2rmp'),
    'Relaxing Pop' : ('Mindy Moss Shaffer', '3LNyeJ7KMVZvNp9zClWCW3'),
    'Relaxing Spanish Guitar' : ('Spotify', '37i9dQZF1DX6BbeVFYBeZs'),
    'Relaxing Spa Music' : ('zenmeditationplanet', '0pUKEVfbKICpYx35RozAk7'),
#    'Relaxing Bathing Music' : ('Hopeyoh', '25wunaTFoLta4HrjNvwHcK'),
        # 2021 revisit - name has now changed to just Bath/Shower, no mention of relaxing.
    'Deep House Relax' : ('Spotify', '37i9dQZF1DX2TRYkJECvfC'),
    'Relaxing Playlist' : ('Pie', '0B1cW8x7Mopg6Du5BJ4spM'),
        # 2021 revisit - name change from Relaxing Songs for headaches.
    'Piano Relaxation' : ('Piano Relaxation', '04Bx6c3eZmYdWZRkQrLB7l'),
    'Bach Relax' : ('Spotify', '37i9dQZF1DWU1JctQodQRj'),
    'Relaxing & Chill House 2021 The Good Life Radio' : ('Sensual Musique', '75XrS5HXOmVYMgdXlaQTwO'),
        # 2021 revisit - title changed from the 2020 edition.
    'Relax Tayo' : ('Spotify', '37i9dQZF1DWU96w4Gh7vJe'),
    'Meditação e Relaxamento' : ('Spotify', '37i9dQZF1DXaKgOqDv3HpW'),
#    'Relaxing Music' : ('akalones', '6j8jy0z4ODGxBAySLI6Sty')
        # and this one has since dropped under 50 tracks! replacing with one below.
    'Mindfulness - Focus/Relax' : ('1165 Recordings','2ozb9cgwMcl2SDWK4SLRp8'),
        # Creator name change, was tommyberre

    # 2021 ADDITIONS
    'Relaxing Music' : ('Pryve', '1r4hnyOWexSvylLokn2hUa')
}

relaxing_playlists_df = analyze_playlist_dict(relaxing_playlists_dict)
relaxing_playlists_df.to_csv('relaxing_playlists_features.csv')
