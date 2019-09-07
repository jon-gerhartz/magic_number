from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By


def scrape_standings(url, driver_path, csv_path):
	driver = webdriver.Chrome(driver_path)
	driver.get(url)
	actions = ActionChains(driver)

	waiter = driver.implicitly_wait(30)

	#find share menu element on page
	menu = driver.find_element_by_xpath("//*[@id='all_playoff_prob_mlb']/div[1]/div/ul/li[2]")

	#find csv element within share menu
	csv_element = driver.find_element_by_xpath("//*[@id='all_playoff_prob_mlb']/div[1]/div/ul/li[2]/div/ul/li[4]/button")

	#waiter = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='all_playoff_prob_mlb']/div[1]/div/ul/li[2]/div/ul/li[4]/button")))
	#find hide rows element on page
	hide_rows = driver.find_element_by_xpath("//*[@id='playoff_prob_mlb_toggle_partial_table']")


	#try hide_rows one time to get it to work
	try:
		hide_rows.click()

	except:
		pass

	#click hide rows button
	hide_rows.click()

	#hover over menu, hover over csv, click
	actions.move_to_element(menu).move_to_element(csv_element).click().perform()

	#get table element
	table = driver.find_element_by_xpath("//*[@id='csv_playoff_prob_mlb']")

	#get table data in text
	data = table.text

	#open new csv file
	with open(csv_path, "w") as f:

		#write table data to csv
		f.write(data)
		#close file
		f.close()

	#quit and close driver
	driver.quit()

	status = "done"

	return status

