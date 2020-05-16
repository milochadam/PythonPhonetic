import requests
from bs4 import BeautifulSoup
from scrapers.scraper import Scraper


class CambrScraper(Scraper):
    WEBSITE = "https://dictionary.cambridge.org/pl/dictionary/english/"

    def scrape_data(self, word):
        print("\nScraping from cambridge dictionary: {}".format(word))
        website = f'{self.WEBSITE}{word}'
        request = requests.get(website).text
        soup = BeautifulSoup(request, 'lxml')
        word_from_site = soup.find('div', class_='pos-header dpos-h').find('span', class_='hw dhw').text
        try:
            phon_en = soup.find('span', class_='uk dpron-i').find('span', class_='ipa dipa lpr-2 lpl-1').text
        except AttributeError:
            phon_en = soup.find('span', class_='us dpron-i').find('span', class_='ipa dipa lpr-2 lpl-1').text
        try:
            phon_am = soup.find('span', class_='us dpron-i').find('span', class_='ipa dipa lpr-2 lpl-1').text
        except AttributeError:
            phon_am = soup.find('span', class_='uk dpron-i').find('span', class_='ipa dipa lpr-2 lpl-1').text
        if word == word_from_site:
            return self.SCRAPED_DATA(word, phon_en, phon_am, website)
        else:
            formated_data = self.format_data(self.SCRAPED_DATA(word, phon_en, phon_am, website), word_from_site)
            return formated_data
