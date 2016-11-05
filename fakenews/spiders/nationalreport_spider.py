""" A spider for the fake-news site nationalreport.com  """

import re
import scrapy

TAGS = re.compile('<.+?>')


class NationalReportSpider(scrapy.Spider):

    name = 'national_report'

    start_urls = [
        ('http://nationalreport.net/casey-anthony-breaks-silence-calls'
         '-planned-parenthood-baby-killers/'),
        ]

    def _extract_ps(self, all_ps):
        """Extract the inner html from all the paragraphs, and remove tags."""
        text = ''
        for p in all_ps:
            curr = p.extract()
            if isinstance(curr, str):
                text += ' '.join(TAGS.split(curr))
        return text

    def parse(self, response):
        content = response.css('#content')
        meta = content.css('.entry-meta')
        post_date = meta.css('abbr::attr(title)').extract_first()
        title = content.css('h1.entry-title::text').extract_first()
        image_url = content.css('.entry img::attr(src)').extract_first()
        article_content = self._extract_ps(
            content.css('.entry p')
            )
        author = content.css('.author-description h3::text').extract_first()

        yield {
            'title': title,
            'post_date': post_date,
            'author': author,
            'image_url': image_url,
            'content': article_content,
            }
