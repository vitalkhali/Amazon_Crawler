# -*- coding: utf-8 -*-
import scrapy

from ..items import CrawlerItem
import sqlite3

#######################################

import matplotlib.pyplot as plt

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

#######################################


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    page_number = 2
    start_urls = [
        'https://www.amazon.com/Books-Last-30-days/s?i=stripbooks&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&page=1&qid=1561311742&ref=sr_pg_1']

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        items = CrawlerItem()

        all_books = response.css('.s-include-content-margin')

        for books in all_books:
            name = books.css('.a-color-base.a-text-normal::text').extract()
            review_count = books.css('div.a-size-small span a span.a-size-base').css('::text').extract()
            price = books.css('.a-spacing-top-small .a-price:nth-child(1) .a-price-whole::text').extract()
            author = books.css('.a-color-secondary .a-size-base+ .a-size-base').css('::text').extract()
            image_link = books.css('.s-image::attr(src)').extract()

            #######################################

            for x in range(len(author)):  # Removing all the newlines
                author[x] = author[x].replace('\n', '')
                author[x] = author[x].replace('  ', '')

            for x in range(len(review_count)):
                review_count[x] = review_count[x].replace(',', '')

            for x in range(len(price)):
                price[x] = price[x].replace(',', '')

            if len(review_count) == 0:
                review_count = ['0']

            if len(price) == 0:
                price = ['0']

            for x in range(len(author)): # Joining multiple authors
                if author[x] == ' and ':
                    author[x - 1] = author[x - 1] + author[x] + author[x + 1]
                    author[x] = ""
                    author[x + 1] = ""

            author = list(filter(None, author))

            #######################################

            items['name'] = name
            items['review_count'] = review_count
            items['price'] = price
            items['author'] = author
            items['image_link'] = image_link

            yield items

        next_page = 'https://www.amazon.com/Books-Last-30-days/s?i=stripbooks&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&page=' + str(
            AmazonSpiderSpider.page_number) + '&qid=1561311742&ref=sr_pg_' + 'str(AmazonSpiderSpider.page_number)'
        if AmazonSpiderSpider.page_number <= 75:
            AmazonSpiderSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def spider_closed(self, spider):
        self.conn = sqlite3.connect("books.db")
        self.curr = self.conn.cursor()

        review_counts = [review_count[0] for review_count in self.curr.execute("SELECT review_count FROM books_tb")]
        prices = [price[0] for price in self.curr.execute("SELECT price FROM books_tb")]

        for i in range(len(review_counts)):
            for j in range(len(prices)):
                if review_counts[j] < review_counts[i]:
                    review_counts[i], review_counts[j] = review_counts[j], review_counts[i]
                    prices[i], prices[j] = prices[j], prices[i]

        plt.plot(review_counts, prices)
        plt.show()
