from bs4 import BeautifulSoup as bs
from helium import *
import json

url = 'https://www.moh.gov.sg/covid-19'
browser = start_chrome(url, headless=True)
soup = bs(browser.page_source, "html.parser")

message = soup.find('div', attrs={"class": "sfContentBlock"}).find_next_sibling().select('h3 strong span')[0].get_text()
message = message.replace(u'\xa0', u' ')
message = message.replace('</br>', '')
print(message)

cases = soup.find('tr', string="IMPORTED").find_next_sibling()
total_imported_cases = cases.select('td span strong span')
total = total_imported_cases[0].get_text()
increase = total_imported_cases[1].get_text()
total = total.replace(u'\xa0', u'')
print(total, increase)

summary = soup.find('div', attrs={"class": "sfContentBlock"}).find_next_sibling().find_next_sibling().select('h3 strong span')[0].get_text()
print(summary)

active_cases = soup.find('div', attrs={"class": "sfContentBlock"}).find_next_sibling().find_next_sibling().find_next_sibling().select('div table tbody tr td font b')[1].get_text()
print(active_cases)

data = {
    "total": total,
    "increase": increase,
    "summary": summary,
    "active_cases": active_cases
}

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)

file = open('index.html', 'w')
file.write(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Covid 19 Stats in Singapore</title>
    <link href="style.css" rel="stylesheet">
</head>
<body>
    <table>
        <tbody>
            <tr>
                <td>{message}</td>
                <td>Increase</td>
            </tr>
            <tr>
                <td>{total}</td>
                <td>{increase}</td>
            </tr>
        </tbody>
    </table>
</body>
</html>''')

browser.close()