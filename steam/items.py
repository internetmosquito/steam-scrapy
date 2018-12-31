# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, Compose, TakeFirst
from scrapy.loader import ItemLoader


class StripText:
    """
    A commodity class to remove any character we decide from some string
    """

    def __init__(self, chars=' \r\t\n'):

        self.chars = chars

    def __call__(self, value):
        try:

            return value.strip(self.chars)

        except:

            return value


def str_to_int(x):

    try:
        return int(float(x))
    except:
        return x


class ProductItem(scrapy.Item):

    game_name = scrapy.Field()

    # For specs use a processor that simply removes \r\t\n chars
    specs = scrapy.Field(

        output_processor=MapCompose(StripText())

    )
    # For number of reviews remove \r\t\n chars first, then replace found ',' and finally try to convert to int
    n_reviews = scrapy.Field(

        output_processor=Compose(

            MapCompose(
                StripText(),
                lambda x: x.replace(',', ''),
                str_to_int),
            max

        )

    )


class ProductItemLoader(ItemLoader):

    default_output_processor=TakeFirst()  # (2)
