import urllib
from datetime import datetime
from os import path
from random import randrange
from sys import exit, maxsize
from time import sleep

import requests
from lxml import html

from cutils.cutils import CsvHelper

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'


class FsoCrawler():
    def __init__(self, csv_writer=None, *args, **kwargs):
        self.csv_writer = csv_writer if csv_writer else CsvHelper()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def crawl(self, url):

        # Store scraped jobs
        fso_info = []
        headers = {'user-agent': USER_AGENT}
        try:
            sleep(randrange(1, 3))
            print('Crawling {}'.format(url))
            page = requests.get(url, headers=headers)
        except Exception:
            return

        try:
            page = html.fromstring(page.content)
            body = page.xpath('//body')[0]
            state = ''.join(body.xpath(
                './/a[contains(@href, "/state/")]/span/text()'))
            city = ''.join(body.xpath(
                './/a[contains(@href, "/state/")]/following-sibling::a/span/text()'))
            name = ''.join(body.xpath('.//h3[@itemprop="name"]/text()'))
            address = ''.join(body.xpath(
                './/td[contains(@itemprop, "location")]/descendant-or-self::*/text()'))
            state_url = ''.join(body.xpath(
                './/td[contains(text(), "State of")]/a/@href'))
            phone = ''.join(body.xpath(
                './/div[contains(@class, "visible-phone")]/span[contains(@itemprop, "telephone")]/a/text()'))
            hours = ' | '.join([''.join(hour.xpath('.//descendant-or-self::*/text()')) for hour in body.xpath(
                './/span[contains(text(), "Hours of Operation")]/following-sibling::table/descendant::td')])

            fso_info.append(state)
            fso_info.append(city)
            fso_info.append(name)
            fso_info.append(address)
            fso_info.append(state_url)
            fso_info.append(phone)
            fso_info.append(hours)

        except Exception:
            pass
        finally:
            # fso_info = [''.join([i if ord(i) < 128 else ' ' for i in text]) for text in fso_info]
            if fso_info and self.csv_writer:
                self.csv_writer.save_to_csv(fso_info)


def main():
    print("""
        Ctrl + C -> Enter to quit
    """)

    urls = []
    with open('urls.txt', mode='r') as f:
        urls = f.read().splitlines()
        urls = [line.strip() for line in urls]

    # Set header fields
    headers = [
        'State',
        'City',
        'Name',
        'Address',
        'State URL',
        'Phone',
        'Hours'
    ]

    crawlr = FsoCrawler()
    output_file = 'data.csv'
    crawlr.csv_writer = CsvHelper(output_file, mode='a', encoding='utf-8')
    crawlr.csv_writer.set_headers(headers)

    for url in urls:
        try:
            crawlr.crawl(url)
        except Exception:
            pass


if __name__ == '__main__':
    main()
