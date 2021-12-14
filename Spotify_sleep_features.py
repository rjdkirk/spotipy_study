import csv
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'bc14dbad3a614e6bac21a603e03e343c'
client_secret = 'd6e20186fd5448f384012f42756b7f5a'
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
    # Using the offset and a while loop to break the limitter.

    n = 0

    while len(sp.user_playlist_tracks(creator, playlist_id, limit=100, offset=n)["items"]) > 0:

        playlist = sp.user_playlist_tracks(creator, playlist_id, limit=100, offset=n)["items"]
        try:
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
        except:
            pass

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
#    'Sleeping Songs' : ('Sleepy Sounds', '6EgSj5fXmdfDPdpnEEv4EU'),
        # and this one has turned into something else entirely. think i've run out of extra sleep
        # playlists which means I will have to search for a new one to add.
    'Sleep Lullabies' : ('gkyla', '30oR4iBzmouadY8aawVODx'),
    'Sleep: Into the Ocean' : ('Spotify', '37i9dQZF1DXabJG3i5q2yk'),
#    'sleep songs' : ('mallen2505', '7lyhW4iOuUumlDubpwBXsS'),
        # 2021 revisit - this one still appears but it has lost its title and does not show up on the users
        # profile.
    'Soothing Strings For Sleeping Babies' : ('Spotify', '37i9dQZF1DX2C8CFEPyYmg'),
    'Lo-Fi Beats' : ('Spotify', '37i9dQZF1DWWQRwui0ExPn'),
    'SLEEPY TIME' : ('macyleeeeedavis22', '68JXTKfqFZEWO1DQRdVndh'),
    'Sleeping Songs' : ('megan21', '5OajoGDWc6pK101SCqH1R7'),
        # two Sleeping Songs playlists, didn't like that, numbered them now...
    'Sleepy Music' : ('Sleepy Times', '1u9NkEi4uwvlKu1Nlhx5T7'),
    'Baby Sleep Aid: White Noise' : ('Spotify', '37i9dQZF1DXby8tlLbzqaH'),
#    'Sleeping Songs 2020' : ('Johansson Jimmy', '4DggdFdvUbwW3X7E6Rtw9Y'),
        # 2021 revisit - this one has changed to something completely different.
    'Lullabies for Sleep' : ('Double J Music', '25wThb57sSId0kPwhgSgaO'),
    'Lofi Fruits Music lofi hip hop music to chill, relax, study, sleep to' : ('Strange Fruits', '3LFIBdP7eZXJKqf3guepZ1'),
    'Relaxing Rain Sleep Sounds' : ('Filtr Sweden', '7f24KaDrATReBg45esAgX8'),
    'ASMR Sleep' : ('Spotify', '37i9dQZF1DWUAeTOoyNaqm'),
    'Sleep Noise' : ('Spotify', '37i9dQZF1DWSW4ppn40bal'),
#    'Sad songs for crying yourself to sleep' : ('Indiemono', '7ABD15iASBIpPP5uJ5awvq'),
        #  2021 revisit - still sad songs, but no longer mentions sleep.
    '432 Hz Sleep Music' : ('Miracle Tones', '4wavvfiVFxWmGgjkR5w0Fh'),

    # 2021 ADDITIONS
    'Calming Sleep Music' : ('gery07', '6X7wz4cCUBR6p68mzM7mZ4'),
    'Sleeping Music' : ('TheGoodVibe', '7mVeHiaEmixl8tKak7UwQT'),
    'Sleep Music' : ('LoudKult', '21wbvqMl5HNxhfi2cNqsdZ')
}

sleep_playlists_df = analyze_playlist_dict(sleep_playlists_dict)

sleep_playlists_df.to_csv('sleep_playlists_features.csv')
