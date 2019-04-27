# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from w3lib.url import url_query_cleaner

from scrapy.dupefilters import RFPDupeFilter
from scrapy.http.request import Request
from scrapy.downloadermiddlewares.cookies import CookiesMiddleware
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware

import re


class SteamSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SteamDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        print(request)
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        if 'agecheck' in response.url:
            print(response)
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CircumventAgeCheckMiddleware(RedirectMiddleware):

    def _redirect(self, redirected, request, spider, reason):

        # Only overrule the default redirect behavior

        # in the case of mature content checkpoints.

        #if not re.findall('app/(.*)/agecheck', redirected.url):

        if not re.search('/agecheck/app/', redirected.url):
            return super()._redirect(redirected, request, spider, reason)



        #logger.debug(f"Button-type age check triggered for {request.url}.")



        return Request(url=request.url,

                       cookies={'mature_content': '1',
                                'birthtime': '189302401',
                                'lastagecheckage': '1-January-1976',
                                },

                       meta={'dont_cache': True},

                       callback=spider.parse_product)


class SteamDupeFilter(RFPDupeFilter):
    """
    This is a customization of RFPDupeFilter class that will help us determine if a request for a particular URl
    was already processed. This can happen in Steam when the snr query parameter points to the same resource and the
    only thing that changes is that paramter. For instance

    http://store.steampowered.com/app/646200/Dead_Effect_2_VR/?snr=1_7_7_230_150_1&gt

    We could find another URL that is mostly the same and only snr changes, thus, this Filter class will remove the
    snr parameter from the request

    """

    def request_fingerprint(self, request):

        url = url_query_cleaner(request.url, ['snr'], remove=True)

        request = request.replace(url=url)

        return super().request_fingerprint(request)
