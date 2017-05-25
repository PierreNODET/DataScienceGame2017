import pandas as pd
import numpy as np
from find_dir import cmd_folder

df = pd.read_csv(cmd_folder + '/data/raw/train.csv')

test1 = pd.read_csv(cmd_folder + '/data/raw/api/enrich78617-0.csv')
test2 = pd.read_csv(cmd_folder + '/data/raw/api/enrich50000-1.csv')
test3 = pd.read_csv(cmd_folder + '/data/raw/api/enrich43227-2.csv')
test4 = pd.read_csv(cmd_folder + '/data/raw/api/enrich41704-3.csv')
test5 = pd.read_csv(cmd_folder + '/data/raw/api/enrich50000-4.csv')
test6 = pd.read_csv(cmd_folder + '/data/raw/api/enrich50000-5.csv')
test7 = pd.read_csv(cmd_folder + '/data/raw/api/enrich100000-6.csv')
test8 = pd.read_csv(cmd_folder + '/data/raw/api/enrich57931-6.csv')

frames = [test1,test2,test3,test4,test5,test6,test7,test8]

concat = pd.concat(frames)
concat = concat.drop(concat.columns[[0]],axis = 1)
concat['song_id'] = concat['song_id'].astype('int64')
#concat.columns.values[0] = 'media_id'
#concat.columns
merged = pd.merge(df, concat, how='left', left_on =['media_id'],right_on=['song_id'])
# (merged.media_id == merged.song_id).sum()/7558835
merged.drop('song_id',axis = 1,inplace = True)

concat.reset_index(inplace = True,drop = True)

concat.to_csv(cmd_folder + "/data/raw/api/infos_musics.csv",index = False)
