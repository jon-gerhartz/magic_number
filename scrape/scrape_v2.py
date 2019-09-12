from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.baseball-reference.com/leagues/MLB/2019-playoff-odds.shtml"

def scrape(path):
	res = requests.get(path)
	soup = BeautifulSoup(res.content,'lxml')
	table = soup.find_all('table')[1] 
	df = pd.read_html(str(table))
	df = df[0]
	return df

df = scrape(url)

df.to_csv("C:/Users/jgerhartz/projects/playoffs/static/csv/new.csv")

print("new.csv saved to path")