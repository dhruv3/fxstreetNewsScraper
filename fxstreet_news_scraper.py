import sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from urllib import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from goose import Goose
import csv
import dateparser

#https://stackoverflow.com/questions/42147601/pyqt4-to-pyqt5-mainframe-deprecated-need-fix-to-load-web-pages'
#dynamic page loading so PyQt5 used
#https://www.youtube.com/watch?v=FSH77vnOGqU
class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()

#get 50 links
BASE_URL = 'https://www.fxstreet.com/cryptocurrencies/news?q=&hPP=50&idx=FxsIndexPro&p=0&is_v=1'
client_response = Page(BASE_URL)
source = client_response.html
soup = BeautifulSoup(source, 'html.parser')

all_links = soup.find_all('h4', class_='fxs_headline_tiny')
#goose to extract content
#install goose again by reaching cd ~ directory and doing steps mentioned
#https://github.com/grangier/python-goose
g = Goose({'browser_user_agent': 'Mozilla', 'parser_class':'soup'})
#you don't have to close csv file
F = csv.writer(open("fxNewsLink.csv", 'w'))

for elem in all_links:
    link = elem.contents[1]['href']
    article = g.extract(url=link)
    content = article.cleaned_text

    #to get date of article we oprn the link and extract time element
    response = urlopen(link).read()
    date_soup = BeautifulSoup(response, 'html.parser')
    date = date_soup.find_all('time')[0]['datetime']
    date = dateparser.parse(date)

    timestamp = datetime.now()
    title = article.title
    #encoding was required as ascii unicode popped up
    #list of element used as strings have commas and these commas act as delimiters
    #so prevent normal commas to act as delimiters we used a list and csv package
    out = [link.encode("utf-8") , content.encode("utf-8") , date.strftime('%Y-%m-%d %H:%M:%S').encode("utf-8") , timestamp.strftime('%Y-%m-%d %H:%M:%S').encode("utf-8") , title.encode("utf-8")]
    F.writerow(out)
