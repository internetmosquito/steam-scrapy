# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import logging
from datetime import datetime, date
import scrapy
from scrapy.loader.processors import MapCompose, Compose, TakeFirst
from scrapy.loader import ItemLoader

logger = logging.getLogger(__name__)

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


def standardize_date(input_date):
    """
    Converts input_date from recognized input formats to desired output format,
    or leave unchanged if input format is not recognized.
    :param str input_date: The date to be formatted if needed
    :return: the formatted date
    :rtype: str
    """
    """
    
    """
    fmt_fail = False

    for fmt in ['%b %d, %Y', '%B %d, %Y']:
        try:
            return datetime.strptime(input_date, fmt).strftime('%Y-%m-%d')
        except ValueError:
            fmt_fail = True

    # Infer year to current year if it is missing.
    for fmt in ['%b %d', '%B %d']:
        try:
            d = datetime.strptime(input_date, fmt)
            d = d.replace(year=date.today().year)
            return d.strftime('%Y-%m-%d')
        except ValueError:
            fmt_fail = True

    if fmt_fail:
        logger.debug('Could not process date {0}'.format(input_date))

    return input_date


class ProductItem(scrapy.Item):
    """
    Used to represent a scrapped Item from Steam

    ...

    Attributes
    ----------
    url : scrapy.Field
        The full URL of the scrapped game
    id : scrapy.Field
        Unique identifier of game
    game_name : scrapy.Field
        Game name
    reviews_url : scrapy.Field
        Contains full reviews URL for game, needed to scrap all reviews
    specs : scrapy.Field
        Used to store specs like Single Player, Steam achievements, etc
    n_reviews : scrapy.Field
        Used to store maximum number of reviews for this game


    Methods
    -------
    None
    """
    url = scrapy.Field()
    id = scrapy.Field()
    reviews_url = scrapy.Field()
    title = scrapy.Field()
    # We need an output processor that will take the list of extracted genres and remove white spaces
    genres = scrapy.Field(
        output_processor=Compose(TakeFirst(), lambda x: x.split(','), MapCompose(StripText()))
    )
    developer = scrapy.Field()
    publisher = scrapy.Field()
    # For release date we need a new function to standardize date itself
    release_date = scrapy.Field(
        output_processor=Compose(TakeFirst(), StripText(), standardize_date)
    )
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

    default_output_processor = TakeFirst()
