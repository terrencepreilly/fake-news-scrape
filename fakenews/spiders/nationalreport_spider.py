""" A spider for the fake-news site nationalreport.com  """

import scrapy

from ..utils.tags import extract_paragraphs

PAGES = 5


class NationalReportSpider(scrapy.Spider):

    name = 'national_report'

    start_urls = [
        'http://nationalreport.net/'
        ]

    def __init__(self, *args, **kwargs):
        self.count = 0
        super().__init__(*args, **kwargs)

    def parse(self, response):
        urls = response.css('#menu-primary .menu-item a::attr(href)').extract()
        for url in urls[1:]:
            self.count = 0
            yield scrapy.Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        current_pages = response.css(
            '.entry-title a::attr(href)'
            ).extract()
        for page in current_pages:
            yield scrapy.Request(url=page, callback=self.parse_page)

        next_url = response.css('.older a::attr(href)').extract_first()
        if next_url is not None and self.count < PAGES:
            self.count += 1
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_page(self, response):
        content = response.css('#content')
        meta = content.css('.entry-meta')
        post_date = meta.css('abbr::attr(title)').extract_first()
        title = content.css('h1.entry-title::text').extract_first()
        image_url = content.css('.entry img::attr(src)').extract_first()
        article_content = extract_paragraphs(
            content.css('.entry p')
            )
        author = content.css('.author-description h3::text').extract_first()
        comments = extract_paragraphs(
            response.css('.commentlist .comment-body p'),
            as_list=True,
            )

        yield {
            'title': title,
            'post_date': post_date,
            'author': author,
            'image_url': image_url,
            'content': article_content,
            'comments': comments,
            }
