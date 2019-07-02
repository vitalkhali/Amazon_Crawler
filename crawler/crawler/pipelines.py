# -*- coding: utf-8 -*-

import sqlite3

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlerPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("books.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        if self.curr.execute("""drop table if exists books_tb"""):
            self.curr.execute("""create table books_tb(
                            name text,
                            review_count int,
                            price int,
                            author text,
                            image_link text
                            )""")

    def process_item(self, item, spider):
        self.store_db(item)
        # print('Pipeline: '+ item['title'][0])
        return item

    def store_db(self, item):
        self.curr.execute("""insert into books_tb values (?,?,?,?,?)""",(
            item['name'][0],
            item['review_count'][0],
            item['price'][0],
            item['author'][0],
            item['image_link'][0]
        ))
        self.conn.commit()
