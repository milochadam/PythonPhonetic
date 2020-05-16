import sqlite3


class Database:
    def __init__(self, name: str, path: str):
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
            return cursor.execute('''SELECT * FROM phonetic''').fetchall()

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

    @staticmethod
    def insert_own(word) -> None:
        website = "user_input"
        phon_en = input("Wprowdź angelski zapis fonetyczny słowa.\n")
        phon_am = input("Wprowdź amerykański zapis fonetyczny słowa.\n")
        with sqlite3.connect('phonetic') as connection:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO phonetic VALUES (NULL, "{}", "{}", "{}", "{}")'''.format(
                word, phon_en, phon_am, website))
