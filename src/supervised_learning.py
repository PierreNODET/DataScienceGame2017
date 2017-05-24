import pandas as pd

learning = pd.read_csv("data/processed/learning.csv")
user_profile = pd.read_csv("data/inter/user_profile.csv")

learning_joined = learning.merge(user_profile,on="user_id")
learning_joined.drop("Unnamed: 0",axis=1,inplace=True)
learning_joined.drop("ts_listen",axis=1,inplace=True)
learning_joined["is_prefered_genre_id"]=((learning_joined["prefered_genre_id"])==(learning_joined["genre_id"]))
learning_joined.drop("prefered_genre_id",axis=1,inplace=True)
learning_joined.drop("genre_id",axis=1,inplace=True)
learning_joined.drop("release_date",axis=1,inplace=True)
learning_joined["moment_listen"]=pd.to_datetime(learning_joined["date_listen"]).dt.hour
learning_joined.drop("date_listen",axis=1,inplace=True)
learning_joined["is_prefered_release_period"]=((learning_joined["prefered_release_period"])==(learning_joined["release_period"]))
learning_joined.drop("prefered_release_period",axis=1,inplace=True)
learning_joined.drop("release_period",axis=1,inplace=True)

import sys
sys.getsizeof(learning_joined)

import xgboost as xgb

model = xgb.sklearn.XGBRegressor(objective='binary:logistic')
model.fit(learning_joined,"is_listened")
