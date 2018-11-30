#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains methods for binding novel or manga into epub and mobi"""
import re
import io
import os
import errno
import logging
import platform
import subprocess
from ebooklib import epub
from progress.spinner import Spinner

logger = logging.getLogger('BINDER')


def bind_epub_book(app, chapters, volume=''):
    bool_title = (app.crawler.novel_title + ' ' + volume).strip()
    logger.debug('Binding %s.epub', bool_title)
    # Create book
    book = epub.EpubBook()
    book.set_language('en')
    book.set_title(bool_title)
    book.add_author(app.crawler.novel_author)
    book.set_identifier(app.output_path + volume)
    # Create book spine
    if app.book_cover:
        book.set_cover('image.jpg', open(app.book_cover, 'rb').read())
        book.spine = ['cover', 'nav']
    else:
        book.spine = ['nav']
    # end if
    # Make contents
    book.toc = []
    for i, chapter in enumerate(chapters):
        xhtml_file = 'chap_%s.xhtml' % str(i + 1).rjust(5, '0')
        content = epub.EpubHtml(
            lang='en',
            uid=str(i + 1),
            file_name=xhtml_file,
            title=chapter['title'],
            content=chapter['body'] or '',
        )
        book.add_item(content)
        book.toc.append(content)
    # end for
    book.spine += book.toc
    book.add_item(epub.EpubNav())
    book.add_item(epub.EpubNcx())
    # Save epub file
    epub_path = os.path.join(app.output_path, 'epub')
    file_path = os.path.join(epub_path, bool_title + '.epub')
    logger.debug('Writing %s', file_path)
    os.makedirs(epub_path, exist_ok=True)
    epub.write_epub(file_path, book, {})
    logger.warn('Created: %s.epub', bool_title)
    return file_path
# end def


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
    logger.debug('Binding %s.epub', mobi_file)

    try:
        devnull = open(os.devnull, 'w')
        subprocess.call(
            [kindlegen, epub_file],
            stdout=devnull,
            stderr=devnull,
        )
    except Exception as err:
        logger.debug(err)
        pass
    # end try

    if os.path.exists(mobi_file_in_epub_path):
        os.makedirs(mobi_path, exist_ok=True)
        if os.path.exists(mobi_file):
            os.remove(mobi_file)
        # end if
        os.rename(mobi_file_in_epub_path, mobi_file)
        logger.warn('Created: %s', mobi_file_name)
        return mobi_file_name
    else:
        logger.error('Failed to generate mobi for %s', epub_file_name)
        return None
    # end if
# end def


def bind_html_chapter(chapter, prev_chapter, next_chapter):
    with open(os.path.join(os.path.dirname(__file__), 'html_style.css')) as f:
        style = f.read()
    # end with
    prev_button = '%s.html' % (str(prev_chapter['id']).rjust(5, '0')) if prev_chapter else '#'
    next_button = '%s.html' % str(next_chapter['id']).rjust(5, '0') if next_chapter else '#'
    button_group = '''<div class="link-group">
        <a class="btn" href="%s">Previous</a>
        <a href="%s" target="_blank">Original Source</a>
        <a class="btn" href="%s">Next</a>
    </div>''' % (prev_button, chapter['url'], next_button)

    html = '<!DOCTYPE html>\n'
    html += '<html>\n<head>'
    html += '<meta charset="utf-8"/>'
    html += '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
    html += '<title>%s</title>' % chapter['title']
    html += '<style>%s</style>' % style
    html += '</head>\n<body>\n<div id="content">\n'
    html += button_group
    html += ('<main>%s</main>' % chapter['body']) if len(chapter['body']) \
        else '<p style="text-align: center">No content was found</p>'
    html += button_group
    html += '\n</div>\n</body>\n</html>'

    file_name = '%s.html' % str(chapter['id']).rjust(5, '0')
    return html, file_name
# end def

#-------------------------------------------------------------------------------------------------#
def manga_to_kindle(input_path):
    '''Convert crawled data to epub'''
    manga_id = os.path.basename(input_path)
    output_path = manga_id
    name = ' '.join([x.capitalize() for x in manga_id.split('_')])
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # end if
    subprocess.call(['kcc-c2e',
          '-p', 'KPW',
          # '--forcecolor',
          # '-f', 'EPUB',
          '-t', name,
          '-o', output_path,
          input_path])
# end def
