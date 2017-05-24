import pandas as pd
from scipy import stats

train = pd.read_csv("data/inter/train.csv")
user_profile = pd.read_csv("data/inter/user_profile.csv")

user_profile["user_occurence"]=train.groupby("user_id").count().iloc[:,1]

#train["platform_name"]=pd.Series(train["platform_name"],dtype="category")
user_profile = pd.merge(user_profile,train[["platform_name","user_id"]].groupby("user_id").agg(lambda x: stats.mode(x)[0][0]).reset_index(),on="user_id")
user_profile.rename(columns={'platform_name':'prefered_platform'},inplace=True)

#train["platform_family"]=pd.Series(train["platform_family"],dtype="category")
user_profile = pd.merge(user_profile,train[["platform_family","user_id"]].groupby("user_id").agg(lambda x: stats.mode(x)[0][0]).reset_index(),on="user_id")
user_profile.rename(columns={'platform_family':'prefered_family'},inplace=True)

#train["listen_type"]=pd.Series(train["listen_type"],dtype="category")
user_profile = pd.merge(user_profile,train[["listen_type","user_id"]].groupby("user_id").agg(lambda x: stats.mode(x)[0][0]).reset_index(),on="user_id")
user_profile.rename(columns={'listen_type':'prefered_listen_type'},inplace=True)

#train["context_type"]=pd.Series(train["context_type"],dtype="category")
user_profile = pd.merge(user_profile,train[["context_type","user_id"]].groupby("user_id").agg(lambda x: stats.mode(x)[0][0]).reset_index(),on="user_id")
user_profile.rename(columns={'context_type':'prefered_context_type'},inplace=True)

user_profile = pd.merge(user_profile,(train[["moment_listen","user_id"]].groupby(["user_id","moment_listen"]).size()/train[["moment_listen","user_id"]].groupby(["user_id"]).size()).unstack().reset_index(),on="user_id")

user_profile = pd.merge(user_profile,(train[["weekday_listen","user_id"]].groupby(["user_id","weekday_listen"]).size()/train[["weekday_listen","user_id"]].groupby(["user_id"]).size()).unstack().reset_index(),on="user_id")
user_profile["weekday"]=user_profile[0]+user_profile[1]+user_profile[2]+user_profile[3]+user_profile[4]
user_profile["weekend"]=user_profile[5]+user_profile[6]
user_profile.drop([0,1,2,3,4,5,6],axis=1,inplace=True)

#train["release_period"]=pd.Series(train["release_period"],dtype="category")
user_profile = pd.merge(user_profile,train[["release_period","user_id"]].groupby("user_id").apply(pd.DataFrame.mode),on="user_id")
user_profile.rename(columns={'release_period':'prefered_release_period'},inplace=True)

user_profile = pd.merge(user_profile,train[["is_listened","user_id"]].groupby("user_id").mean().reset_index(),on="user_id")
user_profile.rename(columns={'is_listened':'mean_is_listened'},inplace=True)

user_profile = pd.merge(user_profile,train[["recent_media","user_id"]].groupby("user_id").mean().reset_index(),on="user_id")
user_profile.rename(columns={'recent_media':'like_recent_media'},inplace=True)

user_profile = pd.merge(user_profile,train[["genre_id","user_id"]].groupby("user_id").max().reset_index(),on="user_id")
user_profile.rename(columns={'genre_id':'prefered_genre_id'},inplace=True)

user_profile = pd.merge(user_profile,((train[["album_id","user_id"]].groupby(["user_id"]).nunique()["album_id"])/train[["user_id"]].groupby("user_id").size()).reset_index(),on="user_id")
user_profile.rename(columns={0:'user_album_per_media'},inplace=True)

user_profile.to_csv("data/processed/user_profile.csv",index=False)
