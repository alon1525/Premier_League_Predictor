README
Overview
This project involves scraping Premier League data from the FBref website and using it to build a predictive model for match outcomes using a Random Forest classifier. The model predicts match results based on various features, including historical performance metrics and match-specific details.

Files
1. predictive_model.py
This file contains the code to preprocess the data, build the predictive model, and make predictions on match outcomes. The main steps include:

Data Loading and Preprocessing:
Load match data from a CSV file.
Create target variable indicating whether the match was won (1) or not (0).
Encode categorical variables such as venue and opponent.
Extract additional features like the hour of the match and the day of the week.
Compute rolling averages for various performance metrics (goals, shots, expected goals, etc.) over the last 3 matches.
Model Training and Prediction:
Split the data into training and test sets based on the date.
Train a Random Forest classifier using the training data.
Make predictions on the test set.
Calculate the precision score to evaluate the model's performance.
Combine predictions with actual results for comparison.
2. data_scraping.py
This file handles the web scraping of Premier League data from the FBref website. The main steps include:

Web Scraping:
Send requests to the FBref website to retrieve HTML content.
Parse the HTML content using BeautifulSoup to extract relevant tables.
Retrieve and process team-specific data for each season, including match results, shooting statistics, and passing types.
Data Aggregation:
Combine data from multiple seasons and teams into a single DataFrame.
Save the aggregated data to a CSV file for use in the predictive model.

Data Explanation
The data used in this project includes various performance metrics for Premier League matches. Key features include:

gf: Goals For
ga: Goals Against
sh: Shots
sot: Shots on Target
dist: Average Shot Distance
fk: Free Kicks
pk: Penalty Kicks
pkatt: Penalty Kick Attempts
xg: Expected Goals
xga: Expected Goals Against
poss: Possession Percentage

These features are used to compute rolling averages, which serve as inputs to the predictive model.

Conclusion
This project demonstrates how to scrape sports data, preprocess it, and build a machine learning model to make predictions. The resulting model can help in understanding and predicting match outcomes in the Premier League based on various performance metrics.
