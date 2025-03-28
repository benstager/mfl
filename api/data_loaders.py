import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

def load_qb_data_cleaned():
    return pd.read_csv("../data/for_modeling.csv")

def scrape_NFL_REF_QB(player_name):

    first_name = player_name.split(' ')[0].lower()
    last_name = player_name.split(' ')[1].lower()
    player_url = f'https://www.sports-reference.com/cfb/players/{first_name}-{last_name}-1.html'
    html_content = requests.get(player_url).text
    
    if player_name == 'Zach Wilson':
        first_name = player_name.split(' ')[0].lower()
        last_name = player_name.split(' ')[1].lower()
        player_url = f'https://www.sports-reference.com/cfb/players/{first_name}-{last_name}-3.html'
        html_content = requests.get(player_url).text
        
    if player_name == 'Justin Fields' or player_name == 'Jordan Love':
        first_name = player_name.split(' ')[0].lower()
        last_name = player_name.split(' ')[1].lower()
        player_url = f'https://www.sports-reference.com/cfb/players/{first_name}-{last_name}-2.html'
        html_content = requests.get(player_url).text
    
    if player_name == 'Daniel Jones':
        first_name = player_name.split(' ')[0].lower()
        last_name = player_name.split(' ')[1].lower()
        player_url = f'https://www.sports-reference.com/cfb/players/{first_name}-{last_name}-4.html'
        html_content = requests.get(player_url).text
    
    if player_name == 'Josh Allen':
        first_name = player_name.split(' ')[0].lower()
        last_name = player_name.split(' ')[1].lower()
        player_url = f'https://www.sports-reference.com/cfb/players/{first_name}-{last_name}-7.html'
        html_content = requests.get(player_url).text

    if player_name == 'Mitchell Trubisky':
        first_name = player_name.split(' ')[0].lower()
        first_name = 'Mitch'
        last_name = player_name.split(' ')[1].lower()
        player_url = 'https://www.sports-reference.com/cfb/players/mitch-trubisky-1.html'
        html_content = requests.get(player_url).text

    if len(player_name.split(' ')) > 2:
        first_name = player_name.split(' ')[0].lower()
        last_name = player_name.split(' ')[1].lower()
        suffix = player_name.split(' ')[2].lower()
        player_url = f'https://www.sports-reference.com/cfb/players/{first_name}-{last_name}-{suffix}-1.html'
        html_content = requests.get(player_url).text
    
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'passing_standard'})
    
    if not table:
        print("Passing stats table not found")
        return None

    baseline_headers = []
    headers = [th.getText() for th in table.find_all('th')]
    rows = []
    
    for tr in table.find_all('tr')[1:]:
        cells = [td.getText() for td in tr.find_all('td')]
        if cells: 
            rows.append(cells)
    
    yr_college = len(rows) - 1

    column_names = [
    'G',        
    'Cmp',      
    'Att',      
    'Cmp%',     
    'Yds',      
    'TD',       
    'TD%',      
    'Int',      
    'Int%',     
    'Y/A',      
    'AY/A',     
    'Y/C',      
    'Y/G',      
    'Rate',
    'seasons',
    'name'
    ]
    
    totals = rows[len(rows)-1]
    totals = [stat for stat in totals if stat.strip()]
    totals.append(yr_college)
    totals.append(player_name)

    if len(totals) == len(column_names):
        final = pd.DataFrame({name: [value] for name, value in zip(column_names, totals)})
    else:
        print("Error: Number of stats does not match number of column names.")

    return final