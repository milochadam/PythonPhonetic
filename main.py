import sqlite3
from bs4 import BeautifulSoup
import requests
from termcolor import colored


class Database:
    def __init__(self) -> None:
        self.name = 'phonetic'

    def is_in_database(self, word) -> bool:
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT * FROM phonetic WHERE word = "{}"'''.format(word))
            if cursor.fetchone():
                return True
            return False

    def update_database(self, word, phon_en, phon_am, website) -> None:
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO phonetic VALUES (NULL, "{}", "{}", "{}", "{}")'''.format(
                word, phon_en, phon_am, website)
            )

    def take_from_database(self, language, word) -> str:
        with sqlite3.connect('phonetic') as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT phon_{} FROM phonetic WHERE word = "{}"
            '''.format(language, word))
            return cursor.fetchone()[0]

    def insert_own(self, word) -> None:
        website = "user_input"
        phon_en = input("Wprowdź angelski zapis fonetyczny słowa.\n")
        phon_am = input("Wprowdź amerykański zapis fonetyczny słowa.\n")
        with sqlite3.connect('phonetic') as connection:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO phonetic VALUES (NULL, "{}", "{}", "{}", "{}")'''.format(
                word, phon_en, phon_am, website))


class PhoneticDict:
    def __init__(self) -> None:
        self.language = "en"
        self.words = None

    def choose_phonetic_language(self) -> None:
        choice = input("Jeśli chcesz pozostawić język angelski jako domyślny, naciśnij enter. W innym przypadku podaj"
                       "dowolną wartość.\n")
        if not choice == "":
            self.language = "am"

    def ask_for_sentence(self) -> None:
        sentence = input('Wprowadź zdanie\n')
        words = sentence.split()
        self.words = [word.strip(",") for word in words]

    def ask_user(self, word, database, phonetic_words):
        while True:
            choice = input('Wprowadź "k" jeśli chcesz kontynouwać, w innym przypadku podaj "w".\n')
            if choice == "k":
                phonetic_words.append(colored(word, 'red'))
                return
            elif choice == "w":
                return database.insert_own(word)
            else:
                print("Podana wartość jest nieprawidłowa!\n")
                continue


class CambrScraper:
    def __init__(self) -> None:
        self.word = None
        self.phon_en = None
        self.phon_am = None
        self.website = 'https://dictionary.cambridge.org/dictionary/english/'

    def scrape_word(self, word) -> None:
        source = requests.get(f'{self.website}{word}]').text
        soup = BeautifulSoup(source, 'lxml')
        self.phon_en = soup.find('span', class_='uk dpron-i').find('span', class_='ipa dipa lpr-2 lpl-1').text
        self.phon_am = soup.find('span', class_='us dpron-i').find('span', class_='ipa dipa lpr-2 lpl-1').text
        self.word = word


def main():
    while True:
        program = PhoneticDict()
        database = Database()
        first_scraper = CambrScraper()
        program.choose_phonetic_language()
        program.ask_for_sentence()
        phonetic_words_list = []
        for word in program.words:
            if not database.is_in_database(word):
                try:
                    first_scraper.scrape_word(word)
                    database.update_database(word, first_scraper.phon_en, first_scraper.phon_am, first_scraper.website)
                except AttributeError:
                    print("Nie można znaleźć słowa: {}.".format(word))
            try:
                colored_word = colored(database.take_from_database(program.language, word), "green")
                phonetic_words_list.append(colored_word)
            except TypeError:
                program.ask_user(word, database, phonetic_words_list)
        print(" ".join(phonetic_words_list))
        choice = input("Jeśli chcesz kontynuować, naciśnij enter. W innym przypadku podaj dowolną wartość.\n")
        if choice:
            break


if __name__ == "__main__":
    main()
# [c]ontinue, [i]nput transcription manually