""" A spider to crawl the fake news site thebostontribune.com """

import scrapy

from ..utils.tags import extract_paragraphs


class BostonTribuneSpider(scrapy.Spider):

    name = 'boston_tribune'

    start_urls = [
        'http://thebostontribune.com/'
        ]

    def parse(self, response):
        blocks = response.css('.td-block-span4')
        articles = [
            x.css('a::attr(href)').extract_first()
            for x in blocks
            ]
        for article in articles:
            yield scrapy.Request(url=article, callback=self._parse_page)

    def _parse_page(self, response):
        author = response.css('.td-post-author-name a::text').extract_first()
        post_date = response.css(
            '.td-post-date time::attr(datetime)'
            ).extract_first()
        image = response.css(
            '.td-post-content img::attr(src)'
            ).extract_first()
        content = extract_paragraphs(
            response.css('.td-post-content p')
            )
        title = response.css(
            '.td-post-title h1::text'
            ).extract_first()
        comments = extract_paragraphs(
            response.css('.comment-content p'),
            as_list=True,
            )
        yield {
            'title': title,
            'post_date': post_date,
            'author': author,
            'image_url': image,
            'content': content,
            'comments': comments,
            }
