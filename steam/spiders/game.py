import logging
from w3lib.url import canonicalize_url, url_query_cleaner
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest
from steam.items import ProductItem, ProductItemLoader


logger = logging.getLogger(__name__)


class ProductSpider(CrawlSpider):

    name = 'games'

    start_urls = ["https://store.steampowered.com/search/?sort_by=Released_DESC"]

    allowed_domains = ["steampowered.com"]

    rules = [

        Rule(

            LinkExtractor(

                allow='/app/(.+)/',

                restrict_css='#search_result_container'),

            callback='parse_product'),

        Rule(

            LinkExtractor(

                allow='page=(\d+)',

                restrict_css='.search_pagination_right'))

    ]

    def load_product(self, response):
        """
        Get game name using css class name and other characteristics same way
        :param response: The obtained response from spider
        :return: A dict containing game name and other characteristics
        """
        
        loader = ProductItemLoader(item=ProductItem(), response=response)
        url = url_query_cleaner(response.url, ['snr'], remove=True)
        url = canonicalize_url(url)
        loader.add_value('url', url)

        loader.add_css('game_name', '.apphub_AppName ::text')
        loader.add_css('specs', '.game_area_details_specs a ::text')
        loader.add_css('n_reviews', '.responsive_hidden',
                       re='\(([\d,]+)')
        item = loader.load_item()
        return item

    def parse_product(self, response):
        # Removed this because it simply ain't working as expected
        """if '/agecheck/app' in response.url:

            logger.debug("Form-type age check triggered for {0}.".format(response.url))

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            }

            body = 'sessionid=778802c11a5b3d97cfcf4fed&ageDay=1&ageMonth=January&ageYear=1959'
            # you can probably leave sessionid empty here or just add some gibberish

            yield Request(
                url=response.url,
                method='POST',
                body=body,
                headers=headers,
                callback=self.parse_product
            )

            form = response.css('#agegate_box form')

            action = form.xpath('@action').extract_first()

            name = form.xpath('input/@name').extract_first()

            value = form.xpath('input/@value').extract_first()

            formdata = {

                'ageDay': '1',

                'ageMonth': '1',

                'ageYear': '1955'

            }

            yield FormRequest(

                url=response.url,

                method='POST',

                formdata=formdata,

                callback=self.parse_product

            )

        else:"""
        # I moved all parsing code into its own function for clarity.
        yield self.load_product(response)





