# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#该文件处理抓取的数据
#验证爬取的数据（检查item包含某些字段）
#查重(并丢弃)
#将爬取结果保存到数据库

from scrapy.exceptions import DropItem
import logging
from redis import Redis
import pymysql


class CheckPipeline(object):
    logger = logging.getLogger(__name__)
    def open_spider(self,spider):
        '''
        运行spider之前运行的函数
        '''
        self.logger.info('Open Spider')

    def close_spider(self,spider):
        '''
        结束spider之后运行的函数
        '''
        self.logger.info('Close Spider')


    def process_item(self, item,spider):              #将yield回的东西返回
        if not item.get('undergraduate_num'): 
            raise DropItem("Missing undergraduate_num in %s"%item['name'])
        if not item.get('postgraduate_num'):
            raise DropItem("Missing postgraduate_num in %s"%item['name'])
        return item

class RedisPipeline(object):
    def __init__(self):
        self.r = Redis()
    def process_item(self,item,spider):
        
        self.r.sadd(spider.name,item.get('name'))
        
        CheckPipeline.logger.info('redis : add %s to list %s'%(item['name'],spider.name))

        return item

    def __del__(self):
        del self.r
    
class MySqlPipeline(object):
    def __init__(self):
        self.conn = None
        self.cur = None


    def open_spider(self,spider):
        self.conn = pymysql.connect(
            host = '127.0.0.1',
            port = 3306,
            user = 'root',
            password='111111',
            charset = 'utf8',
            db = 'first'
        )
        
        self.cur = self.conn.cursor()

    
        
    def process_item(self,item,spider):
        #sql = "INSERT INTO `universities`('name','rank','country','state','city','undergraduate_num','postgraduate_num','website') VALUES(" +','.join(['%s'] * 8) + ")"
        sql = "INSERT INTO `first`.`universities` (`name`, `rank`, `country`, `state`, `city`, `undergraduate_num`, `postgraduate_num`, `website`) VALUES ("+','.join(['%s'] * 8) + ");"
        #self.cur.execute(sql,[item[key] for key in item.keys()])
        self.cur.execute(sql,(item['name'],item['rank'],item['country'],item['state'],item['city'],item['undergraduate_num'],item['postgraduate_num'],item['website']))
        self.conn.commit()
        return item

    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()