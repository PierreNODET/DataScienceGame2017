import unirest
import pandas as pd
import numpy as np
import sys

data = pd.DataFrame(columns = ['artist_id','nb_fan','nb_album','radio'])

df = pd.read_csv(cmd_folder + '/data/raw/train.csv')

def get_artists(ids):
    global data
    for idd in ids:
        response = unirest.get("https://deezerdevs-deezer.p.mashape.com/artist/"+str(idd),
        headers={
        "X-Mashape-Key": "eb4DzzTnELmshvFUju71GssNIry0p1tmYUajsnNUoQx2DDVkUN",
        "Accept": "text/plain"
        })
        try:
            data.loc[len(data)] = [idd,response.body['nb_fan'],response.body['nb_album'],response.body['radio']]
        except KeyError:
            data.loc[len(data)] = [idd,np.nan,np.nan,np.nan]

get_artists(df.artist_id.unique())

data.to_csv(cmd_folder + '/data/raw/api/infos.csv',index = False)

data = pd.DataFrame(columns = ['song_id','bpm','rank','gain','lyrics_explicits'])

def get_track(ids):
    global data
    compteur = 0
    compteur2 = 0
    for idd in ids:
        response = unirest.get("https://deezerdevs-deezer.p.mashape.com/track/"+str(idd),
        headers={
        "X-Mashape-Key": "eb4DzzTnELmshvFUju71GssNIry0p1tmYUajsnNUoQx2DDVkUN",
        "Accept": "text/plain"
        })
        try:
            data.loc[len(data)] = [idd,response.body['bpm'],response.body['rank'],response.body['gain'],response.body['explicit_lyrics']]
            #print([len(data)-1,idd,response.body['bpm'],response.body['rank'],response.body['gain'],response.body['explicit_lyrics']])
        except KeyError:
            data.loc[len(data)] = [idd,np.nan,np.nan,np.nan,np.nan]
            #print([len(data)-1,idd,np.nan,np.nan,np.nan,np.nan])
        compteur += 1
        if compteur % 50000 == 0:
            compteur2 +=1
            data.to_csv(cmd_folder + "/data/raw/api/enrich"+str(compteur2*compteur)+".csv",index = False)
            compteur = 0
            data = pd.DataFrame(columns = ['song_id','bpm','rank','gain','lyrics_explicits'])


get_track(df.media_id.unique())
