import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

from os import listdir

def writeToFile(line, var):
    with open(f'final-data/EndingData-{var}.csv', 'a+') as f:
        f.write(line + '\n')

week_lists = listdir("3b")
weekly_lists = []
# print(weekly_lists)
for i in week_lists:
    weekly_lists.append(i[:-4])

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

spotify_data = ''
list_num=0
for i in weekly_lists:
    with open("3b/"+i+'.csv', 'r', encoding="utf8") as f:
        spotify_data = f.read()
        # print(spotify_data)

    songs = spotify_data.split("\n")
    info = ''
    for j in songs:
        # print(j)
        if "/track/" in j:
            data, url = j.split('/track/')
            info += url + '\n'
        else:
            pass
    with open(f'raw-data/songs-{i}.txt','w', encoding='utf8') as f:
        f.write(info)

    songs = ''
    genres = []
    with open(f'raw-data/songs-{i}.txt', 'r', encoding='utf8') as f:
        song = f.readline()
        while song:
            track = spotify.track(song.rstrip())['artists'][0]['id']
            artist = spotify.artist(track)
            if artist['genres']:
                genre = artist['genres'][0]
            else:
                genre = 'None'
            artist = artist['name']
            genres.append(genre)
            song = f.readline()

    data = ""
    with open('3b/'+i+'.csv', "r", encoding='utf8') as f:
        data = f.read()

    datum = data.split("\n")
    try:
        for j, line in enumerate(datum):
            # print(j)
            # print(line)
            dat = line.split(",")
            dat.append(genres[j])
            writeToFile(",".join(dat), i)
        list_num += 1
        print(f'file #{list_num}complete out of {len(weekly_lists)}')
        time.sleep(120)
    except IndexError:
        pass
    except Exception as e:
        print("SOMETHING WENT WRONG")
        print("ASK NATHAN FOR HELP")
        print(e)


    