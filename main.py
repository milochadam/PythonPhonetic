#!/usr/bin/env python

import sqlite3
from bs4 import BeautifulSoup
import requests
from collections import namedtuple
from termcolor import colored
import argparse


class Database:
    NAME = "phonetic"

    def create_database(self):
        with sqlite3.connect(self.NAME) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE phonetic (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                phon_en TEXT NOT NULL,
                phon_am TEXT NOT NULL,
                website TEXT NOT NULL 
            );''')

    def is_in_database(self, word) -> bool:
        with sqlite3.connect(self.NAME) as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT * FROM phonetic WHERE word = "{}"'''.format(word))
            if cursor.fetchone():
                return True
            return False

    def update_database(self, data) -> None:
        with sqlite3.connect(self.NAME) as connection:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO phonetic VALUES (NULL, "{}", "{}", "{}", "{}")'''.format(
                data.word, data.phon_en, data.phon_am, data.website)
            )

    def drop_table(self):
        with sqlite3.connect(self.NAME) as connection:
            cursor = connection.cursor()
            cursor.execute('''DROP TABLE {}'''.format(self.NAME))

    def select_all(self) -> list:
        with sqlite3.connect(self.NAME) as connection:
            cursor = connection.cursor()
            return cursor.execute('''SELECT * FROM phonetic''').fetchall()

    def take_from_database(self, language, word) -> str:
        with sqlite3.connect(self.NAME) as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT phon_{} FROM {} WHERE word = "{}"
            '''.format(language, self.NAME, word))
            return cursor.fetchone()[0]

    def delete(self, word):
        with sqlite3.connect(self.NAME) as connection:
            cursor = connection.cursor()
            cursor.execute('''DELETE FROM {};'''.format(self.NAME, word))

    def describe(self):
        with sqlite3.connect(self.NAME) as connection:
            cursor = connection.cursor()
            return cursor.execute('''PRAGMA table_info({})'''.format(self.NAME))

    @staticmethod
    def insert_own(word) -> None:
        website = "user_input"
        phon_en = input("Wprowdź angelski zapis fonetyczny słowa.\n")
        phon_am = input("Wprowdź amerykański zapis fonetyczny słowa.\n")
        with sqlite3.connect('phonetic') as connection:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO phonetic VALUES (NULL, "{}", "{}", "{}", "{}")'''.format(
                word, phon_en, phon_am, website))


class Scraper:
    SCRAPED_DATA = namedtuple("scraped_data", ["word", "phon_en", "phon_am", "website"])
    WEBSITE = NotImplemented

    def scrape_data(self, word):
        return NotImplemented


class CambrScraper(Scraper):
    WEBSITE = "https://dictionary.cambridge.org/pl/dictionary/english/"

    def scrape_data(self, word):
        print("\nScraping from cambridge dictionary: {}".format(word))
        website = f'{self.WEBSITE}{word}'
        request = requests.get(website).text
        soup = BeautifulSoup(request, 'lxml')
        word_from_site = soup.find('div', class_='pos-header dpos-h').find('span', class_='hw dhw').text
        phon_en = soup.find('span', class_='uk dpron-i').find('span', class_='ipa dipa lpr-2 lpl-1').text
        phon_am = soup.find('span', class_='us dpron-i').find('span', class_='ipa dipa lpr-2 lpl-1').text
        if word.lower() == word_from_site or word == word_from_site:
            return self.SCRAPED_DATA(word, phon_en, phon_am, website)
        else:
            if word.endswith("ed"):
                if word[-1] in ("t", "d"):
                    return self.SCRAPED_DATA(word_from_site + "ed", phon_en + "id", phon_am + "id", website)
                if word[-1] in ("p", "k", "f", "c", "x") or word[-2:] in ("GH", "CH", "SH", "SS"):
                    return self.SCRAPED_DATA(word_from_site + "ed", phon_en + "t", phon_am + "t", website)
                if word[-1] in ("l", "n", "r", "g", "v", "s", "z", "b", "m"):
                    return self.SCRAPED_DATA(word_from_site + "ed", phon_en + "d", phon_am + "d", website)
            elif word.endswith("s"):
                return self.SCRAPED_DATA(word_from_site + "s", phon_en + "s", phon_am + "s", website)
            elif word.endswith("ing"):
                return self.SCRAPED_DATA(word_from_site + "in", phon_en + "in", phon_am + "in", website)


class OxfordScraper(Scraper):
    WEBSITE = "https://www.oxfordlearnersdictionaries.com/definition/english/"

    def scrape_data(self, word):
        print("\nScraping from oxford dictionary: {}".format(word))
        website = f'{self.WEBSITE}{word}'
        request = requests.get(website).text
        soup = BeautifulSoup(request, 'lxml')
        word_from_site = soup.find('div', class_='top-container').find('h1', class_='headword').text
        phon_en = soup.find('div', class_='phons_br').find('span', class_='phon').text
        phon_am = soup.find('div', class_='phons_n_am').find('span', class_='phon').text
        print(word == word_from_site)
        if word == word_from_site:
            return self.SCRAPED_DATA(word, phon_en, phon_am, website)
        else:
            if word.endswith("ed"):
                if word[-1] in ("t", "d"):
                    return self.SCRAPED_DATA(word_from_site + "ed", phon_en + "id", phon_am + "id", website)
                if word[-1] in ("p", "k", "f", "c", "x") or word[-2:] in ("GH", "CH", "SH", "SS"):
                    return self.SCRAPED_DATA(word_from_site + "ed", phon_en + "t", phon_am + "t", website)
                if word[-1] in ("l", "n", "r", "g", "v", "s", "z", "b", "m"):
                    return self.SCRAPED_DATA(word_from_site + "ed", phon_en + "d", phon_am + "d", website)
            elif word.endswith("s"):
                return self.SCRAPED_DATA(word_from_site + "s", phon_en + "s", phon_am + "s", website)
            elif word.endswith("ing"):
                return self.SCRAPED_DATA(word_from_site + "in", phon_en + "in", phon_am + "in", website)


class PhoneticScraprer:
    SCRAPERS = {
        "cmbr": CambrScraper,
        "oxf": OxfordScraper,
    }

    def __init__(self, sentence: str, language: str = "en", scraper: str = "cmbr"):
        self.language: str = language
        self.sentence: list = [word.strip(",") for word in sentence.split()]
        self.scraper = self.SCRAPERS[scraper]()
        self.databse: Database = Database()

    def execute(self):
        sentence = ""
        for word in self.sentence:
            try:
                if not self.databse.is_in_database(word):
                    data = self.scraper.scrape_data(word)
                    self.databse.update_database(data)
                    sentence += colored(self.databse.take_from_database(self.language, word), "yellow") + " "
                else:
                    sentence += colored(self.databse.take_from_database(self.language, word), "green") + " "
            except AttributeError:
                sentence += colored(word, "red") + " "
        return sentence


parser = argparse.ArgumentParser(description="Phonetic sentence scraping")
parser.add_argument("-s", "--sentence", metavar="", nargs='+', type=str, required=True, help="Give sentence to translate into phonetic")
parser.add_argument("-l", "--language", metavar="", default="en", type=str, help="Give language to translate sentence into phonetic\n"
                                                                                 "en - british english DEFAULT\n"
                                                                                 "am - american english")
parser.add_argument("-S", "--scraper", metavar="", default="cmbr", type=str, help="Choose the website to take data from\n"
                                                                                  "cmbr - Cambridge website\n"
                                                                                  "oxf - Oxford website")
args = parser.parse_args()

if __name__ == "__main__":
    p = PhoneticScraprer(sentence=' '.join(args.sentence), language=args.language, scraper=args.scraper)
    print(p.execute())
