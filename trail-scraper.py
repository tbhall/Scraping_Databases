from bs4 import BeautifulSoup
import urllib2
import requests
import re
import tablib
#Global Variables
#Using tablib creates a mini database of sorts
data = tablib.Dataset()
data.headers = ('Name','Location', 'State(s)', 'Counties', 'Type', 'Length', 'Uses')
#Main trail database
def scrape_national_trail_database():
	# construct url for request
	#Test of 15 trails
	#url = "http://www.americantrails.org/NRTDatabase/trailList.php?usrSortOrder=TrailName&maxRows_rsTrails=15&usrTrailName=&usrTrailState=&usrTrailUse=&usrTrailCounty=&usrTrailUse2=&usrAgency=&usrYearDesignated=&usrTrailLength=0&usrTrailQuery=&usrTrailType="
	
	url = "http://www.americantrails.org/NRTDatabase/trailList.php?usrSortOrder=TrailName&maxRows_rsTrails=15000&usrTrailName=&usrTrailState=&usrTrailUse=&usrTrailCounty=&usrTrailUse2=&usrAgency=&usrYearDesignated=&usrTrailLength=0&usrTrailQuery=&usrTrailType="
	user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
	headers = { "User-Agent" : user_agent }

	try:
		# make request
		req = urllib2.Request(url, headers=headers)
		res = urllib2.urlopen(req)
	except:
		raise
	else:
		soup = BeautifulSoup(res.read(), "html.parser")

		res.close()

		#parses the trails all over the US
		#First Half 
		trails = soup.findAll("div", {"style" : "width:740px;float:left; background:#f0f8e2; padding: 10px 30px;"})
		for trail in trails:

			#Takes the "p" with the anchor to find trail url
			bodyTrail = trail.findAll("p")

			for body in bodyTrail:
				anchor = body.find("a", {"class" : "boldBlue"})
				if anchor is None:
					#this is the Trail info url ending.
					continue
				else:
					scrape_trail_info_americantrails(anchor["href"])

		#Second Half
		trails = soup.findAll("div", {"style" : "width:740px;float:left;  padding: 10px 30px;"})
		for trail in trails:

			#Takes the "p" with the anchor to find trail url
			bodyTrail = trail.findAll("p")

			for body in bodyTrail:
				anchor = body.find("a", {"class" : "boldBlue"})
				if anchor is None:
					#this is the Trail info url ending.
					continue
				else:
					scrape_trail_info_americantrails(anchor["href"])
    				
		with open('/Users/tbhall/Documents/MyProjects/Social/scraper/Database_Trails_US.csv', 'wb') as f:
			f.write(data.csv)

#Information on  each trail
def scrape_trail_info_americantrails(html):
	user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
	headers = { "User-Agent" : user_agent }

	try:
		# make request
		html = "http://www.americantrails.org/NRTDatabase/" + html
		req = urllib2.Request(html, headers=headers)
		res = urllib2.urlopen(req)
	except:
		raise
	else:
		soup = BeautifulSoup(res.read(), "html.parser")

		res.close()
		#extract info data
		trail_head = soup.find("div", {"id" : "innerContent"}).find('h1')
		trail_table = soup.find("div", {"id": "innerContent"}).table.findAll('tr')
		trail_head = trail_head.renderContents().strip()
		
		#Adds New trail to payload
		create_payload(trail_table, trail_head)
		
def create_payload(row, trail_head):
	#Takes each row to begin the parse
	location = row[0].findAll('td')
	states = row[1].findAll('td')
	counties = row[2].findAll('td')
	trail_type = row[3].findAll('td')
	length = row[4].findAll('td')
	uses = row[5].findAll('td')

	#gets the data out of td
	location = location[1].renderContents().strip()
	states = states[1].renderContents().strip()
	counties = counties[1].renderContents().strip()
	trail_type = trail_type[1].renderContents().strip()
	trail_type = trail_type.replace("<br>", ' ').replace("<br/>", ' ').replace("</br>", ' ').split()
	#Takes out the blank fields
	while '' in trail_type:
		trail_type.remove('')
	length = length[1].renderContents().strip()
	uses = uses[1].renderContents().strip()
	uses = uses.replace("<br>", '$').replace("<br/>", '$').replace("</br>", '$').split('$')
	#Takes out the blank fields
	while '' in uses:
		uses.remove('')
	#appends new trail
	trail_append(trail_head, location, states, counties, trail_type, length, uses)

#appends a trail to global data
def trail_append(name, location, state, counties, trail_type, length, uses):
	data.append((name, location, state, counties, trail_type, length, uses))
	



	
#Call the function
scrape_national_trail_database()



