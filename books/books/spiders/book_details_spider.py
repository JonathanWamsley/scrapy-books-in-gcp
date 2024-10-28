import scrapy
from scrapy.loader import ItemLoader
from books.items import ProductItem

class BookDetailsSpider(scrapy.Spider):
    name = 'book_details_spider'
    start_urls = ['https://books.toscrape.com/']

    # pylint: disable=arguments-differ
    def parse(self, response):
        # Log the status code for the main page
        self.logger.info("Visited %s with status code %s", response.url, response.status)

        # Follow each book link to get detailed information
        book_links = response.css('h3 a::attr(href)').getall()
        for link in book_links:
            yield response.follow(link, self.parse_book_details)

        # Follow pagination link
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_book_details(self, response):
        # Log the status code for each book detail page
        self.logger.info("Visited book details page: %s with status code %s", response.url, response.status)

        loader = ItemLoader(item=ProductItem(), response=response)
        loader.add_css('name', 'h1::text')
        loader.add_css('price', 'p.price_color::text')
        loader.add_css('description', '#product_description ~ p::text')
        loader.add_value('url', response.url)

        item = loader.load_item()

        # Check for empty fields and log warnings if necessary
        if not item.get('name'):
            self.logger.warning("Missing name for book at %s", response.url)
        if not item.get('price'):
            self.logger.warning("Missing price for book at %s", response.url)
        if not item.get('description'):
            self.logger.warning("Missing description for book at %s", response.url)

        yield item
