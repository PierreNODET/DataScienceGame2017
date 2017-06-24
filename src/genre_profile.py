import pandas as pd
from src.make_dir import cmd_folder

train = pd.read_csv(cmd_folder + '/data/inter/train.csv')
test = pd.read_csv(cmd_folder + '/data/inter/test.csv')

media_profile = pd.read_csv(cmd_folder + '/data/inter/media_profile.csv')

genre_profile = pd.DataFrame(media_profile.genre_id.unique(),columns=["genre_id"]).set_index("genre_id")

kek = pd.merge(train[["media_id","is_listened"]],media_profile[["genre_id","media_id"]],on="media_id")

genre_profile["genre_occurence"] = kek.genre_id.value_counts()

genre_profile["genre_is_listened"] = kek[["is_listened","genre_id"]].groupby("genre_id").mean()

genre_profile["genre_popularity"] = pd.qcut(genre_profile.genre_occurence,[0,0.25,0.5,0.75,1],labels=["hipster","rare","known","popular"])

genre_profile["genre_likeliness"] = pd.qcut(genre_profile.genre_is_listened,[0,0.25,0.5,0.75,1],labels=["dislike","ok","like","love"])

genre_profile.reset_index(inplace=True)

genre_profile.to_csv("data/inter/genre_profile.csv",index=False)

genre_profile = pd.concat([genre_profile,pd.get_dummies(genre_profile.genre_popularity,prefix="genre_popularity_is")],axis = 1)

genre_profile = pd.concat([genre_profile,pd.get_dummies(genre_profile.genre_likeliness,prefix="genre_likeliness_is")],axis = 1)

genre_profile.drop(["genre_likeliness","genre_popularity"],axis = 1, inplace=True)

genre_profile.to_csv("data/processed/genre_profile.csv",index=False)
