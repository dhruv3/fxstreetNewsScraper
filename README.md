# fxstreet News Scraper

Scraper to get data from Cryptocurrencies section of FXStreet. It takes all the news links present in [this url](https://www.fxstreet.com/cryptocurrencies/news?q=&hPP=25&idx=FxsIndexPro&p=0&is_v=1) and then scrapes them all sequentially.

There are two scrapers present. One that uses Selenium headless browser and other utilizes PyQt5 to extract content.

Requirement file for Selenium scraper has been attached.

The output of both scrapers is a CSV file which is in format <link, content, date of article, timestamp, title>
