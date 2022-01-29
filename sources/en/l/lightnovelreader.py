# -*- coding: utf-8 -*-
import logging
from urllib.parse import quote

from bs4 import Tag

from lncrawl.core.crawler import Crawler

logger = logging.getLogger(__name__)

novel_search_url = '/search/autocomplete?query=%s'
chapter_load_url = '/novel/load-chapters'

class LightnovelReader(Crawler):
    base_url = [
        'https://lightnovelreader.org/',
        'https://www.lightnovelreader.org/',
    ]

    def search_novel(self, query):
        self.get_response(self.home_url)

        url = self.absolute_url(novel_search_url % quote(query))
        logger.debug('Visiting %s', url)
        data = self.get_json(url)

        results = []
        for item in data['results']:
            results.append({
                'title': str(item['original_title']),
                'url': self.absolute_url(item['link']),
            })
        # end for

        return results
    # end def

    def read_novel_info(self):
        logger.debug('Visiting %s', self.novel_url)

        response = self.get_response(self.novel_url)
        html_text = response.content.decode('utf8', 'ignore')
        html_text = html_text.replace(r'</body>', '').replace(r'</html>', '')
        html_text += '</body></html>'
        soup = self.make_soup(html_text)
        
        possible_title = soup.select_one('.section-header h1')
        assert isinstance(possible_title, Tag)
        self.novel_title = possible_title.text.strip()
        logger.info('Novel title: %s', self.novel_title)

        possible_image = soup.select_one('.container  a[href="#"] img.w-full')
        if isinstance(possible_image, Tag):
            self.novel_cover = self.absolute_url(possible_image['src'])
        # end if
        logger.info('Novel cover: %s', self.novel_cover)

        for tag in soup.select('.container dl.text-xs'):
            dt = tag.select_one('dt')
            dd = tag.select_one('dd')
            if not (isinstance(dt, Tag) and isinstance(dd, Tag)):
                continue
            # end if
            if dt.text.strip() == 'Author(s):':
                self.novel_author = dd.text.strip()
            # end if
        # end for
        logger.info('Novel author: %s', self.novel_author)

        possible_novel_id = soup.select_one('.js-load-chapters')
        assert isinstance(possible_novel_id, Tag)
        novel_id = str(possible_novel_id['data-novel-id']).strip()
        logger.info('# novel id = %s', novel_id)

        response = self.submit_form(
            self.absolute_url(chapter_load_url),
            data='novelId=%s' % novel_id,
            headers={
                'accept': '*/*',
                'x-requested-with': 'XMLHttpRequest',
                'origin': self.home_url.strip('/'),
                'referer': self.novel_url.strip('/'),
            },
        )
        soup = self.make_soup(response)

        volumes = set()
        for a in reversed(soup.select('a')):
            chap_id = len(self.chapters) + 1
            vol_id = len(self.chapters) // 100 + 1
            volumes.add(vol_id)
            self.chapters.append({
                'id': chap_id,
                'volume': vol_id,
                'title': a.text.strip(),
                'url': self.absolute_url(a['href']),
            })
        # end for

        self.volumes = [{'id': x} for x in volumes]
    # end def

    def download_chapter_body(self, chapter):
        response = self.get_response(chapter['url'])
        html_text = response.content.decode('utf8', 'ignore')
        html_text = html_text.replace(r'</body>', '').replace(r'</html>', '')
        html_text += '</body></html>'
        soup = self.make_soup(html_text)

        body = soup.select_one('article#chapterText')
        self.bad_css += ['div[style="display:none"]', 'center p']
        return self.extract_contents(body)
    # end def
# end class
