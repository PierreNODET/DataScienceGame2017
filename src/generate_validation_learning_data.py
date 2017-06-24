import pandas as pd
from src.make_dir import cmd_folder

train = pd.read_csv(cmd_folder+"data/inter/train.csv")

def generate_learning_validation(df):

    df = train
    user_occurence = df[["user_id","media_id"]].groupby("user_id").count()
    user_occurence.rename(columns={'media_id':'occurence'},inplace=True)

    selected_id = user_occurence[user_occurence["occurence"]>1][["occurence"]].reset_index()

    selected_rows = train[train["listen_type"]==1].merge(selected_id,on="user_id").drop("occurence",axis=1)

    validation_rows = selected_rows.groupby("user_id").apply(lambda x: x.sample(n=1))

    learning_rows = selected_rows.drop(validation_rows.reset_index(level=1)["level_1"],axis=0)
    validation_rows = validation_rows.reset_index(level=1,drop=True)
    validation_rows = validation_rows.reset_index(drop=True)

    learning_rows = pd.concat([learning_rows,pd.get_dummies(learning_rows.context_type,prefix="context_type")[["context_type_1","context_type_5","context_type_20","context_type_23"]]],axis=1)
    learning_rows.drop(["context_type"],axis=1,inplace=True)

    learning_rows = pd.concat([learning_rows,pd.get_dummies(learning_rows.platform_family,prefix="platform_family")],axis=1)
    learning_rows.drop(["platform_family"],axis=1,inplace=True)

    learning_rows = pd.concat([learning_rows,pd.get_dummies(learning_rows.platform_name,prefix="platform_name")],axis=1)
    learning_rows.drop(["platform_name"],axis=1,inplace=True)

    validation_rows = pd.concat([validation_rows,pd.get_dummies(validation_rows.context_type,prefix="context_type")[["context_type_1","context_type_5","context_type_20","context_type_23"]]],axis=1)
    validation_rows.drop(["context_type"],axis=1,inplace=True)

    validation_rows = pd.concat([validation_rows,pd.get_dummies(validation_rows.platform_family,prefix="platform_family")],axis=1)
    validation_rows.drop(["platform_family"],axis=1,inplace=True)

    validation_rows = pd.concat([validation_rows,pd.get_dummies(validation_rows.platform_name,prefix="platform_name")],axis=1)
    validation_rows.drop(["platform_name"],axis=1,inplace=True)

    learning_rows = pd.concat([learning_rows,pd.get_dummies(learning_rows.weekday_listen,prefix="weekday_listen")],axis=1)
    learning_rows.drop(["weekday_listen"],axis=1,inplace=True)

    learning_rows = pd.concat([learning_rows,pd.get_dummies(learning_rows.moment_listen,prefix="moment_listen")],axis=1)
    learning_rows.drop(["moment_listen"],axis=1,inplace=True)

    validation_rows = pd.concat([validation_rows,pd.get_dummies(validation_rows.weekday_listen,prefix="weekday_listen")],axis=1)
    validation_rows.drop(["weekday_listen"],axis=1,inplace=True)

    validation_rows = pd.concat([validation_rows,pd.get_dummies(validation_rows.moment_listen,prefix="moment_listen")],axis=1)
    validation_rows.drop(["moment_listen"],axis=1,inplace=True)

    validation_rows.drop(["listen_type"],axis=1,inplace=True)
    learning_rows.drop(["listen_type"],axis=1,inplace=True)

    return(learning_rows,validation_rows)

(learning_rows,validation_rows) = generate_learning_validation(train)

learning_rows.to_csv("data/processed/learning.csv",index=False)
validation_rows.to_csv("data/processed/validation.csv",index=False)

test = pd.read_csv(cmd_folder+"data/inter/test.csv")

test = pd.concat([test,pd.get_dummies(test.context_type,prefix="context_type")[["context_type_1","context_type_5","context_type_20","context_type_23"]]],axis=1)
test.drop(["context_type"],axis=1,inplace=True)

test = pd.concat([test,pd.get_dummies(test.platform_family,prefix="platform_family")],axis=1)
test.drop(["platform_family"],axis=1,inplace=True)

test = pd.concat([test,pd.get_dummies(test.platform_name,prefix="platform_name")],axis=1)
test.drop(["platform_name"],axis=1,inplace=True)

test = pd.concat([test,pd.get_dummies(test.weekday_listen,prefix="weekday_listen")],axis=1)
test.drop(["weekday_listen"],axis=1,inplace=True)

test = pd.concat([test,pd.get_dummies(test.moment_listen,prefix="moment_listen")],axis=1)
test.drop(["moment_listen"],axis=1,inplace=True)

test.to_csv("data/processed/test.csv",index=False)
