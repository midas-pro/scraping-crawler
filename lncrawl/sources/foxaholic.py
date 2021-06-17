# -*- coding: utf-8 -*-
import json
import logging
import re
from urllib.parse import urlparse
from ..utils.crawler import Crawler
from ..utils.cleaner import cleanup_text

logger = logging.getLogger(__name__)
search_url = 'https://www.foxaholic.com/?s=%s&post_type=wp-manga'
chapter_list_url = 'https://www.foxaholic.com/wp-admin/admin-ajax.php'


class FoxaholicCrawler(Crawler):
    base_url = 'https://www.foxaholic.com/'

    def search_novel(self, query):
        query = query.lower().replace(' ', '+')
        soup = self.get_soup(search_url % query)

        results = []
        for tab in soup.select('.c-tabs-item__content'):
            a = tab.select_one('.post-title h3 a')
            latest = tab.select_one('.latest-chap .chapter a').text
            status = tab.select_one('.mg_release .summary-content a')
            results.append({
                'title': a.text.strip(),
                'url': self.absolute_url(a['href']),
                'info': '%s | Status: %s' % (latest, status.text.strip()),
            })
        # end for

        return results
    # end def

    def read_novel_info(self):
        '''Get novel title, autor, cover etc'''
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)

        self.novel_title = soup.select_one(
            'meta[property="og:title"]')['content']
        logger.info('Novel title: %s', self.novel_title)

        self.novel_cover = self.absolute_url(
            soup.select_one('.summary_image a img')['data-src'])
        logger.info('Novel cover: %s', self.novel_cover)

        self.novel_author = ' '.join([
            a.text.strip()
            for a in soup.select('.author-content a[href*="novel-author"]')
        ])
        logger.info('%s', self.novel_author)

        self.novel_id = soup.select_one('#manga-chapters-holder')['data-id']
        logger.info('Novel id: %s', self.novel_id)

        response = self.submit_form(
            chapter_list_url, data='action=manga_get_chapters&manga=' + self.novel_id)
        soup = self.make_soup(response)
        for a in reversed(soup.select('.wp-manga-chapter a')):
            chap_id = len(self.chapters) + 1
            vol_id = 1 + len(self.chapters) // 100
            if chap_id % 100 == 1:
                self.volumes.append({'id': vol_id})
            # end if
            self.chapters.append({
                'id': chap_id,
                'volume': vol_id,
                'title': a.text.strip(),
                'url':  self.absolute_url(a['href']),
            })
        # end for
    # end def

    @cleanup_text
    def download_chapter_body(self, chapter):
        '''Download body of a single chapter and return as clean html format.'''
        logger.info('Visiting %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        contents = soup.select('.reading-content p') 
        all_imgs = soup.find_all('img')
        for img in all_imgs:
            if img.has_attr('loading'):
                src_url = img['src']
                parent = img.parent
                img.decompose()
                new_tag = soup.new_tag("img", src=src_url)
                parent.append(new_tag)
        return ''.join([str(p) for p in contents])
    # end def
# end class