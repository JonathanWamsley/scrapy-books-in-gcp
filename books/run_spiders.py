import os
import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from books.spiders.books_spider import BooksSpider
from books.spiders.book_details_spider import BookDetailsSpider

if __name__ == "__main__":
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Create a unique directory for each scrape run
    output_dir = f'scrape_results/scrape_{now}'
    os.makedirs(output_dir, exist_ok=True)

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # First Spider: Save data and logs in the same scrape_results directory
    settings.set('FEEDS', {
        f'{output_dir}/books_spider_output_{now}.csv': {
            'format': 'csv',
        }
    })
    settings.set('LOG_FILE', f'{output_dir}/books_spider_log_{now}.log')
    process.crawl(BooksSpider)

    # Second Spider: Save data and logs in the same scrape_results directory
    settings.set('FEEDS', {
        f'{output_dir}/book_details_spider_output_{now}.csv': {
            'format': 'csv',
        }
    })
    settings.set('LOG_FILE', f'{output_dir}/book_details_spider_log_{now}.log')
    process.crawl(BookDetailsSpider)

    process.start()
