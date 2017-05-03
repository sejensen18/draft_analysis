from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv
import lxml

def get_raw_page(BASE_URL):
	html = urlopen(BASE_URL).read()
	soup = BeautifulSoup(html, "html.parser")
	return html

def get_page(BASE_URL):
	html = urlopen(BASE_URL).read()
	soup = BeautifulSoup(html, "html.parser")
	return soup

def get_dropdown_values(soup, listname):
	val_list = []
	dropdown_vals = soup.findAll('select', attrs={'name': listname})

	if dropdown_vals:
	    for option in dropdown_vals[0].findAll('option'):
	        val_list.append(str(option.text))
	return val_list

def get_table_values(soup, listname):
	val_list = []
	dropdown_vals = soup.findAll('div', attrs={'class': listname})
	return dropdown_vals

def get_score_table(soup):
	score = []
	for e in soup.find_all('tr'):
		head = e.find_all('th')
		row = e.find_all('td')
		row_contents = []
		if len(row) == 0:
			row = head
		for f in row:
			row_contents.append(str(f.text).strip())
		score.append(row_contents)
	return score

	# if dropdown_vals:
	#     for option in dropdown_vals[0].findAll('option'):
	#         val_list.append(str(option.text))
	# return val_list


seed_url = 'http://www.nfl.com/draft/history/fulldraft?season=2014&round=round1'

soup = get_page(seed_url)

draft_years = get_dropdown_values(soup, 'season')
draft_picks = []

for year in draft_years:
	print 'Retrieving draft year: ' + year
	url = 'http://www.nfl.com/draft/history/fulldraft?season=' + year + '&round=round1'
	soup = get_page(url)
	draft_picks_raw = get_score_table(soup)
	
	for e in draft_picks_raw:
		if e[0].isdigit():
			e.append(year)
			draft_picks.append(e)

with open("output.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(draft_picks)

# print draft_years
# print rounds
# print picks

# <div class="draft-history-table">


# <select name="season">
# <option value="2017">2017</option>
# <option selected="selected" value="2016">2016</option>
# <option value="2015">2015</option>
# <option value="2014">2014</option>

# <select name="round">
# <option value="round1">Round 1</option>
# <option value="round2">Round 2</option>