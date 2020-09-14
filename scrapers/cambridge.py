import requests
from bs4 import BeautifulSoup

from scrapers.scraper import Scraper

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept': 'application/json',
    'Accept-Language': 'pl,en;q=0.5',
    'Referer': 'https://dictionary.cambridge.org/pl/dictionary/english/test',
    'AMP-Same-Origin': 'true',
    'DNT': '1',
    'Connection': 'keep-alive',
}
class CambrScraper(Scraper):
    WEBSITE = "https://dictionary.cambridge.org/pl/dictionary/english/"

    def scrape_data(self, word):
        print("Scraping from cambridge dictionary: {}".format(word))
        website = f'{self.WEBSITE}{word}'
        request = requests.get(website, headers=headers).text
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
