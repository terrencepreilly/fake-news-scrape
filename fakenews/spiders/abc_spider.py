""" A spider to scrape the fake news site abcnews.com.co """
import re
import scrapy

TAGS = re.compile('<.+?>')


class ABCSpider(scrapy.Spider):
    name = 'abcnews'
    start_urls = [
        'http://abcnews.com.co',
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
        for detail in response.css('.item-details'):
            h1 = detail.css('h1')
            if len(h1) == 0:
                continue
            title = h1.css('a::text').extract_first()
            time_data = detail.css('.td-post-date time::attr(datetime)')
            post_date = time_data.extract_first()
            author = detail.css('.td-post-author-name a::text').extract_first()
            image = detail.css('.td-post-featured-image img::attr(src)')
            image_url = image.extract_first()
            content = self._extract_ps(
                detail.css('.td-post-text-content p')
                )
            yield {
                'title': title,
                'post_date': post_date,
                'author': author,
                'image_url': image_url,
                'content': content,
                }
