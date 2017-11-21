from scrapy.exceptions import NotConfigured 
import random

class RandomProxyMiddleware(object):
    def __init__(self,settings):
        self.proxies = settings.getlist('PROXIES')
        
    def random_proxy(self):
        return random.choice(self.proxies)

    @classmethod
    def from_crawler(cls,crawler):
        if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
            raise NotConfigured('switch is False')
        if not crawler.settings.getlist('PROXIES'):
            raise NotConfigured('content is False')
        return cls(crawler.settings)

    def process_request(self,request,spider):
        if 'proxy' not in request.meta.keys():
            request.meta['proxy'] = self.random_proxy()