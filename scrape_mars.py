# DEPENDENCIES
from bs4 import BeautifulSoup 
from splinter import Browser
import requests
import pandas as pd

def init_browser():
	executable_path = {"executable_path": "chromedriver"}
	return Browser("chrome", **executable_path, headless=False)

def scrape():
	browser = init_browser()

	mars_update = {}

	# NASA MARS NEWS
	url = 'https://mars.nasa.gov/news/'
	browser.visit(url)

	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')

	recent = soup.find('div', class_='list_text')
	news_title = recent.find('div', class_='content_title').text
	news_p = recent.find('div', class_='article_teaser_body').text

	mars_update['news_title'] = news_title
	mars_update['news_p'] = news_p



	# JPL MARS IMAGE
	url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(url_jpl)

	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')

	img_find = soup.find('footer')
	img = img_find.find('a', class_='button fancybox')['data-fancybox-href']
	img_url = "https://jpl.nasa.gov" + img
	featured_image_url = img_url

	mars_update['featured_image_url'] = featured_image_url



	# MARS WEATHER
	url_tweet = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(url_tweet)

	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')

	tweet_box = soup.find('div', class_='js-tweet-text-container')
	tweet = tweet_box.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
	mars_weather = tweet

	mars_update['mars_weather'] = mars_weather



	# MARS FACTS
	url_facts = 'https://space-facts.com/mars/'
	browser.visit(url_facts)

	mars_table = pd.read_html(url_facts)
	mars_df = mars_table[0]
	mars_df.columns = ['Mars', 'Data']
	mars_df = mars_df.set_index('Mars')
	mars_table_html = mars_df.to_html()
	mars_table_html = mars_table_html.replace('\n', '')

	mars_update['mars_table'] = mars_table_html



	# MARS HEMISPHERES
	url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(url_hemi)

	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')

	hemisphere_image_urls = []

	for h in range(4):
	    browser.find_by_tag('h3')[h].click()   
	    html = browser.html
	    soup = BeautifulSoup(html, 'html.parser')
	    title = soup.find('h2', class_='title').text
	    img_url_partial = soup.find('img', class_='wide-image')['src']
	    img_url = 'https://astrogeology.usgs.gov' + img_url_partial
	    dict = {'title':title, 'img_url':img_url}
	    hemisphere_image_urls.append(dict)
	    browser.back()

	mars_update['mars_hemispheres'] = hemisphere_image_urls
	browser.quit()

	return mars_update