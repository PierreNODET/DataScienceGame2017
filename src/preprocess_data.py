import pandas as pd
import numpy as np
from src.make_dir import cmd_folder

train = pd.read_csv(cmd_folder + "data/raw/train.csv")
test = pd.read_csv(cmd_folder + "data/raw/test.csv")

user_profile = pd.DataFrame(train.groupby("user_id").count().index)
user_profile = user_profile.merge(train[["user_id","user_age","user_gender"]].groupby("user_id").mean().reset_index(),on="user_id")
user_profile.to_csv(cmd_folder + "data/inter/user_profile.csv",index=False)

media_profile = pd.concat([train[["media_id","release_date","media_duration","genre_id"]].groupby("media_id").min().reset_index(),test[["media_id","release_date","media_duration","genre_id"]].groupby("media_id").min().reset_index()])
media_profile.drop_duplicates(inplace=True)
media_profile.to_csv(cmd_folder + "data/raw/media_profile.csv",index=False)

artist_profile = pd.DataFrame(pd.concat([train[["artist_id"]],test[["artist_id"]]]).drop_duplicates())
artist_profile.to_csv(cmd_folder + "data/raw/artist_profile.csv",index=False)

def preprocess_data(df):

    df.drop(["user_age","user_gender"],axis=1,inplace=True)
    df.drop(["release_date","media_duration","genre_id"],axis=1,inplace=True)
    df["date_listen"] = pd.to_datetime(df["ts_listen"],unit="s")

    df.loc[(df["date_listen"].dt.hour>=2) & (df["date_listen"].dt.hour<6),"moment_listen"]="night"
    df.loc[(df["date_listen"].dt.hour>=6) & (df["date_listen"].dt.hour<10),"moment_listen"]="morning"
    df.loc[(df["date_listen"].dt.hour>=10) & (df["date_listen"].dt.hour<18),"moment_listen"]="afternoon"
    df.loc[(df["date_listen"].dt.hour>=18) & (df["date_listen"].dt.hour<20),"moment_listen"]="late_afternoon"
    df.loc[(df["date_listen"].dt.hour>=20) | (df["date_listen"].dt.hour<2),"moment_listen"]="evening"

    df["weekday_listen"] = df["date_listen"].dt.weekday

    #Drop useless rows, that couldn't be deal by algorithms
    df.drop("ts_listen",axis=1,inplace=True)
    df.drop("date_listen",axis=1,inplace=True)

    return df

train = preprocess_data(train)
test = preprocess_data(test)

train.to_csv(cmd_folder + "data/inter/train.csv",index=False)
test.to_csv(cmd_folder + "data/inter/test.csv",index=False)
