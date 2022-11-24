# -*- coding: utf-8 -*-
"""
# TODO: Read the TODOs carefully and remove all existing comments in this file.

This is a sample using the OptionalVolumeSoupTemplate as the template.
It provides a wrapper around the ChapterWithVolumeSoupTemplate that makes the
volume list generation optional.

Put your source file inside the language folder. The `en` folder has too many
files, therefore it is grouped using the first letter of the domain name.
"""
import logging
from typing import Generator

from bs4 import BeautifulSoup, Tag

from lncrawl.models import Chapter, Volume
from lncrawl.templates.soup.optional_volume import OptionalVolumeSoupTemplate

logger = logging.getLogger(__name__)


# TODO: You can safely delete all [OPTIONAL] methods if you do not need them.
class MyCrawlerName(OptionalVolumeSoupTemplate):
    # TODO: [REQUIRED] Provide the URLs supported by this crawler.
    base_url = ["http://sample.url/"]

    # TODO: [OPTIONAL] Set True if this crawler is for manga/manhua/manhwa.
    has_manga = False

    # TODO: [OPTIONAL] Set True if this source contains machine translations.
    has_mtl = False

    # TODO: [OPTIONAL] This is called before all other methods.
    def initialize(self) -> None:
        # You can customize `TextCleaner` and other necessary things.
        pass

    # TODO: [OPTIONAL] This is called once per session before searching and fetching novel info.
    def login(self, username_or_email: str, password_or_token: str) -> None:
        # Examples:
        # - https://github.com/dipu-bd/lightnovel-crawler/blob/master/sources/multi/mtlnovel.py
        # - https://github.com/dipu-bd/lightnovel-crawler/blob/master/sources/multi/ranobes.py
        pass

    # TODO: [OPTIONAL] If it is necessary to logout after session is finished, you can implement this.
    def logout(self):
        pass

    # TODO: [REQUIRED] Parse and return the novel title
    def parse_title(self, soup: BeautifulSoup) -> str:
        # The soup here is the result of `self.get_soup(self.novel_url)`
        pass

    # TODO: [REQUIRED] Parse and return the novel cover
    def parse_cover(self, soup: BeautifulSoup) -> str:
        # The soup here is the result of `self.get_soup(self.novel_url)`
        pass

    # TODO: [REQUIRED] Parse and return the novel authors
    def parse_authors(self, soup: BeautifulSoup) -> Generator[str, None, None]:
        # The soup here is the result of `self.get_soup(self.novel_url)`
        #
        # Example 1: <a single author example>
        #   tag = soup.find("strong", string="Author:")
        #   assert tag
        #   yield tag.next_sibling.text.strip()
        #
        # Example 2: <multiple authors example>
        #   for a in soup.select(".m-imgtxt a[href*='/authors/']"):
        #       yield a.text.strip()
        pass

    # TODO: [OPTIONAL] Select volume list item tags from the page soup
    def select_volume_tags(self, soup: BeautifulSoup) -> Generator[Tag, None, None]:
        # The soup here is the result of `self.get_soup(self.novel_url)`
        #
        # Example: yield from soup.select("#toc .vol-item")
        pass

    # TODO: [OPTIONAL] Parse a single volume from volume list item tag
    def parse_volume_item(self, tag: Tag, id: int) -> Volume:
        # The tag here is either `html` or comes from `self.select_volume_tags`
        # The id here is the next available volume id.
        #
        # Example:
        # return Volume(
        #     id=id,
        #     title= tag.text.strip(),
        # )
        pass

    # TODO: [REQUIRED] Select chapter list item tags from volume tag and page soup
    def select_chapter_tags(self, tag: Tag) -> Generator[Tag, None, None]:
        # The tag here is either `html` or comes from `self.select_volume_tags`
        #
        # Example: yield from tag.select(".chapter-item")
        pass

    # TODO: [REQUIRED] Parse a single chapter from chapter list item tag
    def parse_chapter_item(self, tag: Tag, id: int, vol: Volume) -> Chapter:
        # The tag here comes from `self.select_chapter_tags`
        # The vol here comes from `self.parse_volume_item`
        # The id here is the next available chapter id
        #
        # Example:
        # return Chapter(
        #     id=id,
        #     volume=vol.id,
        #     title=tag.text.strip(),
        #     url=self.absolute_url(tag["href"]),
        # )
        pass
        raise NotImplementedError()

    # TODO: [REQUIRED] Select the tag containing the chapter text
    def select_chapter_body(self, soup: BeautifulSoup) -> Tag:
        # The soup here is the result of `self.get_soup(chapter.url)`
        #
        # Example: return soup.select_one(".m-read .txt")
        pass

    # TODO: [OPTIONAL] Return the index in self.chapters which contains a chapter URL
    def index_of_chapter(self, url: str) -> int:
        # To get more help, check the default implemention in the `Crawler` class.
        pass
