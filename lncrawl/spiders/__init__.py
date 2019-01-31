#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .lnmtl import LNMTLCrawler
from .webnovel import WebnovelCrawler
from .wuxiacom import WuxiaComCrawler
from .wuxiaco import WuxiaCoCrawler
from .wuxiaonline import WuxiaOnlineCrawler
from .boxnovel import BoxNovelCrawler
from .readln import ReadLightNovelCrawler
from .novelplanet import NovelPlanetCrawler
from .lnindo import LnindoCrawler
from .idqidian import IdqidianCrawler
from .romanticlb import RomanticLBCrawler
from .webnonline import WebnovelOnlineCrawler
from .fullnovellive import FullnovelLiveCrawler
from .novelall import NovelAllCrawler
from .novelfull import NovelFullCrawler

# Do not forget to append a slash(/) at the end
crawler_list = {
    'https://lnmtl.com/': LNMTLCrawler,
    'https://www.webnovel.com/': WebnovelCrawler,
    'https://webnovel.online/': WebnovelOnlineCrawler,
    'https://wuxiaworld.online/': WuxiaOnlineCrawler,
    'https://www.wuxiaworld.com/': WuxiaComCrawler,
    'https://www.wuxiaworld.co/': WuxiaCoCrawler,
    'https://m.wuxiaworld.co/': WuxiaCoCrawler,
    'https://boxnovel.com/': BoxNovelCrawler,
    'https://novelplanet.com/': NovelPlanetCrawler,
    'https://www.readlightnovel.org/': ReadLightNovelCrawler,
    'https://lnindo.org/': LnindoCrawler,
    'https://www.idqidian.us/': IdqidianCrawler,
    'https://m.romanticlovebooks.com/': RomanticLBCrawler,
    'https://www.romanticlovebooks.com/': RomanticLBCrawler,
    'http://fullnovel.live/': FullnovelLiveCrawler,
    'https://www.novelall.com/': NovelAllCrawler,
    'http://novelfull.com': NovelFullCrawler,
}
