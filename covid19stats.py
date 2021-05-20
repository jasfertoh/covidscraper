from bs4 import BeautifulSoup as bs
from helium import *
import re
import json

url = 'https://www.worldometers.info/coronavirus/'
browser = start_chrome(url, headless=True)
soup = bs(browser.page_source, 'html.parser')
helium.scroll_down(num_pixels = 4000)
helium.click('Country')
countries = []
file = open('newdata.txt', 'r')
lines = file.readlines()
for line in lines:
    newlist = line.replace("\n", "")
    countries.append(newlist)
file.close()

newdata = soup.find_all('tr', attrs={"role": "row"})

stats = []
for data in newdata:
    stats.append(data.find_all('td'))
update = []
for i in range(len(stats)):
    if i in {1,2,3,4,6,12,110,195}:
        pass
    else:
        if stats[i] not in update:
            update.append(stats[i])
update = update[1:223]
data = {}
for i in range(len(update)):
    if '\n\n' in update[i][1].get_text():
        update[i][1].get_text().replace('\n', '')
    else:
        data[f'{update[i][1].get_text()}'] = []
        data[f'{update[i][1].get_text()}'].append({
            'totalcases': update[i][2].get_text(),
            'newcases': update[i][3].get_text(),
            'totaldeaths': update[i][4].get_text(),
            'newdeaths': update[i][5].get_text(),
            'totalrecovered': update[i][6].get_text()
        })
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)

helium.kill_browser()