from UDNnews.items import UdnnewsItem
import scrapy
import time
import pyquery


class UDNnewsSpider(scrapy.Spider):
    name = "UDNnews"
    allowed_domains = ["udn.com"]
    start_urls = [
        "https://udn.com/news/breaknews/1/99"
    ]

    def parse(self, response):
        full_url = "https://udn.com/news/breaknews/1/99"
        yield scrapy.Request(full_url, callback=self.parse_pyquery)

    def parse_question(self, response):
        turl = 'https://udn.com'
        Len = len(response.xpath('//h2/a/text()').extract())
        for i in range(Len):
            yield {
                'title': response.xpath('//h2/a/text()')[i].extract(),
                'url': turl + response.xpath('//h2/a')[i].extract().split('"')[3],
                'category': response.xpath('//dt/a/text()').extract()[i],
                'time': response.xpath('//div[@class="dt"]/text()').extract()[i]
            }

    def parse_pyquery(self, response):
        dom = pyquery.PyQuery(response.text)
        turl = 'https://udn.com'
        for i in dom('dt').items():
            if i('h2 a').text():
                yield {
                    'title': i('h2 a').text(),
                    'url': turl + i('h2 a').attr('href'),
                    'category': i('.cate').text(),
                    'time': i('div .dt').text()
                }
