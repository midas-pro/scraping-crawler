#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interactive value input"""
import sys
import logging
import urllib3
from PyInquirer import prompt
from .lnmtl import LNMTLCrawlerApp
from .webnovel import WebnovelCrawlerApp
# from .wuxia import WuxiaCrawler
# from .wuxiac import WuxiaCoCrawler
# from .boxnovel import BoxNovelCrawler
# from .readln import ReadLightNovelCrawler
# from .novelplanet import NovelPlanetCrawler

def configure():
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else None
    if mode == '-v' or mode == '--verbose':
        print('\33[91m 🔊 IN VERBOSE MODE\33[0m')
        print('-' * 60)
        logging.basicConfig(level=logging.DEBUG)
    else:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # end if
# end def

def headline():
    with open('VERSION', 'r') as f:
        version = f.read().strip()
    # end with
    print('-' * 60)
    print(' \33[1m\33[92m📒', 'Ebook Crawler 🍀', version, '\33[0m')
    print(' 🔗\33[94m https://github.com/dipu-bd/site-to-epub', '\33[0m')
    print(' 🙏\33[94m https://saythanks.io/to/dipu-bd', '\33[0m')
    print('-' * 60)
# end def

def main():
    headline()
    configure()

    choices = {
        'https://lnmtl.com': (lambda: LNMTLCrawlerApp().start()),
        'https://www.webnovel.com': (lambda: WebnovelCrawlerApp().start()),
        'https://boxnovel.com': (lambda: print('\n  Not yet implemented  \n')),
        'https://novelplanet.com': (lambda: print('\n  Not yet implemented  \n')),
        'https://www.wuxiaworld.co': (lambda: print('\n  Not yet implemented  \n')),
        'https://www.wuxiaworld.com': (lambda: print('\n  Not yet implemented  \n')),
        'https://www.readlightnovel.org': (lambda: print('\n  Not yet implemented  \n')),
    }

    answer = prompt([
        {
            'type': 'list',
            'name': 'source',
            'message': 'Where is the novel from?',
            'choices': choices.keys(),
        },
    ])
    
    choices[answer['source']]()
# end def

if __name__ == '__main__':
    main()
# end if
