import pandas as pd

learning = pd.read_csv("data/processed/learning.csv")
user_profile = pd.read_csv("data/inter/user_profile.csv")

learning_joined = learning.merge(user_profile,on="user_id")
learning_joined["is_prefered_genre_id"]=((learning_joined["prefered_genre_id"])==(learning_joined["genre_id"]))
learning_joined.drop("prefered_genre_id",axis=1,inplace=True)
learning_joined.drop("genre_id",axis=1,inplace=True)

from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()
label_encoder = label_encoder.fit(learning_joined["moment_listen"])
learning_joined["moment_listen"] = label_encoder.transform(learning_joined["moment_listen"])

learning_joined["is_prefered_release_period"]=((learning_joined["prefered_release_period"])==(learning_joined["release_period"]))
learning_joined.drop("prefered_release_period",axis=1,inplace=True)
learning_joined.drop("release_period",axis=1,inplace=True)

learning_joined.to_csv("data/processed/learning_join_user.csv")

import pandas as pd

learning_joined = pd.read_csv("data/processed/learning_join_user.csv")

import xgboost as xgb

model = xgb.sklearn.XGBRegressor(objective='binary:logistic')
model.fit(learning_joined,learning_joined["is_listened"])
