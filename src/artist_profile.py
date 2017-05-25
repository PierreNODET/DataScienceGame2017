import pandas as pd
from make_dir import cmd_folder

train = pd.read_csv(cmd_folder + '/data/inter/train.csv')
test = pd.read_csv(cmd_folder + '/data/inter/test.csv')

artist_profile = pd.read_csv(cmd_folder + '/data/raw/artist_profile.csv')
artist_infos = pd.read_csv(cmd_folder + '/data/raw/infos_artists.csv')

artist_profile = pd.merge(artist_infos,artist_profile,on="artist_id",how="outer")

artist_profile = artist_profile.merge(train[["artist_id","is_listened"]].groupby("artist_id").mean().reset_index(),on="artist_id",how="outer")
artist_profile.rename(columns={'is_listened':'mean_artist_is_listened'},inplace=True)

artist_profile.to_csv(cmd_folder + '/data/inter/media_profile.csv',index=False)
