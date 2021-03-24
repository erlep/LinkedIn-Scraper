# LinkedIn-Scraper
# Stahne "Python Brno" z LinkedIn.com a ulozi do Xls
# dle predlohy: scrapeindeed - https://github.com/jhnwr/scrapeindeed
# https://www.linkedin.com/jobs/search/?distance=10&geoId=101164731&keywords=python&location=Brno%2C%2BSouth%2BMoravia%2C%2BCzechia&start=0
# https://www.linkedin.com/jobs/search/?distance=10&geoId=101164731&keywords=python&location=Brno%2C%20South%20Moravia%2C%20Czechia&redirect=false&position=1&pageNum=0&sortBy=DD
# strankovani je pomoci javascripu - url get nelze pouzit
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
  url = f'https://cz.indeed.com/jobs?q=python&l=brno&start={page}'
  if (page == 1):
    url = f'https://www.linkedin.com/jobs/search/?distance=10&geoId=101164731&keywords=python&location=Brno%2C%20South%20Moravia%2C%20Czechia&redirect=false&position=1&pageNum=0&sortBy=DD'
  else:
    url = f'https://www.linkedin.com/jobs/search/?distance=10&geoId=101164731&keywords=python&location=Brno%2C%2BSouth%2BMoravia%2C%2BCzechia&start=0'
  r = requests.get(url, headers)
  soup = BeautifulSoup(r.content, 'html.parser')
  return soup

def transform(soup):
  # divs = soup.find_all('li', class_='result-card job-result-card result-card--with-hover-state job-card__contents--active')
  divs = soup.find_all('li')
  for item in divs:
    # print(item)
    # print('\n\n')
    try:
      title = item.find('span', class_='screen-reader-text').text.strip()
    except:
      continue
    if (title == ''):
      continue
    try:
      company = item.find('h4').text.strip()
    except:
      company = ''
    try:
      salary = item.find('span', class_='job-result-card__salary-info').text.strip()
    except:
      salary = ''
    href = '' + item.find('a').get("href") + ''
    try:
      dtm = item.find('time', class_='job-result-card__listdate').text.strip()
    except:
      try:
        dtm = item.find('time', class_='job-result-card__listdate--new').text.strip()
      except:
        dtm = ''
    try:
      datum = item.find('time', {"class": "job-result-card__listdate", "datetime": True})['datetime']
    except:
      try:
        datum = item.find('time', {"class": "job-result-card__listdate--new", "datetime": True})['datetime']
      except:
        datum = ''
    # Datum 2021-03-02T01:44:18+01:00 - pryc "T" a  +01:00
    datum = datum.replace("+01:00", "").replace("T", "  ")
    # Job
    job = {
        'Title': title,
        'Company': company,
        'Salary': salary,
        'Kdy': dtm,
        'Date Add': datum,
        # 'item': item,
        'Link': href,
    }
    joblist.append(job)
  return


joblist = []

for i in range(1, 3, 1):
  #print(f'Getting page, {i}')
  c = extract(i)
  transform(c)

df = pd.DataFrame(joblist)
# df.drop_duplicates(inplace=True)
df.to_excel('zzLiPython-Brno.xlsx', index=False)
df.to_csv('zzLiPython-Brno.csv', index=False)

print('OkDone.')
