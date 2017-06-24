import pandas as pd
from scipy import stats
from make_dir import cmd_folder

train = pd.read_csv(cmd_folder+"data/inter/train.csv")
user_profile = pd.read_csv(cmd_folder+"data/raw/user_profile.csv")

user_profile["user_occurence"]=train.groupby("user_id").count().iloc[:,1]

user_profile = pd.merge(user_profile,pd.get_dummies(train[["platform_name","user_id"]].groupby("user_id").agg(lambda x: stats.mode(x)[0][0]).reset_index(),columns=["platform_name"],drop_first=True),on="user_id")

user_profile = pd.merge(user_profile,pd.get_dummies(train[["platform_family","user_id"]].groupby("user_id").agg(lambda x: stats.mode(x)[0][0]).reset_index(),columns=["platform_family"],drop_first=True),on="user_id")

user_profile = pd.merge(user_profile,train[["listen_type","user_id"]].groupby("user_id").agg(lambda x: stats.mode(x)[0][0]).reset_index(),on="user_id")
user_profile.rename(columns={'listen_type':'user_prefered_listen_type','platform_name_1':'user_prefered_platform_name_1','platform_name_2':'user_prefered_platform_name_2','platform_family_2':'user_prefered_platform_family_2','platform_family_1':'user_prefered_platform_family_1'},inplace=True)

user_profile = pd.merge(user_profile,pd.get_dummies(train[["context_type","user_id"]].groupby("user_id").agg(lambda x: stats.mode(x)[0][0]).reset_index(),columns=["context_type"],drop_first=True)[["user_id","context_type_1","context_type_5","context_type_20","context_type_23"]],on="user_id")
user_profile.rename(columns={'context_type_1':'user_prefered_context_type_1','context_type_5':'user_prefered_context_type_5','context_type_20':'user_prefered_context_type_20','context_type_23':'user_prefered_context_type_23'},inplace=True)

user_profile = pd.merge(user_profile,(train[["moment_listen","user_id"]].groupby(["user_id","moment_listen"]).size()/train[["moment_listen","user_id"]].groupby(["user_id"]).size()).unstack().reset_index(),on="user_id")
user_profile.rename(columns={'afternoon':'user_mean_is_listened_afternoon','evening':'user_mean_is_listened_evening','late_afternoon':'user_mean_is_listened_late_afternoon','morning':'user_mean_is_listened_morning','night':'user_mean_is_listened_night'},inplace=True)

user_profile = pd.merge(user_profile,(train[["weekday_listen","user_id"]].groupby(["user_id","weekday_listen"]).size()/train[["weekday_listen","user_id"]].groupby(["user_id"]).size()).unstack().reset_index(),on="user_id")
user_profile["weekday"]=user_profile[0]+user_profile[1]+user_profile[2]+user_profile[3]+user_profile[4]
user_profile["weekend"]=user_profile[5]+user_profile[6]
for i in range(7):
    user_profile.rename(columns={i:'user_mean_is_listened_weekday_'+str(i)},inplace=True)
user_profile.rename(columns={'weekday':'user_mean_is_listened_weekday','weekend':'user_mean_is_listened_weekend'},inplace=True)

user_profile["user_mean_is_listened_weekend_weekday_diff"] = user_profile.user_mean_is_listened_weekend - user_profile.user_mean_is_listened_weekday

user_profile = pd.merge(user_profile,train[["is_listened","user_id"]].groupby("user_id").mean().reset_index(),on="user_id")
user_profile.rename(columns={'is_listened':'user_mean_is_listened'},inplace=True)

user_profile = pd.merge(user_profile,train[["is_listened","user_id","listen_type"]].groupby(["user_id","listen_type"]).mean().unstack().reset_index(),on="user_id")
user_profile.rename(columns={user_profile.columns[29]:'user_mean_is_listened_listen_type_0'},inplace=True)
user_profile.rename(columns={user_profile.columns[30]:'user_mean_is_listened_listen_type_1'},inplace=True)

user_profile["user_mean_is_listened_listen_type_diff"] = user_profile.user_mean_is_listened_listen_type_0 - user_profile.user_mean_is_listened_listen_type_1

user_profile = pd.merge(user_profile,((train[["album_id","user_id"]].groupby("user_id").nunique()["album_id"])/train[["user_id"]].groupby("user_id").size()).reset_index(),on="user_id")
user_profile.rename(columns={0:'user_album_per_media'},inplace=True)

media_profile = pd.read_csv(cmd_folder + "data/inter/media_profile.csv")

user_profile = pd.merge(user_profile,pd.get_dummies(pd.merge(media_profile[["release_period","media_id"]],train[["media_id","user_id"]],on="media_id").groupby("user_id").apply(pd.DataFrame.mode)[["user_id","release_period"]],columns=["release_period"]),on="user_id")
user_profile.rename(columns={'release_period_60s - 80s':'user_prefered_release_period_60s - 80s'},inplace=True)
user_profile.rename(columns={'release_period_80s - 2010s':'user_prefered_release_period_80s - 2010s'},inplace=True)
user_profile.rename(columns={'release_period_after 2010s':'user_prefered_release_period_after 2010s'},inplace=True)
user_profile.rename(columns={'release_period_before 60s':'user_prefered_release_period_before 60s'},inplace=True)

user_profile = pd.merge(user_profile,train[["recent_media","user_id"]].groupby("user_id").mean().reset_index(),on="user_id")
user_profile.rename(columns={'recent_media':'like_recent_media'},inplace=True)

genre_profile = pd.read_csv(cmd_folder + "data/inter/genre_profile.csv")

user_profile = pd.merge(user_profile,pd.get_dummies(pd.merge(genre_profile[["genre_popularity","genre_id"]],train[["genre_id","user_id"]],on="genre_id").groupby("user_id").apply(pd.DataFrame.mode)[["user_id","genre_popularity"]],columns=["genre_popularity"]),on="user_id")
user_profile.rename(columns={'genre_popularity_rare':'user_prefered_genre_popularity_rare'},inplace=True)
user_profile.rename(columns={'genre_popularity_known':'user_prefered_genre_popularity_known'},inplace=True)
user_profile.rename(columns={'genre_popularity_popular':'user_prefered_genre_popularity_popular'},inplace=True)
user_profile.columns

user_profile.to_csv("data/processed/user_profile.csv",index=False)
