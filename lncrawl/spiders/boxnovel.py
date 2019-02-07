#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crawler for [boxnovel.com](https://boxnovel.com/).
"""
import json
import logging
import re
from bs4 import BeautifulSoup
from ..utils.crawler import Crawler

logger = logging.getLogger('BOXNOVEL')
search_url = 'https://boxnovel.com/?s=%s&post_type=wp-manga&author=&artist=&release='


class BoxNovelCrawler(Crawler):
    def search_novel(self, query):
        query = query.lower().replace(' ', '+')
        response = self.get_response(search_url % query)
        soup = BeautifulSoup(response.text, 'lxml')

        results = []
        for a in soup.select('.post-title h4 a'):
            results.append((
                a.text.strip(),
                self.absolute_url(a['href']),
            ))
        # end for

        return results
    # end def

    def read_novel_info(self):
        '''Get novel title, autor, cover etc'''
        logger.debug('Visiting %s', self.novel_url)
        response = self.get_response(self.novel_url)
        soup = BeautifulSoup(response.text, 'lxml')

        self.novel_title = ' '.join([
            str(x)
            for x in soup.select_one('.post-title h3').contents
            if not x.name
        ]).strip()
        logger.info('Novel title: %s', self.novel_title)

        self.novel_cover = self.absolute_url(
            soup.select_one('.summary_image img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)

        author = soup.find('div', {'class': 'author-content'}).findAll('a')
        if len(author) == 2:
            self.novel_author = author[0].text + ' (' + author[1].text + ')'
        else:
            self.novel_author = author[0].text
        logger.info('Novel author: %s', self.novel_author)

        chapters = soup.select('ul.main li.wp-manga-chapter a')
        chapters.reverse()

        for a in chapters:
            chap_id = len(self.chapters) + 1
            vol_id = chap_id//100 + 1
            if len(self.chapters) % 100 == 0:
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
        response = self.get_response(chapter['url'])
        soup = BeautifulSoup(response.text, 'lxml')

        #chapter['title'] = soup.find('li', {'class':'active'}).text
        div = soup.find("div", {"class": "text-left"})
        self.clean_contents(div)
        content = div.findAll("p")

        title = soup.find_all(re.compile('^h[2-4]$'))

        if len(title):
            chapter['title'] = title[0].text
        else:
            if 'Translator' in soup.select_one('p').text:
                chapter['title'] = soup.select_one(
                    'p').text.split("Translator", 1)[0]
            else:
                chapter['title'] = soup.select_one('p').text
                logger.info('Downloading %s', content.pop(0))

        body_parts = ''.join([str(p.extract())
                              for p in content if p.text.strip()])

        return body_parts
    # end def
# end class
