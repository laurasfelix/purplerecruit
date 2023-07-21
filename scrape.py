import json
from urllib.request import urlopen
def scrape(file):
    data = json.loads(file)
    data = data["value"]
    list_clubs = []
    for i in data:
            if i["Name"] not in list_clubs:
                list_clubs.append(i["Name"])
    return list_clubs

def open_site():
    response = urlopen('https://northwestern.campuslabs.com/engage/api/discovery/search/organizations?orderBy%5B0%5D=UpperName%20asc&top=700&filter=&query=&skip=0')
    file = response.read()
    return scrape(file)
                        
