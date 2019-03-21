#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crawler for [LnIndo](https://lnindo.org/).
"""
import json
import logging
import re
from ..utils.crawler import Crawler

logger = logging.getLogger('LNINDO')

chapter_start_url = 'https://lnindo.org/%s/'


class LnindoCrawler(Crawler):
    def read_novel_info(self):
        '''Get novel title, autor, cover etc'''
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url, parser='html5lib')

        self.novel_title = soup.find_all(
            'span', {"typeof": "v:Breadcrumb"})[-1].text
        self.novel_title = self.novel_title.split('~')[0].strip()
        logger.info('Novel title: %s', self.novel_title)

        self.novel_cover = "https://lnindo.org/images/noavailable.jpg"
        logger.info('Novel cover: %s', self.novel_cover)

        author = soup.select('p')[2].text
        self.novel_author = author[20:len(author)-22]
        logger.info('Novel author: %s', self.novel_author)

        # if soup.find('blockquote', {"style": re.compile('-moz-border-radius.*')}):
        #     chapters = soup.find(
        #         'blockquote', {"style": re.compile('moz-border-radius.*')}).findAll('a')
        # elif soup.find('div', {"style": re.compile('moz-border-radius.*')}):
        #     chapters = soup.find(
        #         'div', {"style": re.compile('moz-border-radius.*')}).findAll('a')
        # elif soup.select('div.markobar li a'):
        #     chapters = soup.select('div.markobar li a')
        # elif soup.find('div', {'class': 'sharebar'}):
        #     chapters = soup.find('div', {'class': 'sharebar'}).findNext(
        #         'div', {'class': 'ads'}).findNext('div').select('ul li a')
        # else:
        #     chapters = soup.find('h3').findNextSibling('div').findNextSibling(
        #         'div').findNextSibling('div').select('ul li a')
        # # end if

        volumes = set([])
        checked = set([])
        novel_id = self.novel_url.strip('/').split('/')[-1]
        wrong = [0,3]
        start_url = chapter_start_url % novel_id
        if len(soup.body.contents[0].contents[7].contents[0].contents[16].contents[0].select('a')) not in wrong:
            chapters = soup.body.contents[0].contents[7].contents[0].contents[16].contents[0].select('a')
        elif len(soup.body.contents[0].contents[7].contents[0].contents[17].contents[0].select('a'))not in wrong:
            chapters = soup.body.contents[0].contents[7].contents[0].contents[17].contents[0].select('a')
        elif len(soup.body.contents[0].contents[7].contents[0].contents[18].contents[0].select('a'))not in wrong:
            chapters = soup.body.contents[0].contents[7].contents[0].contents[18].contents[0].select('a')
        else:
            chapters = soup.body.contents[0].contents[7].contents[0].contents[19].contents[0].select('a')
        chapters.reverse()

        for a in chapters:
            chap_id = len(self.chapters) + 1
            if len(self.chapters) % 100 == 0:
                vol_id = chap_id//100 + 1
                vol_title = 'Volume ' + str(vol_id)
                self.volumes.append({
                    'id': vol_id,
                    'title': vol_title,
                })
            # end if
            self.chapters.append({
                'id': chap_id,
                'volume': vol_id,
                'url':  self.absolute_url(a['href']),
                'title': a.text.strip() or ('Chapter %d' % chap_id),
            })
        # end for

        logger.debug(self.chapters)
        logger.debug('%d chapters found', len(self.chapters))
    # end def

    def download_chapter_body(self, chapter):
        '''Download body of a single chapter and return as clean html format.'''
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])

        for a in soup.find_all('a'):
            a.decompose()

        body_parts = soup.select('p')

        return ''.join([str(p.extract()) for p in body_parts if p.text.strip() and not 'Advertisement' in p.text and not 'JavaScript!' in p.text])
    # end def
# end class
