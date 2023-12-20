# import module
import requests
from bs4 import BeautifulSoup
# from URL

# UDF for get HTML cod
def get_html(Airline_code, Flight_number, Date, Month, Year):
	def getdata(url):
		r = requests.get(url)
		return r.text

	# url
	url = "https://www.flightstats.com/v2/flight-tracker/"+Airline_code + \
		"/"+Flight_number+"?year="+Year+"&month="+Month+"&date="+Date

	# pass the url
	# into getdata function
	htmldata = getdata(url)
	soup = BeautifulSoup(htmldata, 'html.parser')
	return(soup)

# Get Flight number
# from Html code


def flight_no(soup):
	Flight_no = ""

	# Find div tag with
	# unique class name
	for i in soup.find("div", class_="ticket__FlightNumberContainer-s1rrbl5o-4 hgbvHg"):
		Flight_no = Flight_no + (i.get_text()) + " "
	return (Flight_no)

# Get Airport name
# from HTML code


def airport(soup):
	Airport_name = []
	# Find div tag with
	# unique class name
	for i in soup.find_all("div", class_="text-helper__TextHelper-s8bko4a-0 CPamx"):
		Airport_name.append(i.get_text())
	return (Airport_name)

# get status
# from HTML code


def status(soup, Airport_list):
	Time_status = []
	Airport_List = []
	Status_str = []
	Gate = []
	Gate_no = []

	# Find div tag with
	# unique class name
	# to get Gate number
	for data in soup.find_all("div", class_="ticket__TGBLabel-s1rrbl5o-15 gcbyEH text-helper__TextHelper-s8bko4a-0 dfeqpK"):
		Gate.append(data.get_text())
	for data in soup.find_all("div", class_="ticket__TGBValue-s1rrbl5o-16 icyRae text-helper__TextHelper-s8bko4a-0 cCfBRT"):
		Gate_no.append(data.get_text())

	# Get status from
	# html code
	for i in soup.find_all("div", class_="text-helper__TextHelper-s8bko4a-0 bcmzUJ"):
		Status_str.append(i.get_text())
	for i in soup.find_all("div", class_="text-helper__TextHelper-s8bko4a-0 cCfBRT"):
		Time_status.append(i.get_text())

	# traverse the Data
	# from scraping data
	for item in range(4):
		if item == 0:
			print(Airport_list[0])
		if item == 2:
			print("")
			print(Airport_list[1])
		print(Status_str[item] + " : " + Time_status[item])
		print(Gate[item] + " : " + Gate_no[item])
	for item in range(len(Gate)):
		print(Gate[item] + " : " + Gate_no[item])


# Driver code
if __name__ == '__main__':
	# Input Data from geek
	Airline_code = 'G8'
	Flight_number = '134'
	Date = '23'
	Month = '10'
	Year = '2022'

	# Calling the get_html
	# with argument
	# function calling
	soup = get_html(Airline_code, Flight_number, Date, Month, Year)
	print("Flight number : ", flight_no(soup))
	Airport_list = airport(soup)
	status(soup, Airport_list)

