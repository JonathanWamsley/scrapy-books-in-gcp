import scrapy
from scrapy.loader import ItemLoader
from books.items import ProductItem

class BooksSpider(scrapy.Spider):
    name = 'books_spider'
    start_urls = ['https://books.toscrape.com/']

    # pylint: disable=arguments-differ
    def parse(self, response):
        # Log the status code
        self.logger.info("Visited %s with status %s", response.url, response.status)

        books = response.css('article.product_pod')
        for book in books:
            loader = ItemLoader(item=ProductItem(), selector=book)
            loader.add_css('name', 'h3 a::attr(title)')
            loader.add_css('price', 'div.product_price p.price_color::text')
            loader.add_css('link', 'h3 a::attr(href)')

            item = loader.load_item()

            # Check if any field is empty and log a warning
            if not item.get('name'):
                self.logger.warning("Missing name for book at %s", response.url)
            if not item.get('price'):
                self.logger.warning("Missing price for book at %s", response.url)

            yield item

        # Follow pagination link
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
