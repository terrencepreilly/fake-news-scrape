""" A spider to scrape the fake news site abcnews.com.co """
import re
import scrapy

TAGS = re.compile('<.+?>')

PAGES = 5


class ABCSpider(scrapy.Spider):
    name = 'abcnews'

    def __init__(self, *args, **kwargs):
        self.curr = 1
        self.log('INSTANTIATING')
        return super().__init__(*args, **kwargs)

    def start_requests(self):
        url = 'http://abcnews.com.co'
        yield scrapy.Request(url=url, callback=self.parse)

    def _extract_ps(self, all_ps):
        """Extract the inner html from all the paragraphs, and remove tags."""
        text = ''
        for p in all_ps:
            curr = p.extract()
            if isinstance(curr, str):
                text += ' '.join(TAGS.split(curr))
        return text

    def _extract_article_and_metadata(self, detail):
            h1 = detail.css('h1')
            if len(h1) == 0:
                return None
            title = h1.css('a::text').extract_first()
            time_data = detail.css('.td-post-date time::attr(datetime)')
            post_date = time_data.extract_first()
            author = detail.css('.td-post-author-name a::text').extract_first()
            image = detail.css('.td-post-featured-image img::attr(src)')
            image_url = image.extract_first()
            content = self._extract_ps(
                detail.css('.td-post-text-content p')
                )
            return {
                'title': title,
                'post_date': post_date,
                'author': author,
                'image_url': image_url,
                'content': content,
                }

    def parse(self, response):
        self.log('PARSING PAGE {}'.format(self.curr))
        for detail in response.css('.item-details'):
            ret = self._extract_article_and_metadata(detail)
            if ret is not None:
                yield ret
        self.curr += 1
        if self.curr < PAGES:
            next_page = response.urljoin('/page/{}/'.format(self.curr))
            yield scrapy.Request(next_page, callback=self.parse)
