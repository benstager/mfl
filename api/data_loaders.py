import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

def scrape_NFL_REF_QB(player_name):

    first_name = player_name.split(' ')[0].lower()
    last_name = player_name.split(' ')[1].lower()
    player_url = f'https://www.sports-reference.com/cfb/players/{first_name}-{last_name}-1.html'
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
        for idx in range(2, 6):
            time.sleep(3)
            first_name = player_name.split(' ')[0].lower()
            last_name = player_name.split(' ')[1].lower()
            player_url = f'https://www.sports-reference.com/cfb/players/{first_name}-{last_name}-{idx}.html'
            html_content = requests.get(player_url).text
            
            soup = BeautifulSoup(html_content, 'html.parser')
            table = soup.find('table', {'id': 'passing_standard'})
            
            if not table:
                print(f"Passing stats table not found for {player_name}. Failed on index {idx}")
            else:
                print(f"Player found on index {idx}")
                break
    
    try:
        table.find_all('th')
        headers = [th.getText() for th in table.find_all('th')]
        yrs = [i for i in headers if ('2' in i) & (len(i) == 4 or len(i) == 5)]
        career_idx = headers.index(yrs[-1]) + 1
        baseline_headers = []
        headers = [th.getText() for th in table.find_all('th')]
        rows = []

        for tr in table.find_all('tr')[1:]:
            cells = [td.getText() for td in tr.find_all('td')]
            if cells: 
                rows.append(cells)

        career_stats = []

        for row in rows:
            if row.count('') == 2:
                career_stats.extend(row)
                break

        career_stats.remove('')
        career_stats.remove('')

        career_stats.append(len(yrs))
        career_stats.append(player_name)

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
        'college_seasons',
        'name'
        ]

        final = pd.DataFrame({name: [value] for name, value in zip(column_names, career_stats)})

        if len(career_stats) == len(column_names):
            final = pd.DataFrame({name: [value] for name, value in zip(column_names, career_stats)})
        else:
            print("Error: Number of stats does not match number of column names.")

        return final    
    except:
        print(f"FAILED: On {player_name}")