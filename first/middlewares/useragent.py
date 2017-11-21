from faker import Faker


class RandomUserAgentMiddleware:
    def __init__(self,settings):
        self.faker = Faker()

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings)

    def process_request(self,request,spider):
        request.headers['User-Agent'] = self.faker.user_agent()
        #request.headers['User-Agent'] = '%s-%s'%(self.faker.user_agent(),'yhp'*1000)