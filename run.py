import pandas as pd
import numpy as np
from analysis.magic_number_table import clean_data, wildcard, div_magic, wildcard_magic
from scrape.web_scrape import scrape_standings


#web_scrape:

path = "C:/Users/jgerhartz/projects/playoffs/static/csv/new.csv"
url = "https://www.baseball-reference.com/leagues/MLB/2019-playoff-odds.shtml"
driver_path = "C:/Users/jgerhartz/chromedriver.exe"


#resp = scrape_standings(url, driver_path, path)

def runner():

	data = pd.read_csv(path)

	magic = clean_data(data)

	al_wild_card = wildcard(magic,'AL')
	nl_wild_card = wildcard(magic, 'NL')


	merge1 = magic.merge(al_wild_card, how='left', on='Tm')
	merge2 = merge1.merge(nl_wild_card, how='left', on='Tm')


	#create div leader mn calculation instances
	ale_mn = div_magic(merge2, "ALE")
	alw_mn = div_magic(merge2, "ALW")
	alc_mn = div_magic(merge2, "ALC")
	nle_mn = div_magic(merge2, "NLE")
	nlw_mn = div_magic(merge2, "NLW")
	nlc_mn = div_magic(merge2, "NLC")

	#create wild card leaders mn calculation instances
	al_wc_mn = wildcard_magic(merge2, "AL")
	nl_wc_mn = wildcard_magic(merge2, "NL")


	#create list of divs with mns minus ale
	mns = [alw_mn, alc_mn, nle_mn, nlw_mn, nlc_mn, al_wc_mn, nl_wc_mn]

	#append div mns to one df
	mns_df = ale_mn.append(mns)

	merge3 = merge2.merge(mns_df, how='left', on='Tm')


	al_bool = merge3['Lg'] == "AL"
	al = merge3[al_bool]

	nl_bool = merge3['Lg'] == "NL"
	nl = merge3[nl_bool]

	return merge3

