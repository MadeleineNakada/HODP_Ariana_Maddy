import urllib2
from bs4 import BeautifulSoup
import csv
import unicodedata

# link suffixes for all sports. Can modify for jsut one sport
sports = ['bsb', 'mbkb', 'mcrew-hw', 'mcrew-lw', 'mfencing', 'fball', 'mgolf',
    'mice', 'mlax', 'sailing', 'skiing', 'msoc', 'msquash', 'mswimdive', 'mten',
    'track', 'mvball', 'mwaterpolo', 'wrest', 'wbkb', 'wcrew-hw', 'wcrew-lw',
    'xc', 'wfencing', 'fh', 'wgolf', 'wlax', 'wrugby', 'wsoc', 'sball', 'wsquash',
    'wten', 'wvball', 'wwaterpolo','wswimdive', 'wice']

# get rid of non-unicode data to read into CSV
def fix(s):
    print s
    return unicodedata.normalize('NFKD', s).encode('ascii','ignore')

def main():
    get_year  = str(raw_input())
    players = []

    for sport in sports:
        # get sports page link
        quote_page = 'http://www.gocrimson.com/sports/'+sport + '/' + get_year + '/roster'
        page = urllib2.urlopen(quote_page)
        soup = BeautifulSoup(page, 'html.parser')
        player_soup = soup.find_all('td', attrs={'class': 'name'})
        links = []
        title = (soup.find('div', attrs={'id': 'wrapper'})).find('h1')
        sport = title.find('a').text
        # get player links
        for player in player_soup:
            link = player.find('a')
            if link.has_attr('href'):
                links.append('http://www.gocrimson.com' + link['href'])
        # scrape player info from each player page
        for link in links:
            player_url = urllib2.urlopen(link)
            player_data = BeautifulSoup(player_url, 'html.parser')
            player_info = player_data.find('div', attrs={'class': 'player-info'})
            player = {}
            name_box = player_info.find('span', attrs={'class': 'name'})
            player['name'] = fix(name_box.text.strip())
            player['sport'] = sport
            players.append(player)
            table_info = player_info.find('table')
            rows = table_info.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                label = cells[0].text.strip()
                label = label.strip(':')
                value = cells[1].text.strip()
                player[label] = fix(value)

    # output all to CSV
    with open(get_year + '.csv', 'w') as csvfile:
        fieldnames = ['sport','name', 'Year', 'Height', 'Weight', 'Hometown', 'High School','House Affiliation','Major', 'Position']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        for player in players:
            writer.writerow(player)

main()
