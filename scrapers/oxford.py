import requests
from bs4 import BeautifulSoup
from scrapers.scraper import Scraper


class OxfordScraper(Scraper):
    WEBSITE = "https://www.oxfordlearnersdictionaries.com/definition/english/"

    def scrape_data(self, word):
        print("\nScraping from oxford dictionary: {}".format(word))
        website = f'{self.WEBSITE}{word}'
        request = requests.get(website).text
        soup = BeautifulSoup(request, 'lxml')
        word_from_site = soup.find('div', class_='top-container').find('h1', class_='headword').text
        try:
            phon_en = soup.find('div', class_='phons_br').find('span', class_='phon').text
        except AttributeError:
            phon_en = soup.find('div', class_='phons_n_am').find('span', class_='phon').text
        try:
            phon_am = soup.find('div', class_='phons_n_am').find('span', class_='phon').text
        except AttributeError:
            phon_am = soup.find('div', class_='phons_br').find('span', class_='phon').text
        if word == word_from_site:
            return self.SCRAPED_DATA(word, phon_en, phon_am, website)
        else:
            formated_data = self.format_data(self.SCRAPED_DATA(word, phon_en, phon_am, website), word_from_site)
            return formated_data
