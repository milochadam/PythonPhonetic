#!/usr/bin/env python

import sqlite3
import argparse
from database import Database
from scrapers import CambrScraper, OxfordScraper
from settings import DATABASE_NAME, DATABASE_PATH
from termcolor import colored


class PhoneticScraprer:
    SCRAPERS = {
        "cmbr": CambrScraper,
        "oxf": OxfordScraper,
    }

    def __init__(self, sentence: str, language: str = "en", scraper: str = "cmbr"):
        self.language: str = language
        self.sentence: list = [word.strip(",") for word in sentence.split()]
        self.scraper = self.SCRAPERS[scraper]()
        self.database: Database = Database(name=DATABASE_NAME, path=DATABASE_PATH)

    def execute(self):
        try:
            self.database.create_database()
        except sqlite3.OperationalError:
            pass
        sentence = ""
        for word in self.sentence:
            try:
                if not self.database.is_in_database(word.lower()):
                    data = self.scraper.scrape_data(word.lower())
                    self.database.update_database(data)
                    sentence += colored(self.database.take_from_database(self.language, word.lower()), "yellow") + " "
                else:
                    sentence += colored(self.database.take_from_database(self.language, word.lower()), "green") + " "
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
