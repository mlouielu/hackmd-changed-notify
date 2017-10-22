#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import concurrent.futures
import json
import os
import re
import subprocess
from datetime import datetime

import alog
import requests
from lxml import etree

# Default database
DATABASE_PATH = 'db.json'

"""
{
   "username": "twngbm",
   "user_github": "https://github.com/twngbm",
   "works": {
        "ternay": {
            "hackmd": "https:/hackmd.com/bla",
            "github": "https://github.com/lala",
            "last_modify": "1000",
            "last_words": "2048"
        }
   }
}
"""

class HackMDNotify:
    def __init__(self, db_path):
        self.path = db_path
        self.db = {}
        self.threshold_minutes = 20
        self.threshold_words = 300

    def init_db(self):
        self.db = {}
        self.save_db()

    def load_db(self):
        if not os.path.exists(self.path):
            self.init_db()

        self.db = json.loads(open(self.path).read())
        return self.db

    def save_db(self):
        with open(self.path, 'w') as f:
            f.write(json.dumps(self.db, ensure_ascii=False))

    def check_if_need_notify(self, work, current):
        # Input
        #  work: {'hackmd': '', 'github': '', 'last_modify': -1, 'last_words': -1}
        #  current: (modify: str, words: int)
        if work['last_modify'] == -1 or work['last_words'] == -1:
            return False

        lmodify = datetime.strptime(work['last_modify'][:-6],
                                    "%a %b %d %Y %H:%M:%S %Z%z")
        cmodify = datetime.strptime(current[0][:-6],
                                    "%a %b %d %Y %H:%M:%S %Z%z")
        minutes_diff = (cmodify - lmodify).seconds // 60
        words_diff = (current[1] - work['last_words'])

        # NOTE: Change the value to change the threshold
        # XXX: Configurable?
        if (minutes_diff > self.threshold_minutes and
            words_diff >= self.threshold_words):
            return True
        return False

    def update_work(self, work, modify, words):
        work['last_modify'] = modify
        work['last_words'] = words

    def check_user_works_update(self, user):
        works = self.db[user]['works']
        for wk in works:
            current = self.parse_work(works[wk]['hackmd'], user, wk)
            if (self.check_if_need_notify(works[wk], current)):
                alog.critical('Bang, please check: %s - %s: %s' % (user, wk, works[wk]['hackmd']))
                self.update_work(works[wk], current[0], current[1])

    def check_works_update(self):
        # This will check all user works in database
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            jobs = [executor.submit(self.check_user_works_update, user) for user in self.db]
            for future in concurrent.futures.as_completed(jobs):
                future.result()

    def init_user_work(self, username, wk):
        url = self.db[username]['works'][wk]['hackmd']
        modify, words = self.parse_work(url, username, wk)

        self.db[username]['works'][wk]['last_modify'] = modify
        self.db[username]['works'][wk]['last_words'] = words

    def insert_user(self, username, user_github, works):
        if username not in self.db:
            self.db[username] = {
                'username': username,
                'user_github': user_github,
                'works': {}
            }

        parentheses = re.compile('\(([^\)]+)\)')
        for work in works:
            try:
                wk = parentheses.findall(work[0])[0]
            except IndexError:
                alog.warn('works: "%s" gave a bad format of "%s"' % (username, work[0]))
                continue

            if wk not in self.db[username]['works']:
                self.db[username]['works'][wk] = {
                    'hackmd': work[1],
                    'github': work[2],
                    'last_modify': "",
                    'last_words': 0
                }

                self.init_user_work(username, wk)

    def parse_work(self, url, username, wk):
        # Return (modify, words)
        r = requests.get(url)
        root = etree.HTML(r.text)

        modify = root.xpath('//span[contains(@class, "ui-lastchange")]')[1].get('data-updatetime', -1)
        try:
            words = len(root.xpath('//div[@id="doc"]')[0].text)
        except TypeError:
            alog.warn('parse-hackmd: "%-12s", work: "%s" Can not get words' % (username, wk))
            if url.startswith('https://hackmd.io/s/'):
                alog.warn('   - You can check at: %s' % url)
            else:
                alog.warn('   - HackMD URL is not in publish mode! Please change it.')
                alog.warn('   - %s - %s: %s' % (username, wk, url))
            words = -1

        return (modify, words)

    def parse_from_homework(self, url):
        r = requests.get(url)
        root = etree.HTML(r.text)
        md = root.xpath('//div[@id="doc"]')[0].text

        USER_NAME_PREFIX = '- [ ] ['
        MARKUP_REGEX = '\\[([^]]+)]\\(\\s*(http[s]?://[^)]+)\\s*\\)'
        for block in md.split('---'):
            if USER_NAME_PREFIX not in block:
                continue

            links = re.findall(MARKUP_REGEX, block)
            if not links:
                # WHY?
                continue
            user = links[0]
            works = []
            for i, link in enumerate(links):
                if link[0].startswith('開發紀錄'):
                    try:
                        github = links[i + 1][1] if 'github' in links[i + 1][1] else ''
                    except IndexError:
                        github = ''
                    finally:
                        works.append([link[0], link[1], github])

            # Insert user into database
            self.insert_user(user[0], user[1], works)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--check-update',
                        help='Check update of the works in database', action='store_true')
    parser.add_argument('-i', '--import-hackmd',
                        help='Import works from hackmd publish page')
    parser.add_argument('-d', '--init-db',
                        help='This will init your database', action='store_true')
    parser.add_argument('--words', help='Threshold words',
                        type=int, default=300)
    parser.add_argument('--minutes', help='Threshold minutes',
                        type=int, default=20)
    return parser

if __name__ == '__main__':
    md = HackMDNotify(DATABASE_PATH)
    md.load_db()

    parser = parse_args()
    args = parser.parse_args()

    md.threshold_words = args.words
    md.threshold_minutes = args.minutes
    if args.init_db:
        alog.info('Init database')
        md.init_db()
        md.save_db()
    elif args.import_hackmd:
        alog.info('Start parsing HackMD')
        md.parse_from_homework(args.import_hackmd)
        alog.info('Done, save the result to database')
        md.save_db()
    elif args.check_update:
        alog.info('Start to check all works in database')
        alog.set_level('CRITICAL')
        md.check_works_update()
        alog.set_level('INFO')
        alog.info('Done, save the update result to database')
        md.save_db()
    else:
        parser.print_help()
