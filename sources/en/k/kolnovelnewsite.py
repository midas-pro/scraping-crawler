# -*- coding: utf-8 -*-
import json
import logging
import re
from urllib.parse import urlparse
from lncrawl.core.crawler import Crawler

logger = logging.getLogger(__name__)
search_url = 'https://newsite.kolnovel.com/?s=%s&post_type=wp-manga'
chapter_list_url = 'https://newsite.kolnovel.com/wp-admin/admin-ajax.php'


class kolnovelnewsite(Crawler):
    base_url = 'https://newsite.kolnovel.com/'

    def search_novel(self, query):
        query = query.lower().replace(' ', '+')
        soup = self.get_soup(search_url % query)

        results = []
        for tab in soup.select('.c-tabs-item__content'):
            a = tab.select_one('.post-title h3 a')
            latest = tab.select_one('.latest-chap .chapter a').text
            votes = tab.select_one('.rating .total_votes').text
            results.append({
                'title': a.text.strip(),
                'url': self.absolute_url(a['href']),
                'info': '%s | Rating: %s' % (latest, votes),
            })
        # end for

        return results
    # end def

    def read_novel_info(self):
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)

        possible_title = soup.select_one('.post-title h1')
        for span in possible_title.select('span'):
            span.extract()
        # end for
        self.novel_title = possible_title.text.strip()
        logger.info('Novel title: %s', self.novel_title)

        possible_image = soup.select_one('.summary_image a img')
        if possible_image:
            self.novel_cover = self.absolute_url(possible_image['src'])
        logger.info('Novel cover: %s', self.novel_cover)

        self.novel_author = ' '.join([
            a.text.strip()
            for a in soup.select('.author-content a[href*="manga-author"]')
        ])
        logger.info('%s', self.novel_author)

        self.novel_id = soup.select_one('#manga-chapters-holder')['data-id']
        logger.info('Novel id: %s', self.novel_id)

        response = self.submit_form(chapter_list_url, data={
            'action': 'manga_get_chapters',
            'manga': self.novel_id,
        })
        soup = self.make_soup(response)
        for a in reversed(soup.select(".wp-manga-chapter a")):
            chap_id = len(self.chapters) + 1
            vol_id = 1 + len(self.chapters) // 100
            if chap_id % 100 == 1:
                self.volumes.append({"id": vol_id})
            # end if
            self.chapters.append(
                {
                    "id": chap_id,
                    "volume": vol_id,
                    "title": a.text.strip(),
                    "url": self.absolute_url(a["href"]),
                }
            )
        # end for

    # end def

    def download_chapter_body(self, chapter):
        soup = self.get_soup(chapter['url'])
        contents = soup.select('.reading-content p')
        return ''.join([str(p) for p in contents])
    # end def
# end class