# -*- coding: utf-8 -*-
import json
import logging
import re
from urllib.parse import quote
from ..utils.crawler import Crawler

logger = logging.getLogger(__name__)
search_url = 'https://id.mtlnovel.com/wp-admin/admin-ajax.php?action=autosuggest&q=%s'


class IdMtlnovelCrawler(Crawler):
    base_url = 'https://id.mtlnovel.com/'

    def search_novel(self, query):
        query = quote(query.lower())
        list_url = search_url % query
        data = self.get_json(list_url)['items'][0]['results']

        results = []
        for item in data[:20]:
            url = item['permalink']
            results.append({
                'url': url,
                'title': re.sub(r'</?strong>', '', item['title']),
            })
        # end for

        return results
    # end def

    def read_novel_info(self):
        '''Get novel title, autor, cover etc'''
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)

        self.novel_title = soup.select_one('h1.entry-title').text.strip()
        logger.info('Novel title: %s', self.novel_title)

        self.novel_cover = self.absolute_url(
            soup.select('div.nov-head amp-img')[1]['src'])
        logger.info('Novel cover: %s', self.novel_cover)

        author_elem = soup.select('table.info tr')[3].find('a')
        if author_elem:
            self.novel_author = soup.select('table.info tr')[3].find('a').text
        else:
            self.novel_author = "Unknown"
        logger.info('Novel author: %s', self.novel_author)

        chapter_list = soup.select('div.ch-list amp-list')

        for item in chapter_list:
            data = self.get_json(item['src'])
            for chapter in data['items']:
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
                    'url':  chapter['permalink'],
                    'title': chapter['no'] + " " + chapter['title'] or ('Chapter %d' % chap_id),
                })
            # end for
        # end for
    # end def

    def download_chapter_body(self, chapter):
        '''Download body of a single chapter and return as clean html format.'''
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])

        logger.debug(soup.title.string)

        contents = soup.select('div.par p')
        # print(contents)
        # for p in contents:
        #    for span in p.findAll('span'):
        #        span.unwrap()
        # end for
        # end for
        # print(contents)
        # self.clean_contents(contents)
        #body = contents.select('p')
        body = [str(p) for p in contents if p.text.strip()]
        return '<p>' + '</p><p>'.join(body) + '</p>'
    # end def
# end class
