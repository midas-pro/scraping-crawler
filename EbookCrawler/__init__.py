#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main point of execution"""
import sys
from .lnmtl import LNMTLCrawler
from .wuxia import WuxiaCrawler
from .webnovel import WebNovelCrawler
from .readln import ReadLightNovelCrawler


def main():
    '''main method to call'''
    if len(sys.argv) < 3:
        return show_help()
    # end if

    site = sys.argv[1]
    if site == 'wuxia':
        WuxiaCrawler(
            novel_id=sys.argv[2],
            start_chapter=sys.argv[3] if len(sys.argv) > 3 else None,
            end_chapter=sys.argv[4] if len(sys.argv) > 4 else None
        ).start()
    elif site == 'lnmtl':
        LNMTLCrawler(
            novel_id=sys.argv[2],
            start_chapter=sys.argv[3] if len(sys.argv) > 3 else '',
            end_chapter=sys.argv[4] if len(sys.argv) > 4 else ''
        ).start()
    elif site == 'webnovel':
        WebNovelCrawler(
            novel_id=sys.argv[2],
            start_chapter=sys.argv[3] if len(sys.argv) > 3 else '',
            end_chapter=sys.argv[4] if len(sys.argv) > 4 else ''
        ).start()
    elif site == 'readln':
        ReadLightNovelCrawler(
            novel_id=sys.argv[2],
            start_chapter=sys.argv[3] if len(sys.argv) > 3 else '',
            end_chapter=sys.argv[4] if len(sys.argv) > 4 else ''
        ).start()
    else:
        show_help()
    # end if
# end def


def show_help():
    '''displays help'''
    print('EbookCrawler:')
    print('  python . <site-name> <novel-id>',
          '[<start-chapter>|<start-url>]',
          '[<end-chapter>|<end-url>]')
    print()
    print('OPTIONS:')
    print('  site-name*     Site to crawl. Available: lnmtl, wuxia, webnovel, readln.')
    print('  novel-id*      Novel id appear in url (See HINTS)')
    print('  start-chapter  Starting chapter')
    print('  end-chapter    Ending chapter')
    print('  start-url      Url of the chapter to start')
    print('  end-url        Url of the final chapter')
    print()
    print('HINTS:')
    print('- * marked params are required')
    print('- Do not provide any start or end chapter for just book binding')
    print('- Get the `novel-id` from the link. Some examples:')
    print('\n  https://www.webnovel.com/book/8143258106003605/21860374051617214 \n    novel_id = `8143258106003605`')
    print('\n  https://www.wuxiaworld.com/novel/a-will-eternal/awe-chapter-1 \n    novel_id = `a-will-eternal`')
    print('\n  https://lnmtl.com/novel/against-the-gods \n    novel_id = `against-the-gods`')
    print('\n  https://www.readlightnovel.org/tales-of-herding-gods \n    novel_id = `tales-of-herding-gods`')
    print()
# end def
