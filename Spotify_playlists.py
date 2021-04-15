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

# Dictionaries of playlist manually collected from search results, 'name: ('creator', 'playlist_id')'
sleep_playlists_dict = {
    'Sleep' : ('Spotify', '37i9dQZF1DWZd79rJ6a7lp'),
    'Deep Sleep' : ('Spotify', '37i9dQZF1DWYcDQ1hSjOpY'),
    'Sleep Piano Music' : ('Pryve', '7xhcF9ddiyF8Skbd1tenro'),
    'Baby Sleep' : ('Spotify', '37i9dQZF1DX0DxcHtn4Hwo'),
    'Songs For Sleeping' : ('Spotify', '37i9dQZF1DWStLt4f1zJ6I'),
    'Sleep, Baby Sleep' : ('Spotify', '37i9dQZF1DXdJ5OFSzWeCS'),
    'Sleepy Piano' : ('Spotify', '37i9dQZF1DX03b46zi3S82'),
    'Jazz for Sleep' : ('Spotify', '37i9dQZF1DXa1rZf8gLhyz'),
    'Sleep Piano' : ('Ron Adelaar', '1Ty8JKNLTI5C7DKE65jvb9'),
    'LoFi Sleep' : ('James Gilsdorf', '3DP5Khm13rl3I9mQkgX6fx'),
    'Sleep Tight' : ('Spotify', '37i9dQZF1DWSUFOo47GEsI'),
    'Classical Sleep' : ('Spotify', '37i9dQZF1DX8Sz1gsYZdwj'),
    'Sleep Sounds' : ('Filtr', '6k6C04ObdWs3RjsabtRUQa'),
    'Sleep Lullabies' : ('gkyla', '30oR4iBzmouadY8aawVODx'),
    'Sleep: Into the Ocean' : ('Spotify', '37i9dQZF1DXabJG3i5q2yk'),
    'sleep songs' : ('mallen2505', '7lyhW4iOuUumlDubpwBXsS'),
    'Soothing Strings For Sleeping Babies' : ('Spotify', '37i9dQZF1DX2C8CFEPyYmg'),
    'Lo-Fi Beats' : ('Spotify', '37i9dQZF1DWWQRwui0ExPn'),
    'SLEEPY TIME' : ('macyleeeeedavis22', '68JXTKfqFZEWO1DQRdVndh'),
    'Sleeping Songs' : ('megan21', '5OajoGDWc6pK101SCqH1R7'),
    'Sleepy Music' : ('Sleepy Times', '1u9NkEi4uwvlKu1Nlhx5T7'),
    'Baby Sleep Aid: White Noise' : ('Spotify', '37i9dQZF1DXby8tlLbzqaH'),
    'Sleeping Songs 2020' : ('Johansson Jimmy', '4DggdFdvUbwW3X7E6Rtw9Y'),
    'Lullabies for Sleep' : ('Double J Music', '25wThb57sSId0kPwhgSgaO'),
    'Lofi Fruits Music lofi hip hop music to chill, relax, study, sleep to' : ('Strange Fruits', '3LFIBdP7eZXJKqf3guepZ1'),
    'Relaxing Rain Sleep Sounds' : ('Filtr Sweden', '7f24KaDrATReBg45esAgX8'),
    'ASMR Sleep' : ('Spotify', '37i9dQZF1DWUAeTOoyNaqm'),
    'Sleep Noise' : ('Spotify', '37i9dQZF1DWSW4ppn40bal'),
    'Sad songs for crying yourself to sleep' : ('Indiemono', '7ABD15iASBIpPP5uJ5awvq'),
    '432 Hz Sleep Music' : ('Miracle Tones', '4wavvfiVFxWmGgjkR5w0Fh')
}

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
    'Relaxing Guitar Music' : ('Augustín Amigó', '6wFWKXnsBFQxWQjSug7ory'),
    'Relaxing Jazz Background Music' : ('jazz_jazz_jazz75', '71tQFRd9OWYWWSQdxLQccn'),
    'Hanging Out and Relaxing' : ('Spotify', '37i9dQZF1DXci7j0DJQgGp'),
    'Relax in the Bath' : ('Matt Johnson', '5sMfgeII8qGOwcgxfqqDaM'),
    'Relaxing Songs' : ('lyssastreiner', '4D3hxAbOjVu5jaC5Bnlmky'),
    'Soothing Relaxation' : ('Soothing Relaxation', '4AyG5SW1hu3toT9kd9PSXR'),
    'Relaxing Reading' : ('Spotify', '37i9dQZF1DX3DZBe6wPMXo'),
    'Relaxing acoustic' : ('samkeane-gb', '4rdl06oulIdgDNjJts2rmp'),
    'Relaxing Pop' : ('Mindy Moss Shaffer', '3LNyeJ7KMVZvNp9zClWCW3'),
    'Relaxing Spanish Guitar' : ('Spotify', '37i9dQZF1DX6BbeVFYBeZs'),
    'Relaxing Spa Music' : ('zenmeditationplanet', '0pUKEVfbKICpYx35RozAk7'),
    'Relaxing Bathing Music' : ('Hopeyoh', '25wunaTFoLta4HrjNvwHcK'),
    'Deep House Relax' : ('Spotify', '37i9dQZF1DX2TRYkJECvfC'),
    'Relaxing Songs for headaches' : ('Pie', '0B1cW8x7Mopg6Du5BJ4spM'),
    'Piano Relaxation' : ('Piano Relaxation', '04Bx6c3eZmYdWZRkQrLB7l'),
    'Bach Relax' : ('Spotify', '37i9dQZF1DWU1JctQodQRj'),
    'Relaxing & Chill House 2020 The Good Life Radio' : ('Sensual Musique', '75XrS5HXOmVYMgdXlaQTwO'),
    'Relax Tayo' : ('Spotify', '37i9dQZF1DWU96w4Gh7vJe'),
    'Meditação e Relaxamento' : ('Spotify', '37i9dQZF1DXaKgOqDv3HpW'),
    'Mindfulness - Focus/Relax' : ('tommyberre','2ozb9cgwMcl2SDWK4SLRp8')
}

energising_playlists_dict = {
    'Energising music' : ('louisep!', '76YdW0YY1aEYUwAUQPv2kr'),
    'GYM_PLAYLIST ENERGIE' : ('Energie Fitness', '4qJhnePHLlfgWqnvEAGnVH'),
    'Energizing Study Music - No Lyrics' : ('smd82408', '4axJH5T0SzA0G91NeszOws'),
    'Foco com Energia' : ('Spotify', '37i9dQZF1DX8ZSkZGhJFi1'),
    'Enfoque con Energia' : ('Spotify', '37i9dQZF1DX5EY8JFBuaLS'),
    'Energizing Music' : ('chaj1', '7yKgnCJZQDlqOLFSr2HC56'),
    'Energiser' : ('nutatiahh', '2BIu9x9P6wXjrtsQtGepfg'),
    'Pura Energía' : ('Spotify', '37i9dQZF1DWYp5sAHdz27Y'),
    'energizing songs' : ('kaitlyn_2898', '2REQF25ftpVd4itSGF6PMY'),
    'Energia positiva' : ('salamander_05', '1xyGdY1GuPHaQyvikZglmB'),
    'Dance Hits' : ('Spotify', '37i9dQZF1DX0BcQWzuB7ZO'),
    'DANCE 2020' : ('Victor Oliveira', '0tLyGnQZ5T8wlu0tydvQU3'),
    'Dance Anthems 2020' : ('Double J Music', '0qiyp96nNBGdRLApUAmMtG'),
    'Dancehall 2020 [new]' : ('fabi_benz', '1AKuDAKQOUSbQ8KKJkrlMi'),
    'Massive Dance Classics' : ('Spotify', '37i9dQZF1DWYtg7TV07mgz'),
    'Dance Party! Best Dance Hits' : ('Blurred Lines', '5oKz4DsTP8zbL97UIPbqp4'),
    'Dance Workout' : ('Filtr UK', '7wBpRbIoatquCDVcxybHEk'),
    'Dance Hits 2020' : ('Enforce The Sound', '4soPjt4Q9nPeAmVDlLAQtN'),
    'Dancehall Official' : ('Spotify', '37i9dQZF1DXan38dNVDdl4'),
    'Dance Pop' : ('Spotify','37i9dQZF1DWZQaaqNMbbXa'),
    'Workout Music 2020' : ('BLACK DOT', '190wZ2oVo7MTrBvNlPiub2'),
    'Workout' : ('Spotify', '37i9dQZF1DX70RN3TfWWJh'),
    'The Rock Workout' : ('Spotify', '37i9dQZF1DX6hvx9KDaW4s'),
    'Workout Beats' : ('Spotify', '37i9dQZF1DWUSyphfcc6aL'),
    'Workout Motivation 2020' : ('Jay Cutler', '2237sMNMlXS4wWLgdQ1UuV'),
    'Workout Playlist 2020' : ('metr', '7AiuMp1D8Hli18nyTbriZ9'),
    'Workout Bhangra' : ('Spotify', '37i9dQZF1DX8To1hlfhp7U'),
    'Workout Beats 2020' : ('Selected', '4XIEV4NaByrujFUjFoG32v'),
    '80s Workout' : ('Spotify', '37i9dQZF1DWZY6U3N4Hq7n'),
    'Adrenaline Workout' : ('Spotify', '37i9dQZF1DXe6bgV3TmZOL')
}

# Run main function on each playlist dictionary
sleep_playlists_df = analyze_playlist_dict(sleep_playlists_dict)
relaxing_playlists_df = analyze_playlist_dict(relaxing_playlists_dict)
energising_playlists_df = analyze_playlist_dict(energising_playlists_dict)

# Export results to .csv files
sleep_playlists_df.to_csv('sleep_playlists.csv')
relaxing_playlists_df.to_csv('relaxing_playlists.csv')
energising_playlists_df.to_csv('energising_playlists.csv')
