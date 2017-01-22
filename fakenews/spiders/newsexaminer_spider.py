"""A spider for the various pages of newsexaminer.net"""
import scrapy

from ..utils.tags import extract_paragraphs


class NewsExaminerSpider(scrapy.Spider):

    name = 'news_examiner'

    start_urls = [
        'http://newsexaminer.net/',
        ]

    def parse(self, response):
        links = response.css(
            '#vce_main_navigation_menu '
            '.menu-item '
            '.sub-menu '
            '.menu-item '
            'a'
            )
        urls = [x.css('::attr(href)').extract_first() for x in links]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        urls = [
            x.css('::attr(href)').extract_first()
            for x in response.css('article a')
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        title = response.css('article h1::text').extract_first()
        author = response.css('.meta-author-wrapped a::text').extract_first()
        image = response.css('.meta-image img::attr(src)').extract_first()
        content = extract_paragraphs(
            response.css('.entry-content p')
            )
        comments = extract_paragraphs(
            response.css('.comment-content p'),
            as_list=True,
            )
        post_date = [
            x.css('::attr(content)').extract_first()
            for x in response.css('meta')
            if (x.css('::attr(property)').extract_first()
                == 'article:published_time')
            ]
        yield {
            'title': title,
            'post_date': post_date[0] if len(post_date) > 0 else None,
            'author': author,
            'image_url': image,
            'content': content,
            'comments': comments,
            }
