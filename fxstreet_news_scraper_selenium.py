import sys
import csv
from selenium import webdriver
import os
from datetime import datetime
import csv
import dateparser
import MySQLdb

# code to get all fxstreet links from last two days in database
def dbconnect():
	conn = MySQLdb.connect(host='cs336.ckksjtjg2jto.us-east-2.rds.amazonaws.com', port=3306, user='student', passwd='cs336student', db='CryptoNews', charset='utf8')
	return conn.cursor()
cursor = dbconnect()
cursor.execute(""" SELECT link FROM CryptoNews.cryptonews WHERE link LIKE "https://www.fxstreet%" and date >= DATE(NOW()) - INTERVAL 2 DAY order by date desc """)
cursor.fetchall()
curr_links_set = set()
for row in cursor:
	curr_links_set.add(row[0])

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'), chrome_options=options)

#get 25 links
BASE_URL = 'https://www.fxstreet.com/cryptocurrencies/news?q=&hPP=25&idx=FxsIndexPro&p=0&is_v=1'
driver.get(BASE_URL)
all_links_util = driver.find_elements_by_class_name('fxs_headline_tiny')
all_links = []

for elem in all_links_util:
    if len(elem.find_elements_by_tag_name('a')) != 0:
		link = elem.find_elements_by_tag_name('a')[0].get_attribute('href')
		if link not in curr_links_set:
			all_links.append(link)

#you don't have to close csv file
F = csv.writer(open("fxCryptoNews.csv", 'w'))

for link in all_links:
    driver.get(link)
    title = driver.title

    timestamp = datetime.now()

    date = driver.find_elements_by_tag_name('time')[1].get_attribute('datetime')
    date = dateparser.parse(date)

    content_div = driver.find_elements_by_class_name('fxs_article_content')[0]
    paras = content_div.find_elements_by_tag_name('p')
    content = ''
    for para in paras:
        content += para.get_attribute('innerText')
    #encoding was required as ascii unicode popped up
    #list of element used as strings have commas and these commas act as delimiters
    #so prevent normal commas to act as delimiters we used a list and csv package
    out = [link.encode("utf-8") , content.encode("utf-8") , date.strftime('%Y-%m-%d %H:%M:%S'), timestamp.strftime('%Y-%m-%d %H:%M:%S') , title.encode("utf-8")]
    F.writerow(out)
