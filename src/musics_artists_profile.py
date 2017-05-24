import pandas as pd
from make_dir import cmd_folder

df = pd.read_csv(cmd_folder + '/data/raw/train.csv')

musics = pd.read_csv(cmd_folder + '/data/raw/api/infos_musics.csv')
musics = musics.rename(columns={"song_id":"media_id"})

artists = pd.read_csv(cmd_folder + '/data/raw/api/infos.csv')
artists['artist_id'] = artists['artist_id'].astype('int64')

#df.groupby(['artist_id']).agg(lambda x:x.value_counts().index[0])
occ_artists = pd.DataFrame(df.groupby(['artist_id']).count().sort_values(['media_id'],ascending=False).iloc[:,0])
occ_artists.reset_index(inplace= True)
merg_artist = pd.merge(artists,occ_artists,how='left',on='artist_id')
merg_artist = merg_artist.rename(columns = {'genre_id':'occurences'})


occ_musics = pd.DataFrame(df.groupby(['media_id']).count().sort_values(['genre_id'],ascending=False).iloc[:,0])
occ_musics.reset_index(inplace= True)
merg_musics = pd.merge(musics,occ_musics,how='left',on='media_id')
merg_musics = merg_musics.rename(columns = {'genre_id':'occurences'})

merg_artist.to_csv(cmd_folder + '/data/raw/infos_artists.csv',index = False)
merg_musics.to_csv(cmd_folder + '/data/raw/infos_musics.csv',index = False)
