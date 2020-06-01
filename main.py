#!/usr/bin/env python

import sqlite3
import argparse
from database import Database
from scrapers import CambrScraper, OxfordScraper
from termcolor import colored


class PhoneticApp:
    SCRAPERS = {
        "cmbr": CambrScraper,
        "oxf": OxfordScraper,
    }

    def __init__(self, sentence: str = None, language: str = "en", scraper: str = "cmbr"):
        self.language: str = language
        self.sentence: list = [word.strip(",") for word in sentence.split()] if sentence is not None else None
        self.scraper = self.SCRAPERS[scraper]()
        self.database: Database = Database()

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
parser.add_argument("-s", "--sentence", metavar="", default=None, nargs='+', type=str, help="Give sentence to translate into phonetic")
parser.add_argument("-l", "--language", metavar="", default="en", type=str, help="Give language to translate sentence into phonetic\n"
                                                                                 "en - british english DEFAULT\n"
                                                                                 "am - american english")
parser.add_argument("-S", "--scraper", metavar="", default="cmbr", type=str, help="Choose the website to take data from\n"
                                                                                  "cmbr - Cambridge website\n"
                                                                                  "oxf - Oxford website")
parser.add_argument("-aa", "--add_british", metavar="", default=None, type=str, help="Write a string containing word and british"
                                                                                     "phonetic"
                                                                                     "Example: hello heˈləʊ")
parser.add_argument("-ab", "--add_american", metavar="", default=None, type=str, help="Write a string containing word and american"
                                                                                      "phonetic"
                                                                                      "Example: hello heˈloʊ")

args = parser.parse_args()

if __name__ == "__main__":
    if args.sentence is not None:
        p = PhoneticApp(sentence=' '.join(args.sentence), language=args.language, scraper=args.scraper)
        print(p.execute())
    else:
        p = PhoneticApp()
        if args.add_british is not None:
            word, phon_en = args.add_british.split(" ")
            p.database.insert_own(word, phon_en=phon_en)
        elif args.add_american is not None:
            word, phon_am = args.add_american.split(" ")
            p.database.insert_own(word, phon_am=phon_am)
