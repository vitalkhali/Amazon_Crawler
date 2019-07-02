# -*- coding: utf-8 -*-
import scrapy

from ..items import CrawlerItem

#######################################

import matplotlib.pyplot as plt

#######################################


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    page_number = 2
    start_urls = ['https://www.amazon.com/Books-Last-30-days/s?i=stripbooks&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&page=1&qid=1561311742&ref=sr_pg_1']

    def parse(self, response):
        items = CrawlerItem()

        name = response.css('.a-color-base.a-text-normal::text').extract()
        review_count = response.css('div.a-size-small span a span.a-size-base').css('::text').extract()
        price = response.css('.a-spacing-top-small .a-price:nth-child(1) .a-price-whole::text').extract()
        author = response.css('.a-color-secondary .a-size-base+ .a-size-base').css('::text').extract()
        image_link = response.css('.s-image::attr(src)').extract()

        #######################################

        for x in range(len(author)):
            author[x] = author[x].replace('\n', '')
            author[x] = author[x].replace('  ', '')

        for x in range(len(author)):
            if author[x] == ' and ':
                author[x-1] = author[x-1] + author[x] + author[x+1]
                author[x] = ""
                author[x+1] = ""

        author = list(filter(None, author))

        #######################################

        items['name'] = name
        items['review_count'] = review_count
        items['price'] = price
        items['author'] = author
        items['image_link'] = image_link

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # review_counts = list(map(int, items['review_count']))
        # prices = list(map(int, items['price']))
        #
        # for i in range(len(review_counts)):
        #     for j in range(len(prices)):
        #         if review_counts[j] < review_counts[i]:
        #             review_counts[i], review_counts[j] = review_counts[j], review_counts[i]
        #             prices[i], prices[j] = prices[j], prices[i]
        #
        # plt.plot(review_counts, prices)
        # plt.show()

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        yield items

        # next_page = 'https://www.amazon.com/Books-Last-30-days/s?i=stripbooks&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&'+ str(AmazonSpiderSpider.page_number) +'&qid=1561311742&ref=sr_pg_' + str(AmazonSpiderSpider.page_number)
        # if AmazonSpiderSpider.page_number <= 75:
        #     AmazonSpiderSpider.page_number += 1
        #     yield response.follow(next_page, callback=self.parse)
