# -*- coding: utf-8 -*-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# credit : https://www.pragnakalp.com/python-tutorial-scrapy-website-crawler/

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import mysql.connector
from mysql.connector import errorcode
from scrapy.crawler import CrawlerProcess

# MySQL Connection
try:
    # use database credentials and name for connections
    mydb = mysql.connector.connect(host='localhost', user='user1', password='password1', database='rsg_db')
    cursor = mydb.cursor(buffered=True)
    print("Connected")
    
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

# Crawl Spider - run as: scrapy crawl rsg1
class Rsg(CrawlSpider):
	
	name = 'rsg1'	
	allowed_domains = ['books.toscrape.com']
	start_urls = ['http://books.toscrape.com/']
	headers = {
                'user-agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
				}
	rules = (Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),)
		
	def parse_item(self, response): 
		x = response.url
		y = str(x)
		print("Value to be inserted is ===> ",y)
		myquery = 'INSERT IGNORE INTO links (url) VALUE ( "'+y+'" );'
		cursor.execute(myquery)
		mydb.commit()	


if __name__ == "__main__":
	process = CrawlerProcess()
	process.crawl(Rsg)
	process.start()
	
