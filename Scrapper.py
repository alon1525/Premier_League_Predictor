import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url = "https://fbref.com/en/comps/9/Premier-League-Stats"
# Send a GET request to the URL
response = requests.get(url)
# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')
mainTable = soup.find('table', {'id': 'results2023-202491_home_away'})

# Find the table with the class 'championship'
mainTablepd = pd.read_html(response.text, match="Regular season Table")  # getting the tables from the first page
rankingsTable = mainTablepd[0].iloc[:, 1:]
home_away_table = mainTablepd[1].iloc[:, 1:]
rankingsTable.head(20)
years = list(range(2024, 2020, -1))
all_matches = []
standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

for year in years:
    data = requests.get(standings_url)
    soup = BeautifulSoup(data.text)
    standings_table = soup.select('table.stats_table')[0]

    links = [link.get("href") for link in standings_table.find_all('a')]
    links = [link for link in links if '/squads/' in link]
    team_urls = [f"https://fbref.com{link}" for link in links]

    previous_season = soup.select("a.prev")[0].get("href")
    standings_url = f"https://fbref.com{previous_season}"

    for team_url in team_urls:
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        data = requests.get(team_url)
        print(team_name, year)
        matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
        soup = BeautifulSoup(data.text)
        links = [link.get("href") for link in soup.find_all('a')]
        links = [link for link in links if link and 'all_comps/shooting/' in link]
        data = requests.get(f"https://fbref.com{links[0]}")
        try:
            shooting = pd.read_html(data.text, match="Shooting")[0]
            shooting.columns = shooting.columns.droplevel()
            team_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
        except ValueError:
            continue
        links = soup.find_all('a')
        links = [link.get("href") for link in links]
        links = [link for link in links if link and 'all_comps/passing_types/' in link]
        data = requests.get(f"https://fbref.com{links[0]}")
        try:
            Passing = pd.read_html(data.text, match="Pass Types")[0]
            Passing.columns = Passing.columns.droplevel()  # removing the upper text
            team_data = team_data.merge(Passing[["Date", "CK"]],
                                        on="Date")  # merging the Corners and the team stats tables
        except ValueError:
            continue
        team_data = team_data[team_data["Comp"] == "Premier League"]

        team_data["Season"] = year
        team_data["Team"] = team_name
        all_matches.append(team_data)
        time.sleep(6)
# Testing if it's alright
assert len(all_matches) == len(years) * 20
# combine all games together
all_matches = pd.concat(all_matches)
all_matches.columns = [c.lower() for c in all_matches.columns]
all_matches.to_csv("Matches.csv")

