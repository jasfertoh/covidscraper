from bs4 import BeautifulSoup as bs
import requests

r = requests.get('https://keithgalli.github.io/web-scraping/webpage.html')

soup = bs(r.content, "html.parser")

# socials = soup.select('ul.socials a')

# for social in socials:
#     print(social['href'])

# socials = soup.find('ul', attrs={"class": "socials"}).find_all("a")
# for social in socials:
#     print(social['href'])\

# fun facts
# import re
# facts = soup.select('ul.fun-facts li')
# for fact in facts: 
#     if fact.find(string=re.compile('is')) != 'None':
#         print(fact.get_text())

links = soup.select('div.block ul li a')
links = [link['href'] for link in links]
print(links)

for link in links:
    url = link
    r = requests.get('https://keithgalli.github.io/web-scraping/' + url)
    soup = bs(r.content, "html.parser")
    message = soup.find('p', attrs={"id": "secret-word"})
    print(message.get_text())

