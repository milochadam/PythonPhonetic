import sqlite3

from settings import DATABASE_PATH, DATABASE_NAME


class Database:
    def __init__(self, name: str = DATABASE_NAME, path: str = DATABASE_PATH):
        self.name: str = name
        self.path: str = path

    def create_database(self):
        with sqlite3.connect(self.path) as connection:
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
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT * FROM phonetic WHERE word = "{}"'''.format(word))
            if cursor.fetchone():
                return True
            return False

    def update_database(self, data) -> None:
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO phonetic VALUES (NULL, "{}", "{}", "{}", "{}")'''.format(
                data.word, data.phon_en, data.phon_am, data.website)
            )

    def drop_table(self):
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            cursor.execute('''DROP TABLE {}'''.format(self.name))

    def select_all(self) -> list:
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            return cursor.execute('''SELECT * FROM {}'''.format(self.name)).fetchall()

    def take_from_database(self, language, word) -> str:
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT phon_{} FROM {} WHERE word = "{}"
            '''.format(language, self.name, word))
            return cursor.fetchone()[0]

    def delete(self, word):
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            cursor.execute('''DELETE FROM {};'''.format(self.name, word))

    def describe(self):
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            return cursor.execute('''PRAGMA table_info({})'''.format(self.name))

    def insert_own(self, word, phon_en=None, phon_am=None) -> None:
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO {} VALUES (NULL, "{}", "{}", "{}", "NULL")'''.format(
                self.name,
                word,
                "NULL" if phon_en is None else phon_en,
                "NULL" if phon_am is None else phon_am)
            )
