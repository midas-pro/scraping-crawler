#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import re
from ..utils.crawler import Crawler

logger = logging.getLogger('KISSLIGHTNOVEL')
search_url = 'https://kisslightnovels.info/wp-admin/admin-ajax.php'


class KissLightNovels(Crawler):
    def search_novel(self, query):
        body = {
            'action': 'wp-manga-search-manga',
            'title': query,
        }
        response = self.submit_form(search_url, body)
        data = response.json()
        return data['data']
    # end def

    def read_novel_info(self):
        '''Get novel title, autor, cover etc'''
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)

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

        volumes = set()
        for a in chapters:
            chap_id = len(self.chapters) + 1
            vol_id = chap_id // 100 + 1
            volumes.add(vol_id)
            self.chapters.append({
                'id': chap_id,
                'volume': vol_id,
                'url':  self.absolute_url(a['href']),
                'title': a.text.strip() or ('Chapter %d' % chap_id),
            })
        # end for

        self.volumes = [{'id': x} for x in volumes]

        logger.debug('%d volumes and %d chapters found',
                     len(self.volumes), len(self.chapters))
    # end def

    def download_chapter_body(self, chapter):
        '''Download body of a single chapter and return as clean html format.'''
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])

        contents = soup.select_one('div.text-left')

        if contents.h3:
            contents.h3.decompose()

        for codeblock in contents.findAll('div', {'class': 'code-block'}):
            codeblock.decompose()

        self.clean_contents(contents)
        return str(contents)
    # end def
# end class
