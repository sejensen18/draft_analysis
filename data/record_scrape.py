from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv
import lxml

def get_page(BASE_URL):
	#pulls HTML and converts to soup
	html = urlopen(BASE_URL).read()
	soup = BeautifulSoup(html, "html.parser")
	return soup

def get_dropdown_values(soup, listname):
	#pulls the values of a dropdown
	val_list = []
	dropdown_vals = soup.findAll('select', attrs={'name': listname})

	if dropdown_vals:
	    for option in dropdown_vals[0].findAll('option'):
	        val_list.append(str(option.text))
	return val_list

def get_table(soup, year):
	#pulls tables from a page and stores as list of lists
	picks = []
	for e in soup.find_all('tr'):
		head = e.find_all('th')
		row = e.find_all('td')
		row_contents = []
		for g in head:
			row_contents.append(str(g.text).strip())
		for f in row:
			row_contents.append(str(f.text).strip())
		row_contents.append(str(year))
		if len(row_contents) > 12 and 'AP High' not in row_contents:
			picks.append(row_contents)
	return picks


year = 2016

while year > 1935:
	url = str('http://www.sports-reference.com/cfb/years/' + str(year) + '.html')
	soup = get_page(url)
	links = soup.select("a[href*=conferences]")

	clean_links = []
	for link in links:
		pot_link = str(link.get('href'))
		if str(year) in pot_link and pot_link not in clean_links:
			clean_links.append(str(pot_link))

	for link in clean_links:
		url = 'http://www.sports-reference.com' + link
		soup = get_page(url)
		wltable = get_table(soup, year)
		print url
		with open("record_output.csv", "a") as f:
		    writer = csv.writer(f)
		    writer.writerows(wltable)
	year = year - 1

