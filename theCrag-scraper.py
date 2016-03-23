from bs4 import BeautifulSoup
import urllib2
import requests
import re
import tablib

#Global Variables

#Tablib DataSet
data = tablib.Dataset()
data.headers = ("Region of World", "Country","State", "Name", "Type", "Grade")

#Request using beautiful soup
def request_url(url):
	url = "http://www.thecrag.com" + url
	user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT"
	headers = { "User-Agent" : user_agent}

	try:
		#make request
		req = urllib2.Request(url, headers=headers)
		res = urllib2.urlopen(req)
	except:
		raise
	else:
		soup = BeautifulSoup(res.read(), "html.parser")
		res.close()
		return soup
	
def scrape_thecrag(world):
	
	#requests world url ending
	url_ending = "/climbing/"+world

	soup = request_url(url_ending)

	#TODO Recursive function (soup)
	scrape_areas(soup)

#Recursive function to get the areas and routes
def scrape_areas(soup):
	if soup is not None:
		if soup.find("div", {"class" : "node-listview"}).find("h2", {"class" : "inline"}).renderContents().strip() != None:

			area_route = soup.find("div", {"class" : "node-listview"}).find("h2", {"class" : "inline"}).renderContents().strip()
			# Areas
			if area_route == "Areas":
				areas = soup.find("div", {"class" : "node-listview"}).findAll(lambda tag: tag.name == 'div' and tag.get('class') == ['area'])
				for area in areas:
					climbs = area.find("div", {"class" : "stats"}).find("div", {"class" : "routes"})
					for climb in climbs:
						climb = climb.replace(',', '')
						if 'k' not in climb:
							if float(climb) > 0:
								class_names = area.find("div", {"class" : "name"})
								anchor = class_names.find('a')
								if anchor is not None:
									new_soup = request_url(anchor['href'])
									scrape_areas(new_soup)
						else:
							climb = climb[:-1]
							if float(climb) > 0:
								class_names = area.find("div", {"class" : "name"})
								anchor = class_names.find('a')
								if anchor is not None:
									new_soup = request_url(anchor['href'])
									scrape_areas(new_soup)
			# Routes
			if area_route == "Routes":
				#gets world/state
				region = soup.find("div",{"id" : "breadCrumbs"}).find('ul').findAll('li')
				world = region[1].find('a').find("span").renderContents().strip()
				country = region[2].find('a').find("span").renderContents().strip()
				if region[3] is not None:
					state = region[3].find('a').find("span").renderContents().strip()
				#get routes
				routes = soup.find("div", {"class" : "node-listview"}).findAll(lambda tag: tag.name == 'div' and tag.get('class') == ['route'])
				for route in routes:
					[s.extract() for s in route('img')]
					extract_info(route, world, country, state)
					
				with open('/Users/tbhall/Documents/MyProjects/Social/scraper/Database_Routes_World.csv', 'wb') as f:
					f.write(data.csv)

#extracts the name of route, type of route, and the grade
def extract_info(route, world, country, state):
	name = route.find("div", {"class" : "title"}).find("span",{"class" : "name"}).find('a').renderContents().strip()
	type_climb = route.find("div", {"class" : "title"}).find("span",{"class" : "flags"}).find('span').renderContents().strip()
	grade = route.find("div", {"class" : "title"}).find("span",{"class" : "r-grade"}).find('span').renderContents().strip()
	route_append(world, country, state, name, type_climb, grade)

#appends to the data
def route_append(world, country, state,name, type_climb, grade):
	data.append((world, country, state, name, type_climb, grade))

#Execuation
World_Places = ["north-america"]#"australia", "new-zealand", "pacific-islands", "europe", "north-america", "central-america", "south-america", "africa", "asia", "middle-east","artic-region", "antarctica"]
for places in World_Places:
	scrape_thecrag(places)
with open('/Users/tbhall/Documents/MyProjects/Social/scraper/Database_Routes_World.csv', 'wb') as f:
			f.write(data.csv)












