import pandas as pd

train = pd.read_csv("data/inter/train.csv")
test = pd.read_csv("data/inter/test.csv")

def generate_learning_validation(df):

    user_occurence = df[["user_id","media_id"]].groupby("user_id").count()
    user_occurence.rename(columns={'media_id':'occurence'},inplace=True)

    selected_id = user_occurence[user_occurence["occurence"]>1][["occurence"]].reset_index()

    selected_rows = train.merge(selected_id,on="user_id").drop("occurence",axis=1)

    validation_rows = selected_rows.groupby("user_id").apply(lambda x: x.sample(n=1))

    learning_rows = selected_rows.drop(validation_rows.reset_index(level=1)["level_1"],axis=0)
    validation_rows = validation_rows.reset_index(level=1,drop=True)

    return(learning_rows,validation_rows)

(learning_rows,validation_rows) = generate_learning_validation(train)

learning_rows.to_csv("data/processed/learning.csv",index=False)
validation_rows.to_csv("data/processed/validation.csv",index=False)
