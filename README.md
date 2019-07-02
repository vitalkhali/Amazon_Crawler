# Amazon_Crawler
Web crawler and data filter using Scrapy.

A Web crawler or spiderbot often shortened to crawler, is an Internet bot that systematically browses the Internet 
for the purpose of Web indexing (web spidering).
Web search engines and many other sites use Web crawling or spidering software to update their web content or indices of other sites's web content.

Scrapy is written with Twisted, a popular event-driven networking framework for Python. 
Thus, it’s implemented using a non-blocking (aka asynchronous) code for concurrency. 
The Scrapy Engine is responsible for controlling the data flow between all components of the system, and triggering events when certain actions occur.

The Scheduler receives requests from the engine and enqueues them for feeding them later (also to the engine) when the engine requests them. 

The Downloader is responsible for fetching web pages and feeding them to the engine which, in turn, feeds them to the spiders.
