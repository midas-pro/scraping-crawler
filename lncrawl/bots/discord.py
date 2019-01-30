#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
import logging
import asyncio
import discord

from ..core.app import App
from ..spiders import crawler_list
from ..utils.uploader import upload

logger = logging.getLogger('DISCORD_BOT')


class DiscordBot(discord.Client):
    # Store user message handlers
    handlers = dict()

    def start_bot(self):
        self.run(os.getenv('DISCORD_TOKEN'))
    # end def

    @asyncio.coroutine
    async def on_ready(self):
        logger.warn('Discord bot in online!')
        await self.change_presence(
            game=discord.Game(name="above the clouds")
        )
    # end def

    @asyncio.coroutine
    async def on_message(self, message):
        if message.author == self.user:
            return  # I am not crazy to talk with myself
        # end if
        if message.author.bot:
            return  # Other bots are not edible
        # end if
        if message.channel.is_private:
            await self.handle_message(message)
        elif message.content == '!lncrawl':
            await self.handle_message(message)
        elif message.content == '!help':
            await self.public_help(message)
        else:
            return  # It goes over the head
        # end if
    # end def

    async def public_help(self, message):
        await self.send_message(
            message.channel,
            'Enter `!lncrawl` to start a new session of **Lightnovel Crawler**'
        )
    # end def

    async def handle_message(self, message):
        user = message.author
        handler = self.init_handler(user.id)
        await handler.process(message)
    # end def

    def init_handler(self, uid):
        if not self.handlers.get(uid):
            self.handlers[uid] = MessageHandler(self)
        # end if
        return self.handlers.get(uid)
    # end def
# end def


class MessageHandler:
    def __init__(self, client):
        self.app = App()
        self.client = client
        self.state = None
        self.executors = ThreadPoolExecutor(1)
    # end def

    def destroy(self):
        self.client.handlers.pop(self.user.id)
        self.app.destroy()
        self.executors.shutdown()
        shutil.rmtree(self.app.output_path, ignore_errors=True)
    # end def

    @asyncio.coroutine
    async def send(self, *contents):
        for text in contents:
            if not text:
                continue
            await self.client.send_message(self.user, text)
        # end for
    # end def

    @asyncio.coroutine
    async def process(self, message):
        self.message = message
        self.user = message.author
        if not self.state:
            await self.send(
                '-' * 80 + '\n' +
                ('Hello %s\n' % self.user.name) +
                '*Lets make reading lightnovels great again!*\n' +
                '-' * 80 + '\n'
            )
            self.state = self.get_novel_url
        # end if
        await self.state()
    # end def

    async def get_novel_url(self):
        await self.send(
            'I recognize these two categories:\n'
            '- Profile page url of a lightnovel.\n'
            '- A query to search your lightnovel.',
            'What are you looking for?'
        )
        self.state = self.handle_novel_url
    # end def

    async def handle_novel_url(self):
        try:
            self.app.user_input = self.message.content.strip()
            self.app.init_search()
        except:
            await self.send(
                'Sorry! I only know these sources:\n' +
                '\n'.join(['- %s' % x for x in crawler_list.keys()]),
                'Enter something again.')
        # end try

        if self.app.crawler:
            await self.send('Got your page link')
            await self.get_novel_info()
        else:
            await self.send('Got your query: "%s"' % self.app.user_input)
            await self.crawlers_to_search()
        # end if
    # end def

    async def crawlers_to_search(self):
        await self.send(
            ('I have %d sources to search your novel:\n' % len(self.app.crawler_links)) +
            '\n'.join([
                '%d. <%s>' % (i + 1, url)
                for i, url in enumerate(self.app.crawler_links)
            ]) + '\n' +
            'Enter name of index of the site you want to search, '
            'or send `!all` to search in all of them.'
        )
        self.state = self.handle_crawlers_to_search
    # end def

    async def handle_crawlers_to_search(self):
        text = self.message.content.strip()
        if text == '!cancel':
            await self.get_novel_url()
            return
        # end if

        selected = []
        if text == '!all':
            selected = self.app.crawler_links
        else:
            for i, url in enumerate(self.app.crawler_links):
                if str(i + 1) == text:
                    selected.append(url)
                elif text.isdigit() or len(text) < 3:
                    pass
                elif url.find(text) != -1:
                    selected.append(url)
                # end if
            # end for
        # end if

        if len(selected) == 0:
            await self.send('Sorry! I do not have it on my list')
            await self.crawlers_to_search()
            return
        # end if

        self.app.crawler_links = selected
        await self.send(
            ('Great! You have selected %d source:\n' % len(selected)) +
            '\n'.join([
                '- <%s>' % x for x in selected
            ]) + '\n' +
            'I will start searching immediately.'
        )

        try:
            self.app.search_novel()
        except:
            pass
        # end try

        if len(self.app.search_results) == 0:
            await self.send(
                ('Sorry! Nothing found by "%s"\n' % self.app.user_input) +
                'Send !cancel to enter your novel again.'
            )
            await self.crawlers_to_search()
        elif len(self.app.search_results) == 1:
            title, url = self.app.search_results[0]
            await self.send('Found one: **%s** (%s)' % (title, url))
            self.app.init_crawler(url)
            await self.get_novel_info()
        else:
            await self.send(
                ("Found %d novels:\n" % len(self.app.search_results)) +
                '\n'.join([
                    '%d. %s (<%s>)' % (i + 1, title, url)
                    for i, (title, url) in enumerate(self.app.search_results)
                ]) + '\n' +
                'Which one is your novel? Enter the index or the title.'
            )
            self.state = self.handle_search_result
        # end def
    # end def

    async def handle_search_result(self):
        text = self.message.content.strip()
        if text == '!cancel':
            await self.get_novel_url()
            return
        # end if

        selected = []
        for i, (title, url) in enumerate(self.app.search_results):
            if str(i + 1) == text:
                selected.append(url)
            elif text.isdigit() or len(text) < 3:
                pass
            elif title.find(text) != -1:
                selected.append(url)
            elif url.find(text) != -1:
                selected.append(url)
            # end if
        # end for

        if len(selected) != 1:
            await self.send('Sorry! We could not identify which one you want to download')
        else:
            await self.send('Selected: %s' % selected[0])
            self.app.init_crawler(selected[0])
            await self.get_novel_info()
        # end if
    # end def

    async def get_novel_info(self):
        if not self.app.crawler:
            await self.send('Could not find any crawler to get your novel')
            self.state = self.get_novel_info
            return
        # end if

        # TODO: Handle login here

        await self.send('Getting information about your novel')
        self.app.get_novel_info()

        # Setup output path
        good_name = os.path.basename(self.app.output_path)
        output_path = os.path.abspath(
            os.path.join('.discord_bot_output', str(self.user.id), good_name))
        if os.path.exists(output_path):
            shutil.rmtree(output_path, ignore_errors=True)
        # end if
        os.makedirs(output_path, exist_ok=True)
        self.app.output_path = output_path

        # Get chapter range
        await self.send('It has %d volumes and %d chapters.' % (
            len(self.app.crawler.volumes),
            len(self.app.crawler.chapters)
        ))

        await self.display_range_selection()
    # end def

    async def display_range_selection(self):
        await self.send('\n'.join([
            'Now you can send the following commands to modify what to download:',
            '- To download everything send `!all` or pass `!cancel` to stop.',
            '- Send `!last` followed by a number to download last few chapters. '
            'If it does not followed by a number, last 50 chapters will be downloaded.',
            '- Similarly you can send `!first` followed by a number to get first few chapters.',
            '- Send `!volume` followed by volume numbers to download.',
            '- To download a range of chatpers, Send `!chapter` followed by ' +
            'two chapter numbers or urls separated by *space*. ' +
            ('Chapter number must be between 1 and %d, ' % len(self.app.crawler.chapters)) +
            ('and chapter urls should be from <%s>.' %
             (self.app.crawler.home_url))
        ]))
        self.state = self.handle_range_selection
    # end def

    async def handle_range_selection(self):
        text = self.message.content.strip()
        if text.startswith('!cancel'):
            await self.get_novel_url()
            return
        # end if
        if text.startswith('!all'):
            self.app.chapters = self.app.crawler.chapters[:]
        elif text.startswith('!first'):
            n = text.split(' ')[-1]
            n = int(n) if n.isdigit() else 50
            n = 50 if n < 0 else 50
            self.app.chapters = self.app.crawler.chapters[:n]
        elif text.startswith('!last'):
            n = text.split(' ')[-1]
            n = int(n) if n.isdigit() else 50
            n = 50 if n < 0 else 50
            self.app.chapters = self.app.crawler.chapters[-n:]
        elif text.startswith('!volume'):
            text = text[len('!volume'):].strip()
            selected = re.findall(r'\d+', text)
            await self.send(
                'Selected volumes: ' + ', '.join(selected),
            )
            selected = [int(x) for x in selected]
            self.app.chapters = [
                chap for chap in self.app.crawler.chapters
                if selected.count(chap['volume']) > 0
            ]
        elif text.startswith('!chapter'):
            text = text[len('!chapter'):].strip()
            pair = text.split(' ')
            if len(pair) == 2:
                def resolve_chapter(name):
                    cid = 0
                    if name.isdigit():
                        cid = int(str)
                    else:
                        cid = self.app.crawler.get_chapter_index_of(name)
                    # end if
                    return cid - 1
                # end def                   
                first = resolve_chapter(pair[0])
                second = resolve_chapter(pair[1])
                if first > second:
                    second, first = first, second
                # end if
                if first >= 0 or second < len(self.app.crawler.chapters):
                    self.app.chapters = self.app.crawler.chapters[first:second]
                # end if
            # end if
            if len(self.app.chapters) == 0:
                await self.send('Chapter range is not valid. Please try again')
                return
            # end if
        else:
            await self.send('Sorry! I did not recognize your input. Please try again')
            return
        # end if

        if len(self.app.chapters) == 0:
            await self.send('You have not selected any chapters. Please select at least one')
            return
        # end if

        await self.send(
            'Received your request. Starting download...\n' +
            'Send anthing to view status, or `!cancel` to cancel it'
        )

        self.state = self.report_download_progress
        await self.start_download()
    # end def

    async def start_download(self):
        self.app.pack_by_volume = False

        await self.send('\n'.join([
            'Downloading **%s**' % self.app.crawler.novel_title,
            'I will not respond untill I am done.',
            'So sit tight and wait patiently.',
        ]))
        self.app.start_download()
        await self.send(
            '%d out of %d chapters has been downloaded.'
            % (self.app.progress, len(self.app.chapters))
        )

        await self.send('Binding books...')
        self.app.bind_books()
        await self.send('Book binding completed.')

        await self.send('Compressing output folder...')
        self.app.compress_output()
        await self.send('Compressed output folder.')
        
        for archive in self.app.archived_outputs:
            file_size = os.stat(archive).st_size
            if file_size > 7.99 * 1024 * 1024:
                link_id = upload(archive)
                if link_id:
                    await self.send('https://drive.google.com/open?id=%s' % link_id)
                else:
                    await self.send(
                        'The compressed file is above 8MB in size which exceeds Discord\'s limitation.\n'
                        'Can not upload your file.\n',
                        'I am trying my best to come up with an alternative.\n'
                        'It will be available in near future.\n'
                        'Sorry for the inconvenience.'
                    )
                # end if
            else:
                k = 0
                while(file_size > 1024 and k < 3):
                    k += 1
                    file_size /= 1024.0
                # end while

                await self.send('Uploading file... %d%s' % (
                    int(file_size * 100) / 100.0,
                    ['B', 'KB', 'MB', 'GB'][k]
                ))
                await self.client.send_file(
                    self.user,
                    open(archive, 'rb'),
                    filename=os.path.basename(archive),
                    content='Here you go!'
                )
            # end if
        # end for

        self.destroy()
    # end def

    async def report_download_progress(self):
        text = self.message.content.strip()

        if text == '!cancel':
            await self.send('Closing the session')
            self.destroy()
            await self.send('Session is now closed. Type *anything* to create a new one.')
        # end if

        await self.send('Send `!cancel` to stop')
    # end def
# end class
