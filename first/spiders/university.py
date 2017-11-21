# -*- coding: utf-8 -*-
import scrapy
from w3lib.html import remove_tags
from ..items import UniversityItem

class UniversitySpider(scrapy.Spider):
    def __init__(self,max_num = -1,name = None,**kwargs):
        super(UniversitySpider,self).__init__(name,**kwargs)
        self.max_num = int(max_num)

    name = 'university'
    allowed_domains = ['140.143.192.76']
    start_urls = ['http://140.143.192.76:8002/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D']

    def parse(self, response):
        links = response.xpath("//div[@id='content']//tr[position()>1]/td[2]//@href").extract()
        for i,link in enumerate(links):
            if self.max_num >= 0 and i > self.max_num:
                break
            if not link.startswith('http://'):    
                link = 'http://140.143.192.76:8002/' + link
             
            request = scrapy.Request(link,callback=self.parse_university)
            request.meta['rank'] = i + 1
            yield request
            #yield response.follow(link,callback = self.parse_university)
    
    def filter(self,html):
        return remove_tags(html,which_ones=('sup',)).replace('\r','').replace('\n','').replace('\t','')

    def parse_university(self,response):
        #self.logger.info(response.meta['link'])
        response = response.replace(body=self.filter(response.text))  #将response中字符串替换   默认response是不能更改的
        wiki_content = response.xpath('//div[@id="wikiContent"]')
        item = UniversityItem(
            name = wiki_content.xpath('./h1[@class="wikiTitle"]/text()').get(),
            rank = response.meta['rank'],
        )
        #item = dict(title=wiki_content.xpath('./h1[@class="wikiTitle"]/text()').extract_first())
        keys = wiki_content.xpath('./div[@class="infobox"]/table//tr/td[1]//text()').extract()
        values = wiki_content.xpath('./div[@class="infobox"]/table//tr/td[2]')
        values = [','.join(val.xpath('.//text()').extract()) for val in values]
        data = dict(zip(keys,values))
        item['country'] = data.get('国家','')
        item['state'] = data.get('州省','')
        item['city'] = data.get('城市','')
        item['undergraduate_num'] = data.get('本科生人数','')
        item['postgraduate_num'] = data.get('研究生人数','')
        item['website'] = data.get('网址','')
        print(item)
        self.logger.info('%s scraped'%item['name'])
        yield item