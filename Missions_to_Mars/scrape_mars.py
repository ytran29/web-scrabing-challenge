from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd

def init_browser():
	executable_path = {"executable_path": "/Users/ytran/Downloads/chromedriver/chromedriver.exe"}
	return Browser("chrome", **executable_path, headless=False)

def scrape():
	browser = init_browser()
	
	news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&year=2020%3Apublish_date&category=19%2C165%2C184%2C204&blank_scope=Latest"
	browser.visit(news_url)
	html = browser.html
	soup = bs(html, "html.parser")
	News_Title = soup.find('div', class_='content_title').text.strip('\n')
	News_P = soup.find('div', class_='rollover_description_inner').text.strip('\n')

	image_url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(image_url)
	html = browser.html
	soup = bs(html, "html.parser")
	Mars_Image_url = image_url + soup.find('a', class_='button fancybox')["data-fancybox-href"]

	weather_url = "https://twitter.com/marswxreport?lang=en"
	headers = {'User-Agent': "Nokia5310XpressMusic_CMCC/2.0 (10.10) Profile/MIDP-2.1 'Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; 'Nokia5310XpressMusic) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile"}
	response = requests.get(weather_url, headers=headers)
	soup = bs(response.text, 'html.parser')
	mars_weather = soup.find_all('div',class_="dir-ltr")[2].text.strip('\n')

	Mars_facts_url = "https://space-facts.com/mars"
	browser.visit(Mars_facts_url)
	tables = pd.read_html(Mars_facts_url)
	Mars_facts = tables[0]
	Mars_facts.columns = ['Object', 'Measurement']
	Mars_facts.set_index('Object', inplace=True)
	Mars_facts_table = Mars_facts.to_html()
	Mars_facts_table.replace('\n', '')

	Hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(Hemispheres_url)
	html=browser.html
	soup = bs(html, "html.parser")
	Mars_hemisphere = []

	Hemispheres = soup.find_all("div", class_="item")
	for hemisphere in Hemispheres:
		title = hemisphere.find('h3').text
		link = hemisphere.find('a')['href']
		image_link = 'https://astrogeology.usgs.gov/' + link
		browser.visit(image_link)
		html = browser.html
		soup = bs(html, "html.parser")
		downloads = soup.find("div", class_="downloads")
		image_url = downloads.find("a")["href"]
		Mars_hemisphere.append({"title": title, "img_url": image_url})
	
	mars_data = {
		"News_Title": News_Title,
		"News_P": News_P,
		"Mars_Image_url": Mars_Image_url,
		"mars_weather": mars_weather,
		"Mars_facts_table": Mars_facts_table,
		"Mars_hemisphere": Mars_hemisphere
	}

	browser.quit()

	return mars_data



