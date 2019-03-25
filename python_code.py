import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
wiki_link = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
page = requests.get(wiki_link).text
soup = BeautifulSoup(page, 'html5lib')
table = soup.find('table', class_='wikitable')
row = []
for tr in table.find_all('tr'):
	td = tr.find_all('td')
	row.append([tr.text.strip() for tr in td if tr.text.strip()])
df = pd.DataFrame(data=row, columns=['PostalCode', 'Borough', 'Neighborhood'])
df = df.drop([0])
df = df[df.Borough != 'Not assigned']
df = df.groupby(['PostalCode','Borough'])['Neighborhood'].apply(','.join).reset_index()
df.loc[df.Neighborhood == 'Not assigned', 'Neighborhood'] = df.Borough
df.shape
df.head(10)
geo_data = pd.read_csv('http://cocl.us/Geospatial_data')
geo_data.head(10)
geo_data.rename(columns={'Postal Code':'PostalCode'}, inplace=True)
geo_data.head(10)
df = pd.merge(df, geo_data, how='left', on='PostalCode')
df.head(10)