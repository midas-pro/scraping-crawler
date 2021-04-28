# Lightnovel Crawler [![pip package](https://img.shields.io/badge/%F0%9F%93%A6-pip-blue)](https://pypi.org/project/lightnovel-crawler) [![download win](https://img.shields.io/badge/%E2%A7%AA-lncrawl.exe-red)](https://rebrand.ly/lncrawl) [![download linux](<https://img.shields.io/badge/%E2%A7%AD-lncrawl%20(linux)-brown>)](https://rebrand.ly/lncrawl-linux)

[![Build Status](https://travis-ci.com/dipu-bd/lightnovel-crawler.svg?branch=master)](https://travis-ci.com/dipu-bd/lightnovel-crawler)
[![Python version](https://img.shields.io/pypi/pyversions/lightnovel-crawler.svg)](https://pypi.org/project/lightnovel-crawler)
[![PyPI version](https://img.shields.io/pypi/v/lightnovel-crawler.svg)](https://pypi.org/project/lightnovel-crawler)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/dipu-bd/lightnovel-crawler/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/dipu-bd/lightnovel-crawler)](https://github.com/dipu-bd/lightnovel-crawler)

<!-- [![Build status](https://ci.appveyor.com/api/projects/status/l7ci88f7ae7rxek5?svg=true)](https://ci.appveyor.com/project/dipu-bd/lightnovel-crawler) -->
<!-- [![Downloads](https://pepy.tech/badge/lightnovel-crawler)](https://pepy.tech/project/lightnovel-crawler) -->
<!-- [![Heroku](https://heroku-badge.herokuapp.com/?app=lncrawl)] -->
<!-- [![Snap Status](https://build.snapcraft.io/badge/dipu-bd/lightnovel-crawler.svg)](https://build.snapcraft.io/user/dipu-bd/lightnovel-crawler) -->

An app to download novels from online sources and generate e-books.

> **Discord: [https://discord.gg/wMECG2Q](https://discord.gg/wMECG2Q)**

> **Telegram: [https://t.me/epub_smelter_bot](https://t.me/epub_smelter_bot)**

## Table of contents

- [Lightnovel Crawler ![pip package](https://pypi.org/project/lightnovel-crawler) [![download win](https://img.shields.io/badge/%E2%A7%AA-lncrawl.exe-red)](https://rebrand.ly/lncrawl) [![download linux](<https://img.shields.io/badge/%E2%A7%AD-lncrawl%20(linux)-brown>)](https://rebrand.ly/lncrawl-linux)](#lightnovel-crawler---)
  - [Table of contents](#table-of-contents)
  - [(A) Installation](#a-installation)
    - [A1. Standalone Bundle (Windows, Linux)](#a1-standalone-bundle-windows-linux)
    - [A2. PIP (Windows, Mac, and Linux)](#a2-pip-windows-mac-and-linux)
    - [A3. Termux (Android)](#a3-termux-android)
    - [A4. Chatbots](#a4-chatbots)
      - [A4.1 Discord](#a41-discord)
      - [A4.2 Telegram](#a42-telegram)
    - [A5. Run from source](#a5-run-from-source)
    - [A6. Heroku Deployment](#a6-heroku-deployment)
  - [(B) General Usage](#b-general-usage)
    - [B1. Available options](#b1-available-options)
    - [B2. Example Usage](#b2-example-usage)
    - [B3. Running the bot](#b3-running-the-bot)
  - [(C) Development](#c-development)
    - [C1. Adding new source](#c1-adding-new-source)
    - [C2. Adding new Bot](#c2-adding-new-bot)
    - [C3. Supported sources](#c3-supported-sources)
    - [C4. Rejected sources](#c4-rejected-sources)
    - [C5. Supported output formats](#c5-supported-output-formats)
    - [C6. Supported bots](#c6-supported-bots)

<a href="https://github.com/dipu-bd/lightnovel-crawler"><img src="res/lncrawl-icon.png" width="128px" align="right"/></a>

## (A) Installation

**This application uses _Calibre_ to convert ebooks.** <br>
**Install it from https://calibre-ebook.com/download** <br>
Without it, you will only get output in epub, text, and web formats.

<!-- Also, you have to install **node.js** to access cloudflare enabled sites (e.g. https://novelplanet.com/). Download and install node.js from here: https://nodejs.org/en/download/ -->

### A1. Standalone Bundle (Windows, Linux)

⏬ **Windows**: [lightnovel-crawler v2.24.5 ~ 23MB](https://rebrand.ly/lncrawl)

> In Windows 8, 10 or later versions, it might say that `lncrawl.exe` is not safe to dowload or execute. You should bypass/ignore this security check to execute this program.

_To get older versions visit the [Releases page](https://github.com/dipu-bd/lightnovel-crawler/releases)_

⏬ **Linux**: [lightnovel-crawler v2.24.5 ~ 24MB](https://rebrand.ly/lncrawl-linux)

> Copy it to `/usr/bin` or `~/.local/bin` to make it accessible in terminal. Or, you can [create a launcher](https://askubuntu.com/a/66918/457551) to easily access the app.
> However, it is recommended to use **pip** version directly if you are on Linux

### A2. PIP (Windows, Mac, and Linux)

📦 A python package named `lightnovel-crawler` is available at [pypi](https://pypi.org/project/lightnovel-crawler).

> Make sure you have installed **Python** v3.6 or higher and have **pip** enabled. Visit these links to install python with pip in [Windows](https://stackoverflow.com/a/44437176/1583052), [Linux](https://stackoverflow.com/a/51799221/1583052) and [MacOS](https://itsevans.com/install-pip-osx/). Feel free to ask on the Discord server if you are stuck.

To install this app or to update installed one via `pip`, just run:

```bash
$ pip install --user -U lightnovel-crawler
```

In some cases you have to use `python3 -m pip` or `pip3` or `python -m pip`. And you do not need `--user` option, if you are running from root.

Next, open your terminal and enter:

```bash
$ lightnovel-crawler

# Or, a shortcut:
$ lncrawl
```

> To view extra logs, use: `lncrawl -lll`

### A3. Termux (Android)

> Mobile platforms are unpredictable. It is not guaranteed that the app will run on all devices.
> It is recommended to use the bots on either Discord or Telegram if you are on mobile.

📱 Using Termux, you can run this app in your android phones too. Follow this instructions:

- Install [Termux](https://play.google.com/store/apps/details?id=com.termux) from playstore.
- Open the app and run these commands one by one:
  - `apt update && apt upgrade`
  - `termux-setup-storage`
  - `pkg install ndk-sysroot make python zlib clang`
  - `pkg install libxml2 libxslt libiconv libcrypt libffi zlib libjpeg-turbo`
  - `pkg install nodejs-lts`
  - `pip install -U lightnovel-crawler` to install the latest version of this app.
- Now exit the console and relaunch it.
- Type `cd ~/storage/downloads` to store novels there.
- Type `lncrawl` to start.
- You navigate up using <kbd>Volume UP</kbd> + <kbd>W</kbd> and down using <kbd>Volume UP</kbd> + <kbd>S</kbd>.
- Run `pip install -U lightnovel-crawler` again to install the latest updates.

### A4. Chatbots

#### A4.1 Discord

Join our server: https://discord.gg/7A5Hktx

Or, visit this link to install discord bot to your own server:
https://discordapp.com/oauth2/authorize?client_id=537526751170002946&permissions=51264&scope=bot

#### A4.2 Telegram

Visit this link to get started with the telegram bot:
https://t.me/epub_smelter_bot

Send `!help` to open the bot help message.

### A5. Run from source

- First clone the repository:

```bash
$ git clone https://github.com/dipu-bd/lightnovel-crawler
```

- Open command prompt inside of the project folder and install requirements:

```bash
$ pip install --user -r requirements.txt
```

- Run the program (use python v3.6 or higher):

```bash
$ python __main__.py

# Or, in short,
$ python .
```

### A6. Heroku Deployment

Simply fill out the environment variables and you get a running instance.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## (B) General Usage

### B1. Available options

```bash
$ lncrawl -h
================================================================================
                           📒 Lightnovel Crawler 🍀2.25.0 
                  https://github.com/dipu-bd/lightnovel-crawler 
--------------------------------------------------------------------------------
usage: lncrawl [options...]
       lightnovel-crawler [options...]

optional arguments:
  -h, --help            show this help message and exit

  -v, --version         show program's version number and exit
  -l                    Set log levels. (-l = warn, -ll = info, -lll = debug).
  --list-sources        Display a list of available sources.
  -s URL, --source URL  Profile page url of the novel.
  -q STR, --query STR   Novel query followed by list of source sites.
  -x [REGEX], --sources [REGEX]
                        Filter out the sources to search for novels.
  --login USER PASSWD   User name/email address and password for login.
  --format E [E ...]    Define which formats to output. Default: all.
  --add-source-url      Add source url at the end of each chapter.
  --single              Put everything in a single book.
  --multi               Build separate books by volumes.
  -o PATH, --output PATH
                        Path where the downloads to be stored.
  --filename NAME       Set the output file name
  --filename-only       Skip appending chapter range with file name
  -f, --force           Force replace any existing folder.
  -i, --ignore          Ignore any existing folder (do not replace).
  --all                 Download all chapters.
  --first [COUNT]       Download first few chapters (default: 10).
  --last [COUNT]        Download last few chapters (default: 10).
  --page START STOP.    The start and final chapter urls.
  --range FROM TO.      The start and final chapter indexes.
  --volumes [N [N ...]]
                        The list of volume numbers to download.
  --chapters [URL [URL ...]]
                        A list of specific chapter urls.
  --bot {console,telegram,discord,test}
                        Select a bot. Default: console.
  --shard-id [SHARD_ID]
                        Discord bot shard id (default: 0)
  --shard-count [SHARD_COUNT]
                        Discord bot shard counts (default: 1)
  --suppress            Suppress all input prompts and use defaults.
  ENV                   [chatbots only] Pass query string at the end of all options. It will be use instead of .env file. Sample: "BOT=discord&DISCORD_TOKEN=***&LOG_LEVEL=DEBUG"

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

### B2. Example Usage

Open your console and type `lncrawl --version` first to check if you have installed it properly.
Here are some example usage of the app:

- To start an interactive session: `lncrawl`

- To download using an url: `lncrawl -s https://boxnovel.com/novel/reincarnation-of-the-strongest-sword-god/`
- To search novels: `lncrawl -q "Strongest Sword God"`
- To search novels from selected sources: `lncrawl -q "Strongest Sword God" --sources`

- To download all chapters: `lncrawl --all`
- To download first 25 chapters: `lncrawl --first 25`
- To download all between two chapters: `lncrawl --range 10 30`
- To download all between two chapter links: `lncrawl https://boxnovel.com/novel/reincarnation-of-the-strongest-sword-god/chapter-2205 https://boxnovel.com/novel/reincarnation-of-the-strongest-sword-god/chapter-2211`
- To download a specific volumes: `lncrawl --volumes 2 3`

- To define output path: `lncrawl -o "D:\Lightnovels\reincarnation-of-the-strongest-sword-god"`
- To delete the output folder if exists: `lncrawl -f`
- To ignore the output folder if exists: `lncrawl -i`
- To resume download where is has been left previously: `lncrawl -i`
- To specify output formats: `lncrawl --format epub pdf mobi`

- To display list of supported sources: `lncrawl ---list-sources`

- If you provide an option in the argument, it will skip it in the interactive session.
  If you want to disable all interactive prompts, pass `--suppress` at the end.

- You can stack up options like this: `lncrawl -s https://boxnovel.com/novel/reincarnation-of-the-strongest-sword-god/ -o "D:\Lightnovels\reincarnation-of-the-strongest-sword-god" --last 50 -i --format pdf --suppress`

### B3. Running the bot

There are two chatbots available at this moment: Telegram and Discord. To run your own bot server, follow these instructions:

- Clone this repository
```bash
$ git clone https://github.com/dipu-bd/lightnovel-crawler
```

- Install calibre for pdf, mobi etc. formats.
  - https://calibre-ebook.com/download

- Install requirements
```bash
$ pip3 install --user -r requirements.txt
$ pip3 install --user -r requirements-dev.txt
```

- Copy `.env.example` file to `.env` file. Edit this file and give your API credentials here.

- To run the discord bot:
```bash
$ python3 . --bot discord --shard-id 0 --shard-count 1
```

- To run the telegram bot
```bash
$ python3 . --bot telegram
```

_There is a `start.sh` script to run a bot in ubuntu servers. It will basically execute the `python __main__.py` and send the task to run in background. I use it to run my discord bot in the server._

## (C) Development

You are very welcome to contribute in this project. You can:

- create new issues pointing out the bugs.
- solve existing issues.
- add your own sources.
- add new output formats.
- create new bots.

### C1. Adding new source

- Create new crawler using the [`sources/_template_.py`](https://github.com/dipu-bd/lightnovel-crawler/blob/master/lncrawl/sources/_template_.py) as template.
- Update [Supported sources](#c3-supported-sources) section in `README.md`
- Add some test inputs to `test_user_inputs` variable in `lncrawl/bots/test/test_inputs.py`

### C2. Adding new Bot

- Create a new bot file using [`bots/_sample.py`](https://github.com/dipu-bd/lightnovel-crawler/blob/master/lncrawl/bots/_sample.py) as template.
- Import bot to [`bots/__init__.py`](https://github.com/dipu-bd/lightnovel-crawler/blob/master/lncrawl/bots/__init__.py) file.

### C3. Supported sources

> Request new one by [creating a new issue](https://github.com/dipu-bd/lightnovel-crawler/issues/new/choose).

| Available Sources                            | Can Search | Can Login |      Maintainer       |
| -------------------------------------------- | :--------: | :-------: | :-------------------: |
| http://boxnovel.org                          |     ✔      |           |       @dipu-bd        |
| http://liberspark.com                        |            |           |                       |
| http://novelfull.com                         |     ✔      |           |       @dipu-bd        |
| http://tiknovel.com                          |            |           |                       |
| http://wspadancewichita.com                  |     ✔      |           |                       |
| http://www.fujitranslation.com               |            |           |                       |
| http://www.hanyunovels.site                  |     ✔      |           |      @SirGryphin      |
| http://www.machinenoveltranslation.com       |            |           |                       |
| http://www.tiknovel.com                      |            |           |                       |
| http://zenithnovels.com                      |            |           |                       |
| http://zhi-end.blogspot.co.id                |            |           |      @SirGryphin      |
| http://zhi-end.blogspot.com                  |            |           |      @SirGryphin      |
| https://1stkissnovel.love                    |     ✔      |           |      @SirGryphin      |
| https://88tangeatdrinkread.wordpress.com     |            |           |      @SirGryphin      |
| https://9kqw.com                             |     ✔      |           |                       |
| https://allnovel.org                         |     ✔      |           |      @SirGryphin      |
| https://anonanemone.wordpress.com            |            |           |      @SirGryphin      |
| https://arangscans.com                       |            |           |      @SirGryphin      |
| https://asadatranslations.com                |     ✔      |           |      @SirGryphin      |
| https://automtl.wordpress.com                |            |           |      @SirGryphin      |
| https://babelnovel.com                       |     ✔      |           |                       |
| https://bestlightnovel.com                   |     ✔      |           |                       |
| https://bestoflightnovels.com                |     ✔      |           |      @SirGryphin      |
| https://book.qidian.com                      |            |           |                       |
| https://boxnovel.com                         |     ✔      |           |       @dipu-bd        |
| https://clicknovel.net                       |            |           |      @SirGryphin      |
| https://creativenovels.com                   |            |           |                       |
| https://crescentmoon.blog                    |            |           |                       |
| https://daonovel.com                         |     ✔      |           |      @SirGryphin      |
| https://darktranslation.com                  |            |           |      @SirGryphin      |
| https://demontranslations.com                |            |           |      @SirGryphin      |
| https://dmtranslationscn.com                 |            |           |      @SirGryphin      |
| https://dsrealmtranslations.com              |            |           |      @SirGryphin      |
| https://es.mtlnovel.com                      |     ✔      |           |                       |
| https://exiledrebelsscanlations.com          |     ✔      |           |      @SirGryphin      |
| https://fanstranslations.com                 |            |           |      @SirGryphin      |
| https://fastnovel.net                        |            |           |      @SirGryphin      |
| https://foxaholic.com                        |     ✔      |           |                       |
| https://fr.mtlnovel.com                      |     ✔      |           |                       |
| https://fujitranslation.com                  |            |           |      @SirGryphin      |
| https://hui3r.wordpress.com                  |            |           |      @SirGryphin      |
| https://id.mtlnovel.com                      |     ✔      |           |                       |
| https://inadequatetranslations.wordpress.com |            |           |      @SirGryphin      |
| https://indowebnovel.id                      |            |           |                       |
| https://infinitenoveltranslations.net        |            |           |      @SirGryphin      |
| https://instadoses.com                       |            |           |                       |
| https://jpmtl.com                            |            |           |       @dipu-bd        |
| https://jstranslations1.com                  |            |           |      @SirGryphin      |
| https://justatranslatortranslations.com      |            |           |      @SirGryphin      |
| https://kiss-novel.com                       |            |           |                       |
| https://kisslightnovels.info                 |     ✔      |           |                       |
| https://lemontreetranslations.wordpress.com  |            |           |      @SirGryphin      |
| https://light-novel.online                   |     ✔      |           |                       |
| https://lightnovel.world                     |            |           |      @SirGryphin      |
| https://lightnovelheaven.com                 |            |           |      @SirGryphin      |
| https://lightnovelsonl.com                   |     ✔      |           |      @SirGryphin      |
| https://lightnovelstranslations.com          |            |           |      @SirGryphin      |
| https://listnovel.com                        |     ✔      |           |                       |
| https://litnet.com                           |     ✔      |           |                       |
| https://lnmtl.com                            |            |     ✔     |       @dipu-bd        |
| https://m.chinesefantasynovels.com           |            |           |                       |
| https://m.mywuxiaworld.com                   |     ✔      |           |                       |
| https://m.novelspread.com                    |            |           |                       |
| https://m.readlightnovel.cc                  |            |           |                       |
| https://m.romanticlovebooks.com              |            |           |                       |
| https://m.wuxiaworld.co                      |     ✔      |           |       @dipu-bd        |
| https://mangatoon.mobi                       |            |           |                       |
| https://meionovel.id                         |     ✔      |           |                       |
| https://moonstonetranslation.com             |            |           |      @SirGryphin      |
| https://morenovel.net                        |     ✔      |           |      @SirGryphin      |
| https://myoniyonitranslations.com            |            |           |                       |
| https://mysticalmerries.com                  |     ✔      |           |      @SirGryphin      |
| https://novel27.com                          |     ✔      |           |      @SirGryphin      |
| https://novelcrush.com                       |     ✔      |           |      @SirGryphin      |
| https://novelfull.com                        |     ✔      |           |       @dipu-bd        |
| https://novelgo.id/                          |            |           |                       |
| https://novelonlinefree.com                  |     ✔      |           |      @SirGryphin      |
| https://novelonlinefull.com                  |     ✔      |           |                       |
| https://novelraw.blogspot.com                |            |           |                       |
| https://novels.pl                            |            |           |       @dipu-bd        |
| https://novelsite.net                        |     ✔      |           |      @SirGryphin      |
| https://novelsrock.com                       |            |           |                       |
| https://noveltranslate.com                   |     ✔      |           |      @SirGryphin      |
| https://noveltrench.com                      |     ✔      |           |      @SirGryphin      |
| https://omgnovels.com                        |     ✔      |           |      @SirGryphin      |
| https://ranobelib.me                         |            |           |                       |
| https://readlightnovels.net                  |     ✔      |           |     @PreownedFIN      |
| https://readwebnovels.net                    |     ✔      |           |      @SirGryphin      |
| https://reincarnationpalace.com              |            |           |      @SirGryphin      |
| https://rewayat.club                         |            |           |                       |
| https://shalvationtranslations.wordpress.com |            |           |      @SirGryphin      |
| https://skynovel.org/                        |            |           |      @SirGryphin      |
| https://sleepytranslations.com               |            |           |      @SirGryphin      |
| https://steambunlightnovel.com               |            |           |      @SirGryphin      |
| https://supernovel.net                       |     ✔      |           |      @SirGryphin      |
| https://tomotranslations.com                 |            |           |                       |
| https://viewnovel.net                        |     ✔      |           |      @SirGryphin      |
| https://vipnovel.com                         |     ✔      |           |      @SirGryphin      |
| https://vistranslations.wordpress.com        |            |           |      @SirGryphin      |
| https://volarenovels.com                     |            |           |                       |
| https://wbnovel.com                          |     ✔      |           |                       |
| https://webnovel.online                      |            |           |                       |
| https://webnovelindonesia.com                |            |           |                       |
| https://webnovelonline.com                   |            |           |                       |
| https://woopread.com                         |     ✔      |           |                       |
| https://wordexcerpt.com                      |     ✔      |           | @dipu-bd, @SirGryphin |
| https://wordexcerpt.org                      |            |           | @dipu-bd, @SirGryphin |
| https://wuxiaworld.io                        |     ✔      |           |      @SirGryphin      |
| https://wuxiaworld.live                      |     ✔      |           |      @SirGryphin      |
| https://wuxiaworld.online                    |     ✔      |           |       @dipu-bd        |
| https://wuxiaworld.site                      |            |           |       @dipu-bd        |
| https://www.aixdzs.com                       |            |           |                       |
| https://www.asianhobbyist.com                |            |           |                       |
| https://www.box-novel.com                    |     ✔      |           |      @SirGryphin      |
| https://www.daocaorenshuwu.com               |            |           |      @SirGryphin      |
| https://www.f-w-o.com                        |     ✔      |           |      @SirGryphin      |
| https://www.foxteller.com/                   |     ✔      |           |       @dipu-bd        |
| https://www.fuyuneko.org                     |            |           |      @SirGryphin      |
| https://www.idqidian.us                      |            |           |                       |
| https://www.koreanmtl.online                 |            |           |       @dipu-bd        |
| https://www.lightnovelpub.com                |     ✔      |           |                       |
| https://www.machine-translation.org          |     ✔      |           |                       |
| https://www.miraslation.net                  |            |           |      @SirGryphin      |
| https://www.mtlnovel.com                     |     ✔      |           |                       |
| https://www.mywuxiaworld.com                 |     ✔      |           |                       |
| https://www.novelall.com                     |     ✔      |           |                       |
| https://www.novelcool.com                    |            |           |      @SirGryphin      |
| https://www.novelhall.com                    |            |           |                       |
| https://www.novelhunters.com                 |     ✔      |           |      @SirGryphin      |
| https://www.novelpassion.com                 |     ✔      |           |      @SirGryphin      |
| https://www.novelringan.com                  |            |           |                       |
| https://www.novels.pl                        |            |           |       @dipu-bd        |
| https://www.novelspread.com                  |            |           |                       |
| https://www.novelupdates.cc                  |            |           |      @SirGryphin      |
| https://www.oppatranslations.com             |            |           |      @SirGryphin      |
| https://www.qidian.com                       |            |           |                       |
| https://www.readlightnovel.cc                |            |           |                       |
| https://www.readlightnovel.org               |            |           |                       |
| https://www.readnovelfull.com                |     ✔      |           |                       |
| https://www.romanticlovebooks.com            |            |           |                       |
| https://www.royalroad.com                    |     ✔      |           |                       |
| https://www.scribblehub.com                  |     ✔      |           |                       |
| https://www.shinsori.com                     |            |           |                       |
| https://www.tapread.com                      |            |           |                       |
| https://www.translateindo.com                |            |           |                       |
| https://www.virlyce.com                      |            |           |      @SirGryphin      |
| https://www.wattpad.com                      |            |           |       @dipu-bd        |
| https://www.webnovel.com                     |     ✔      |           |       @dipu-bd        |
| https://www.webnovelover.com                 |     ✔      |           |      @SirGryphin      |
| https://www.worldnovel.online                |     ✔      |           |                       |
| https://www.wuxialeague.com                  |            |           |                       |
| https://www.wuxiaworld.co                    |     ✔      |           |       @dipu-bd        |
| https://www.wuxiaworld.com                   |     ✔      |           |       @dipu-bd        |
| https://www.x81zw.com                        |            |           |      @SirGryphin      |
| https://www.xiainovel.com                    |            |           |      @SirGryphin      |
| https://www.xsbiquge.com                     |            |           |      @SirGryphin      |
| https://yukinovel.id                         |            |           |                       |
| https://zinnovel.com                         |     ✔      |           |      @SirGryphin      |

### C4. Rejected sources

| Rejected Sources                | Reason                                                                                             |
| ------------------------------- | -------------------------------------------------------------------------------------------------- |
| http://fullnovel.live           | `403 - Forbidden: Access is denied`                                                                |
| http://gravitytales.com         | `Redirects to webnovel.com`                                                                        |
| http://moonbunnycafe.com        | `Does not follow uniform format`                                                                   |
| https://anythingnovel.com       | `Site broken`                                                                                      |
| https://chrysanthemumgarden.com | `Removed on request of the owner` [#649](https://github.com/dipu-bd/lightnovel-crawler/issues/649) |
| https://indomtl.com             | `Does not like to be crawled`                                                                      |
| https://lnindo.org              | `Does not like to be crawled`                                                                      |
| https://mtled-novels.com        | `Domain is expired`                                                                                |
| https://novelplanet.com         | `Site is closed`                                                                                   |
| https://www.flying-lines.com    | `Obfuscated content`                                                                               |
| https://www.jieruihao.cn        | `Unavailable`                                                                                      |
| https://www.noveluniverse.com   | `Site is down`                                                                                     |
| https://www.novelupdates.com    | `Does not host any novels`                                                                         |
| https://www.novelv.com          | `Site is down`                                                                                     |
| https://www.rebirth.online      | `Site moved`                                                                                       |
| https://4scanlation.xyz         | `Site moved`                                                                                       |
| https://pery.info               | `Site is down`                                                                                     |
| https://writerupdates.com       | `Site is down`                                                                                     |
| https://www.centinni.com        | `Site is down`                                                                                     |

### C5. Supported output formats

- JSON (default)
- EPUB (default)
- TEXT
- WEB
- DOCX
- MOBI
- PDF
- RTF
- TXT
- AZW3
- FB2
- LIT
- LRF
- OEB
- PDB
- PML
- RB
- SNB
- TCR
- HTML

### C6. Supported bots

- Console Bot
- Telegram Bot
- Discord Bot
