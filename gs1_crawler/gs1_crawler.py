import logging
import os
import shutil
import json

from scrapy.crawler import CrawlerProcess
from gs1_crawler import BASE_DIR, PKG_DIR
from gs1_crawler.services import KoreanNet

from urllib import parse
from scrapy import Spider, Request
from gs1_crawler.foods import Foods
from gs1_crawler.items import GS1Item


class GS1_crawler(object):
  def __init__(self):
    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.INFO)
    settings = {
      'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
      'FEED_FORMAT': 'json',
      'FEED_EXPORT_ENCODING': 'UTF-8',
      'FEED_URI': os.path.join(BASE_DIR, 'out.json'),
      'LOG_LEVEL': 'INFO'
    }

    self.process = CrawlerProcess(settings)
    self.logger.info('The file location: %s' % os.path.join(BASE_DIR, 'out.json'))

  def start(self):

    self.process.crawl(KoreanNet)
    self.process.start()
    self.logger.info('############################### completed')

    return True