import logging
from enum import Enum
from typing import List

from bs4 import Tag
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver.webelement import WebElement as _WebElement

from ..core.soup import SoupMaker
from . import scripts

logger = logging.getLogger(__name__)


__all__ = [
    "EC",
    "By",
    "Command",
    "WebElement",
]


# from selenium.webdriver.common.by import By
class By(str, Enum):
    ID = "id"
    XPATH = "xpath"
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"
    NAME = "name"
    TAG_NAME = "tag name"
    CLASS_NAME = "class name"
    CSS_SELECTOR = "css selector"

    def __str__(self) -> str:
        return self.value


class WebElement(_WebElement):
    def __init__(self, parent, id_):
        super().__init__(parent, id_)

    @property
    def _soup_maker(self) -> SoupMaker:
        if hasattr(self._parent, "_soup_maker"):
            maker = getattr(self._parent, "_soup_maker")
            if isinstance(maker, SoupMaker):
                return maker
        return SoupMaker()

    @property
    def inner_html(self) -> str:
        return self.get_attribute("innerHTML")

    @property
    def outer_html(self) -> str:
        return self.get_attribute("outerHTML")

    def as_tag(self) -> Tag:
        html = self.outer_html
        if not hasattr(self, "_tag") or self._html != html:
            self._html = html
            self._tag = self._soup_maker.make_tag(html)
        return self._tag

    def find_all(self, selector: str, by: By = By.CSS_SELECTOR) -> List["WebElement"]:
        if isinstance(by, By):
            by = str(by)
        return self.find_elements(by, selector)

    def find(self, selector: str, by: By = By.CSS_SELECTOR) -> "WebElement":
        if isinstance(by, By):
            by = str(by)
        return self.find_element(by, selector)

    def remove(self):
        self.parent.execute_script(scripts.remove_element, self)

    def scroll_into_view(self):
        self.parent.execute_script(scripts.scroll_into_view_if_needed, self)


def _add_virtual_authenticator(chrome: WebDriver):
    try:
        from selenium.webdriver.common.virtual_authenticator import (
            Transport,
            VirtualAuthenticatorOptions,
        )

        auth_options = VirtualAuthenticatorOptions()
        auth_options.transport = Transport.INTERNAL
        auth_options.has_user_verification = True
        auth_options.is_user_verified = True
        auth_options.is_user_consenting = True
        chrome.add_virtual_authenticator(auth_options)
    except Exception as e:
        logger.debug("Could not attach a virtual authenticator | %s", e)
