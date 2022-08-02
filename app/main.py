import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

def localCopy():
  raw_text = ""
  script_dir = os.path.dirname(__file__)
  rel_path = f'development/draftkings_nfl.html'
  abs_file_path = os.path.join(script_dir, rel_path)
  with open(abs_file_path, 'r') as localFile:
    raw_text = localFile.read()
  return raw_text

def retrieveWebsite(website, mode):
  if mode == 'development':
    return localCopy()
  response = requests.get(website)
  return response.text

def save2Json(name, contents):
  with open(name, 'w') as saveFile:
    json.dump(contents, saveFile)
  
def executeRecipe(raw_text):
  # How to make this generic and agnostic and easy to build?
  data = []
  soup = BeautifulSoup(raw_text, "html.parser")
  tables = soup.find_all('table', {"class": "sportsbook-table"})
  for table in tables:
    # Game Date (useful for game matching)
    header = table.find('div', {"class": "sportsbook-table-header__title"})
    # Games for that Day
    rows = table.find('tbody').find_all('tr')
    for row in rows:
      event = row.find('th').find('a', {"class", "event-cell-link"})['href']
      name = row.find('div', {"class": "event-cell__name-text"})
      betInfo = row.find_all('td') # need to check if I get 3 tds back
      data.append({
        "date": header.text,
        "event": event,
        "team": name.text,
        'spread': betInfo[0].text,
        'total': betInfo[1].text,
        'moneyLine': betInfo[2].text
      })
  return data

def main():
  now = datetime.today().isoformat()
  mode = 'production'
  # read from some file url schema
  # scrape data -> match game ids with schedule
  website = "https://sportsbook.draftkings.com/leagues/football/nfl"
  raw_text = retrieveWebsite(website, mode)
  data = executeRecipe(raw_text)
  script_dir = os.path.dirname(__file__)
  rel_path = f'data/{now}.json'
  abs_file_path = os.path.join(script_dir, rel_path)
  # save file 
  save2Json(abs_file_path, data)

if __name__ == "__main__":
    main()
