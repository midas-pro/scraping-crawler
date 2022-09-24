import logging
import os

from minify_html import minify

from ..assets.epub import get_css_style

try:
    from ebooklib import epub
except Exception as err:
    logging.fatal("Failed to import `ebooklib`")

logger = logging.getLogger(__name__)


def make_cover_image(app):
    if not (app.book_cover and os.path.isfile(app.book_cover)):
        return None

    logger.info("Creating cover: %s", app.book_cover)
    # ext = app.book_cover.split('.')[-1]
    cover_image = epub.EpubImage()
    cover_image.file_name = "cover.jpg"
    cover_image.media_type = "image/jpeg"
    with open(app.book_cover, "rb") as image_file:
        cover_image.content = image_file.read()

    return cover_image


def make_intro_page(app, cover_image):
    logger.info("Creating intro page")
    github_url = "https://github.com/dipu-bd/lightnovel-crawler"

    html = '<div id="intro">'

    html += """
        <div>
            <h1>%s</h1>
            <h3>%s</h3>
        </div>
    """ % (
        app.crawler.novel_title or "N/A",
        app.crawler.novel_author or app.crawler.home_url,
    )

    if cover_image:
        html += '<img id="cover" src="%s">' % (cover_image.file_name,)

    html += """
    <div>
        <b>Source:</b> <a href="%s">%s</a><br>
        <i>Generated by <b><a href="%s">Lightnovel Crawler</a></b></i>
    </div>""" % (
        app.crawler.novel_url,
        app.crawler.novel_url,
        github_url,
    )

    html += "</div>"
    html += f'<style type="text/css">{get_css_style()}</style>'

    intro = epub.EpubHtml(
        uid="intro",
        file_name="intro.xhtml",
        title="Intro",
        content=minify(html, minify_js=True, minify_css=True),
    )
    return intro


def make_chapters(book, chapters):
    toc = []
    volume = []
    for i, chapter in enumerate(chapters):
        if not chapter["body"]:
            continue

        html = str(chapter["body"])
        html += f'<style type="text/css">{get_css_style()}</style>'
        html = minify(html, minify_js=True, minify_css=True)

        xhtml_file = "chap_%s.xhtml" % str(i + 1).rjust(5, "0")

        # create chapter xhtml file
        content = epub.EpubHtml(
            # uid=str(i + 1),
            content=html,
            file_name=xhtml_file,
            title=chapter["title"],
            direction=book.direction,
        )

        book.add_item(content)
        volume.append(content)
        book.spine.append(content)

        # separate chapters by volume
        if i + 1 == len(chapters) or chapter["volume"] != chapters[i + 1]["volume"]:
            toc.append(
                (
                    epub.Section(chapter["volume_title"], href=volume[0].file_name),
                    tuple(volume),
                )
            )
            volume = []

    book.toc = tuple(toc)


def make_chapter_images(book, image_output_path):
    if not os.path.isdir(image_output_path):
        return

    for filename in os.listdir(image_output_path):
        if not filename.endswith(".jpg"):
            continue

        image_item = epub.EpubImage()
        image_item.media_type = "image/jpeg"
        image_item.file_name = "images/" + filename
        with open(os.path.join(image_output_path, filename), "rb") as fp:
            image_item.content = fp.read()

        book.add_item(image_item)


def bind_epub_book(app, chapters, volume=""):
    book_title = (app.crawler.novel_title + " " + volume).strip()
    logger.debug("Binding epub: %s", book_title)

    # Create book
    book = epub.EpubBook()
    book.set_language("en")
    book.set_title(book_title)
    book.add_author(app.crawler.novel_author)
    book.set_identifier(app.output_path + volume)
    book.set_direction("rtl" if app.crawler.is_rtl else "default")

    # Create intro page
    cover_image = make_cover_image(app)
    if cover_image:
        book.add_item(cover_image)

    intro_page = make_intro_page(app, cover_image)
    book.add_item(intro_page)

    # Create book spine
    try:
        book.set_cover("book-cover.jpg", open(app.book_cover, "rb").read())
        book.spine = ["cover", intro_page, "nav"]
    except Exception:
        book.spine = [intro_page, "nav"]
        logger.warn("No cover image")

    # Create chapters
    make_chapters(book, chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Add chapter images
    image_path = os.path.join(app.output_path, "images")
    make_chapter_images(book, image_path)

    # Save epub file
    epub_path = os.path.join(app.output_path, "epub")
    file_name = app.good_file_name
    if not app.no_append_after_filename:
        file_name += " " + volume

    file_path = os.path.join(epub_path, file_name + ".epub")
    logger.debug("Writing %s", file_path)
    os.makedirs(epub_path, exist_ok=True)
    epub.write_epub(file_path, book, {})
    print("Created: %s.epub" % file_name)
    return file_path


def make_epubs(app, data):
    epub_files = []
    for vol in data:
        if len(data[vol]) > 0:
            book = bind_epub_book(
                app,
                volume=vol,
                chapters=data[vol],
            )
            epub_files.append(book)

    return epub_files
