# -*- coding: utf-8 -*-
import logging

from bs4.element import Tag
from lncrawl.core.crawler import Crawler

logger = logging.getLogger(__name__)


class TravisTranslations(Crawler):
    base_url = 'https://travistranslations.com/'

    def read_novel_info(self):
        soup = self.get_soup(self.novel_url)

        possible_title = soup.select_one('.novel-info h1[title]')
        assert isinstance(possible_title, Tag)
        self.novel_title = possible_title['title']
        logger.info('Novel title: %s', self.novel_title)

        possible_cover = soup.select_one('meta[property="og:image"]')
        if isinstance(possible_cover, Tag):
            self.novel_cover = self.absolute_url(possible_cover['content'])
        # end if
        logger.info('Novel cover: %s', self.novel_cover)

        possible_author = soup.select_one('.novel-info .author')
        if isinstance(possible_author, Tag):
            self.novel_author = possible_author.text.strip()
        # end if
        logger.info('Novel author: %s', self.novel_author)

        for a in soup.select('ul.releases li a'):
            chap_id = 1 + len(self.chapters)
            vol_id = 1 + len(self.chapters) // 100
            if chap_id % 100 == 1:
                self.volumes.append({'id': vol_id})
            # end if

            title = None
            possible_chapter_title = a.select_one('span')
            if isinstance(possible_chapter_title, Tag):
                title = possible_chapter_title.text.strip()
            # end if

            self.chapters.append({
                'id': chap_id,
                'volume': vol_id,
                'title': title,
                'url': self.absolute_url(a['href']),
            })
        # end for
    # end def

    def download_chapter_body(self, chapter):
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])

        para = []
        for span in soup.select('p > span[style="font-weight: 400;"]'):
            text = span.text.strip()
            if text:
                para.append(f'<p>{text}</p>')
            # end if
        # end for

        return '\n'.join(para)
    # end def
# end class
