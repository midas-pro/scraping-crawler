# -*- coding: utf-8 -*-
import json
import logging
import re
from urllib.parse import urlparse
from ..utils.crawler import Crawler

logger = logging.getLogger(__name__)
search_url = (
    "https://noveltranslate.com/?s=%s&post_type=wp-manga&author=&artist=&release="
)
wp_admin_ajax_url = "https://noveltranslate.com/wp-admin/admin-ajax.php"


class NovelTranslateCrawler(Crawler):
    base_url = "https://noveltranslate.com/"

    def search_novel(self, query):
        query = query.lower().replace(" ", "+")
        soup = self.get_soup(search_url % query)

        results = []
        for tab in soup.select(".c-tabs-item__content"):
            a = tab.select_one(".post-title h3 a")
            latest = tab.select_one(".latest-chap .chapter a").text
            votes = tab.select_one(".rating .total_votes").text
            results.append(
                {
                    "title": a.text.strip(),
                    "url": self.absolute_url(a["href"]),
                    "info": "%s | Rating: %s" % (latest, votes),
                }
            )
        # end for

        return results
    # end def

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug("Visiting %s", self.novel_url)
        soup = self.get_soup(self.novel_url)

        possible_title = soup.select_one(".post-title h1")
        for span in possible_title.select("span"):
            span.extract()
        # end for
        self.novel_title = possible_title.text.strip()
        logger.info("Novel title: %s", self.novel_title)

        self.novel_cover = self.absolute_url(
            soup.select_one(".summary_image a img")["src"]
        )
        logger.info("Novel cover: %s", self.novel_cover)

        self.novel_author = " ".join(
            [
                a.text.strip()
                for a in soup.select('.author-content a[href*="manga-author"]')
            ]
        )
        logger.info("%s", self.novel_author)

        self.novel_id = soup.select_one("#manga-chapters-holder")["data-id"]
        logger.info("Novel id: %s", self.novel_id)

        # For getting cookies
        self.submit_form(wp_admin_ajax_url, data={
            'action': 'manga_views',
            'manga': self.novel_id,
        })
        print(self.cookies)
        response = self.submit_form(wp_admin_ajax_url, data={
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
        """Download body of a single chapter and return as clean html format."""
        logger.info("Visiting %s", chapter["url"])
        soup = self.get_soup(chapter["url"])

        contents = soup.select('div.reading-content p')

        body = []
        for p in contents:
            for ad in p.select('.ezoic-adpicker-ad, .ezoic-ad, .ezoic-adl'):
                ad.decompose()
            body.append(str(p))

        return ''.join(body)
    # end def
# end class
