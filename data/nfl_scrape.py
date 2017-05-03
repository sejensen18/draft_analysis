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

def get_table(soup):
	#pulls tables from a page and stores as list of lists
	picks = []
	for e in soup.find_all('tr'):
		head = e.find_all('th')
		row = e.find_all('td')
		row_contents = []
		if len(row) == 0:
			row = head
		for f in row:
			row_contents.append(str(f.text).strip())
		picks.append(row_contents)
	return picks

seed_url = 'http://www.nfl.com/draft/history/fulldraft?season=2014&round=round1'
soup = get_page(seed_url) #first page
draft_years = get_dropdown_values(soup, 'season') #get all possible draft years
draft_picks = [] #initialize empty list

#loop through each draft year pulling data
for year in draft_years:
	print 'Retrieving draft year: ' + year
	url = 'http://www.nfl.com/draft/history/fulldraft?season=' + year + '&round=round1'
	soup = get_page(url)
	draft_picks_raw = get_table(soup)
	
	#clean the data
	for e in draft_picks_raw:
		if e[0].isdigit():
			e.append(year)
			draft_picks.append(e)

#write to csv
with open("output.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(draft_picks)

