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
    playlist_features_list = ['timbre1_loudness',
        'timbre2_brightness',
        'timbre3_flatness',
        'timbre4_attack',
        'timbre5',
        'timbre6',
        'timbre7',
        'timbre8',
        'timbre9',
        'timbre10',
        'timbre11',
        'timbre12']

    playlist_df = pd.DataFrame(columns = playlist_features_list)

    # Loop through every track in the playlist, extract features and append the features to the playlist df

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

                # Get audio analysis - timbre
                audio_analysis = sp.audio_analysis(playlist_features["track_id"])
                audio_segments = audio_analysis['segments']
                timbre_vals = pd.DataFrame(audio_segments, columns=['timbre'])
                timbre_vals[['timbre1_loudness','timbre2_brightness','timbre3_flatness','timbre4_attack',
                    'timbre5','timbre6','timbre7','timbre8','timbre9','timbre10','timbre11',
                    'timbre12']] = pd.DataFrame(timbre_vals.timbre.tolist(), index= timbre_vals.index)
                timbre_full = pd.DataFrame(timbre_vals['timbre'].to_list(), columns=['timbre1_loudness',
                    'timbre2_brightness','timbre3_flatness','timbre4_attack','timbre5','timbre6','timbre7',
                    'timbre8','timbre9','timbre10','timbre11','timbre12'])
                timbre1 = timbre_full.mean()
                audio_timbre = pd.DataFrame(timbre1).transpose()
                for feature in playlist_features_list[0:]:
                    playlist_features[feature] = audio_timbre[feature]

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

energising_playlists_dict = {
    'Energising music' : ('louisep!', '76YdW0YY1aEYUwAUQPv2kr'),
    'GYM_PLAYLIST ENERGIE' : ('Energie Fitness', '4qJhnePHLlfgWqnvEAGnVH'),
    'Energizing Study Music - No Lyrics' : ('smd82408', '4axJH5T0SzA0G91NeszOws'),
#    'Foco com Energia' : ('Spotify', '37i9dQZF1DX8ZSkZGhJFi1'),
        # 2021 revisit - doesn't like this one, missing about two thirds of the tracks.
    'Enfoque con Energia' : ('Spotify', '37i9dQZF1DX5EY8JFBuaLS'),
    'Energizing Music' : ('chaj1', '7yKgnCJZQDlqOLFSr2HC56'),
    'Energiser' : ('nutatiahh', '2BIu9x9P6wXjrtsQtGepfg'),
    'Pura Energ??a' : ('Spotify', '37i9dQZF1DWYp5sAHdz27Y'),
#    'energizing songs' : ('kaitlyn_2898', '2REQF25ftpVd4itSGF6PMY'),
        # 2021 revisit - title changed to Workout; has very few likes anyway, so dropped.
    'Energia positiva' : ('salamander_05', '1xyGdY1GuPHaQyvikZglmB'),

    # 2021 ADDITIONS
    'Alta Vibraci??n 432 Hz & Energ??a Positiva' : ('Jordi Sanz', '1Upphcq8Euc3IpsIhuCnkw'),
    'Energia 97FM 2021' : ('hotvibesnetwork', '4ttPvH5KXUbAKpR6ucYD6R'),
# }

# dance_playlists_dict = {
    'Dance Hits' : ('Spotify', '37i9dQZF1DX0BcQWzuB7ZO'),
    'DANCE 2020' : ('Victor Oliveira', '0tLyGnQZ5T8wlu0tydvQU3'),
    'Dance Anthems 2021' : ('Double J Music', '0qiyp96nNBGdRLApUAmMtG'),
    'Dancehall 2021 [new]' : ('DJ Fabi Benz', '1AKuDAKQOUSbQ8KKJkrlMi'),
        # 2021 revisit - name change from fabi_benz.
    'Massive Dance Classics' : ('Spotify', '37i9dQZF1DWYtg7TV07mgz'),
    'Dance Party! Best Dance Hits' : ('Lost Records', '5oKz4DsTP8zbL97UIPbqp4'),
        # 2021 revisit - name change from Blurred Lines
    'Dance Workout' : ('Filtr UK', '7wBpRbIoatquCDVcxybHEk'),
#    'Dance Hits 2021' : ('Enforce The Sound', '4soPjt4Q9nPeAmVDlLAQtN'),
        # 2021 revisit - not found.
#    'Dancehall Official' : ('Spotify', '37i9dQZF1DXan38dNVDdl4'),
        # 2021 revisit - dropped below 50.
#    'The Dance List' : ('Spotify', '37i9dQZF1DX7364T8tu1TH'),
        # this playlist has changed, it now has only 49 tracks! replacement below.
    'Dance Pop' : ('Spotify','37i9dQZF1DWZQaaqNMbbXa'),

    # 2021 ADDITIONS
    'Dance Nation | Ministry of Sound' : ('Ministry of Sound', '7FUhHHA0zXAPVsJdDrNxNs'),
    'DANCE MUSIC 2021 Best Dance 2021 & EDM Hits 2021' : ('Filtr ??xitos', '6g40a9GjWBkX8ewR0vF9C2'),
# }

# workout_playlists_dict = {
    'Workout Music 2021' : ('BLACK DOT', '190wZ2oVo7MTrBvNlPiub2'),
    'Workout' : ('Spotify', '37i9dQZF1DX70RN3TfWWJh'),
#    'Rap Workout' : ('Spotify', '37i9dQZF1DX76t638V6CA8'),
        # This one not working for the timbre extraction, weirdly? have replaced with the one at the end,
        # also a workout playlist, this one had the most likes of the extras remaining. may need to
        # change the other one as well so they're consistent.
    'The Rock Workout' : ('Spotify', '37i9dQZF1DX6hvx9KDaW4s'),
    'Workout Beats' : ('Spotify', '37i9dQZF1DWUSyphfcc6aL'),
    'Workout Motivation 2021' : ('Jay Cutler', '2237sMNMlXS4wWLgdQ1UuV'),
    'Workout Playlist 2021' : ('metr', '7AiuMp1D8Hli18nyTbriZ9'),
    'Workout Bhangra' : ('Spotify', '37i9dQZF1DX8To1hlfhp7U'),
    'Workout Beats 2021' : ('Selected', '4XIEV4NaByrujFUjFoG32v'),
    '80s Workout' : ('Spotify', '37i9dQZF1DWZY6U3N4Hq7n'),
    'Adrenaline Workout' : ('Spotify', '37i9dQZF1DXe6bgV3TmZOL')
}

energising_playlists_df = analyze_playlist_dict(energising_playlists_dict)

energising_playlists_df.to_csv('energising_playlists_timbres.csv')
