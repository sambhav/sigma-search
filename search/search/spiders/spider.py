#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import scrapy
import urllib
import urlparse
import imagehash
from PIL import Image
from bs4 import BeautifulSoup as bs
from search.items import SearchItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class MySpider(CrawlSpider):

    name = 'intra-spider'
    allowed_domains = ['iitg.ernet.in']
    start_urls = ['http://intranet.iitg.ernet.in/sitemap']

    denyList = (
        '\.tar.*',
        '\.zip',
        '.*cclrs.*',
        '.*showstructure.*',
        '.*calendar.*',
        '.*eventcal.*',
        '.*interactive-sessions.*',
        '.*/resources/resources/.*',
        '.*month.php?.*',
        '.*csea/Public.*',
        '.*forum.*',
        '.*csesoftwarerepo.*',
        '.*reservation.*',
        '.*month=\d+',
        '.*C=D&O=D*',
        '.*C=M&O=.*',
        '.*C=S&O=.*',
        '.*C=N&O=.*',
        '.*all-events.*',
        )

    custom_settings = {
        'CONCURRENT_ITEMS': 100,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
        'REACTOR_THREADPOOL_MAXSIZE': 20,
        'LOG_LEVEL': 'INFO',
        'RETRY_ENABLED': False,
        'COOKIES_ENABLED': False,
        'DOWNLOAD_TIMEOUT': 15,
        'DOWNLOAD_MAXSIZE': 33554432,
        }

    rules = (Rule(LinkExtractor(allow=(), tags=('a', 'area', 'frame'),
             attrs=('href', 'src'), deny=denyList),
             callback='parse_item', follow=True), )

    def parse_item(self, response):
        item = SearchItem()
        item['URL'] = response.url
        title = ''
        soup = bs(response.body, 'lxml')
        try:
            title = soup.title.string
        except(e):
            print e
        item['Title'] = title
        vis = []
        try:
            texts = soup.findAll(text=True)
            for i in texts:
                if i.parent.name in ['style', 'script', '[document]',
                        'head', 'title']:
                    pass
                else:
                    i = re.sub('(<!--.*?-->)', '', i,
                               flags=re.MULTILINE)
                    i = re.sub("\s+", ' ', i)
                    vis.append(i)
        except(e):
            print e
        item['Content'] = ' '.join(vis)
        imgs = []

        images = soup.find_all('img', src=True)

        for i in images:
            URL = urlparse.urljoin(response.url, i['src'])
            IMAGE = URL.rsplit('/', 1)[1]
            EXT = URL.rsplit('.', 1)[1]
            urllib.urlretrieve(URL, r"/home/sam/Desktop/imagestore/" + IMAGE)
            hashval = imagehash.average_hash(Image.open(r"/home/sam/Desktop/imagestore/" + IMAGE))
            data = [URL, IMAGE, str(hashval)]
            imgs.append(' :: '.join(data))
        item['Images'] = ' || '.join(imgs)

        return item



