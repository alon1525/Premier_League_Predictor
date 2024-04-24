import pandas as pd
matches = pd.read_csv("Matches.csv", index_col=0)

matches["target"] = (matches["result"] == "W").astype("int")
matches["date"] = pd.to_datetime(matches["date"])
matches["venue_code"] = matches["venue"].astype("category").cat.codes
matches["opponent_code"] = matches["opponent"].astype("category").cat.codes
matches["hour"] = matches["time"].str.replace(":.+", "", regex=True).astype("int")
matches["day_code"] = matches["date"].dt.dayofweek

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100,min_samples_split= 10 ,random_state=1)
train = matches[matches["date"] < "2024-01-01"]#use this to train it
test = matches[matches["date"] > "2024-01-01"]#test it on this dates

predictors = ["venue_code", "opponent_code", "hour", "day_code"]
model.fit(train[predictors], train["target"])#traub the left based on predictors and predict the right
prediction = model.predict(test[predictors])