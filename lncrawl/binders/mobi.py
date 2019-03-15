#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import subprocess

from ..utils.kindlegen_download import download_kindlegen, retrieve_kindlegen

logger = logging.getLogger('MOBI_BINDER')


def epub_to_mobi(kindlegen, epub_file):
    if not os.path.exists(epub_file):
        return None
    # end if

    epub_path = os.path.dirname(epub_file)
    input_path = os.path.dirname(epub_path)
    mobi_path = os.path.join(input_path, 'mobi')
    epub_file_name = os.path.basename(epub_file)
    mobi_file_name = epub_file_name.replace('.epub', '.mobi')
    mobi_file_in_epub_path = os.path.join(epub_path, mobi_file_name)
    mobi_file = os.path.join(mobi_path, mobi_file_name)
    logger.debug('Binding %s', mobi_file)

    try:
        isdebug = os.getenv('debug_mode') == 'yes'
        with open(os.devnull, 'w') as dumper:
            logger.debug('')
            subprocess.call(
                [kindlegen, epub_file],
                stdout=None if isdebug else dumper,
                stderr=None if isdebug else dumper,
            )
        # end with
    except Exception:
        import traceback        
        logger.debug(traceback.format_exc())
    # end try

    if os.path.exists(mobi_file_in_epub_path):
        os.makedirs(mobi_path, exist_ok=True)
        if os.path.exists(mobi_file):
            os.remove(mobi_file)
        # end if
        os.rename(mobi_file_in_epub_path, mobi_file)
        print('Created: %s' % mobi_file_name)
        return mobi_file_name
    else:
        logger.error('Failed to generate mobi for %s', epub_file_name)
        return None
    # end if
# end def


def make_mobis(app, epubs):
    kindlegen = retrieve_kindlegen()
    if not kindlegen:
        # if app.bot.should_fetch_kindlegen():
        download_kindlegen()
        kindlegen = retrieve_kindlegen()
        if not kindlegen:
            logger.error('Mobi files were not generated')
            return
        # end if
    # end if

    mobi_files = []
    for epub in epubs:
        file = epub_to_mobi(kindlegen, epub)
        if file:
            mobi_files.append(file)
        # end if
    # end for
    return mobi_files
# end def
