from typing import Generator

from bs4 import Tag

from ...models import Chapter, Volume
from ..soup.with_volume import ChapterWithVolumeSoupTemplate
from .general import GeneralBrowserTemplate


class ChapterWithVolumeBrowserTemplate(
    GeneralBrowserTemplate, ChapterWithVolumeSoupTemplate
):
    """Attempts to crawl using cloudscraper first, if failed use the browser."""

    def parse_chapter_list_in_browser(self) -> None:
        for vol in self.select_volume_tags_in_browser():
            if not isinstance(vol, Tag):
                continue
            vol_id = len(self.volumes) + 1
            vol_item = self.parse_volume_item_in_browser(vol, vol_id)
            self.volumes.append(vol_item)
            for tag in self.select_chapter_tags_in_browser(vol, vol_item):
                next_id = len(self.chapters) + 1
                item = self.parse_chapter_item_in_browser(tag, next_id, vol_item)
                item.volume = vol_id
                self.chapters.append(item)

    def select_volume_tags_in_browser(self) -> Generator[Tag, None, None]:
        """Select volume list item tags from the browser"""
        return self.select_volume_tags(self.browser.soup)

    def parse_volume_item_in_browser(self, tag: Tag, id: int) -> Volume:
        """Parse a single volume from volume list item tag from the browser"""
        return self.parse_volume_item(tag, id)

    def select_chapter_tags_in_browser(
        self, tag: Tag, vol: Volume
    ) -> Generator[Tag, None, None]:
        """Select chapter list item tags from volume tag from the browser"""
        raise self.select_chapter_tags(tag, vol)

    def parse_chapter_item_in_browser(self, tag: Tag, id: int, vol: Volume) -> Chapter:
        """Parse a single chapter from chapter list item tag from the browser"""
        raise self.parse_chapter_item(tag, id, vol)
