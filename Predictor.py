import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score


def make_predictions(data,predictors):
    train = data[data["date"] < '2022-01-01']
    test = data[data["date"] > '2022-01-01']
    model.fit(train[predictors], train["target"])
    preds = model.predict(test[predictors])
    combined = pd.DataFrame(dict(actual=test["target"], predicted=preds), index=test.index)
    error = precision_score(test["target"], preds)
    return combined, error


def rolling_averages(group, cols, new_cols):
    group = group.sort_values("date")
    rolling_stats = group[cols].rolling(3, closed='left').mean()
    group[new_cols] = rolling_stats
    group = group.dropna(subset=new_cols)
    return group


matches = pd.read_csv("Matches.csv", index_col=0)

matches["target"] = (matches["result"] == "W").astype("int")
matches["date"] = pd.to_datetime(matches["date"])
matches["venue_code"] = matches["venue"].astype("category").cat.codes
matches["opponent_code"] = matches["opponent"].astype("category").cat.codes
matches["hour"] = matches["time"].str.replace(":.+", "", regex=True).astype("int")
matches["day_code"] = matches["date"].dt.dayofweek

model = RandomForestClassifier(n_estimators=200,min_samples_split= 30 ,random_state=1)
train = matches[matches["date"] < "2024-01-01"]  # use this to train it
test = matches[matches["date"] > "2024-01-01"]  # test it on this dates
predictors = ["venue_code", "opponent_code", "hour", "day_code"]

cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt","xg","xga","poss"]
new_cols = [f"{c}_rolling" for c in cols]
matches_rolling = matches.groupby("team").apply(lambda x: rolling_averages(x, cols, new_cols))
matches_rolling = matches_rolling.droplevel('team')
matches_rolling.index = range(matches_rolling.shape[0])

combined, error = make_predictions(matches_rolling, predictors + new_cols)
combined = combined.merge(matches_rolling[["date", "team", "opponent", "result"]], left_index=True, right_index=True)

class MissingDict(dict):
    __missing__ = lambda self, key: key

map_values = {"Brighton and Hove Albion": "Brighton", "Manchester United": "Manchester Utd", "Newcastle United": "Newcastle Utd", "Tottenham Hotspur": "Tottenham", "West Ham United": "West Ham", "Wolverhampton Wanderers": "Wolves"}
mapping = MissingDict(**map_values)
combined["new_team"] = combined["team"].map(mapping)
combined["new_team"] = combined["team"].map(mapping)
merged = combined.merge(combined, left_on=["date", "new_team"], right_on=["date", "opponent"])