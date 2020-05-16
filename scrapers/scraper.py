from collections import namedtuple


class Scraper:
    SCRAPED_DATA = namedtuple("scraped_data", ["word", "phon_en", "phon_am", "website"])
    WEBSITE = NotImplemented

    def scrape_data(self, word):
        return NotImplemented

    def format_data(self, data, word_from_site):
        if data.word.endswith("ed"):
            if data.word[-1] in ("t", "d"):
                return self.SCRAPED_DATA(word_from_site + "ed", data.phon_en + "id", data.phon_am + "id", data.website)
            if data.word[-1] in ("p", "k", "f", "c", "x") or data.word[-2:] in ("GH", "CH", "SH", "SS"):
                return self.SCRAPED_DATA(word_from_site + "ed", data.phon_en + "t", data.phon_am + "t", data.website)
            if data.word[-1] in ("l", "n", "r", "g", "v", "s", "z", "b", "m"):
                return self.SCRAPED_DATA(word_from_site + "ed", data.phon_en + "d", data.phon_am + "d", data.website)
        elif data.word.endswith("s"):
            return self.SCRAPED_DATA(word_from_site + "s", data.phon_en + "s", data.phon_am + "s", data.website)
        elif data.word.endswith("ing"):
            return self.SCRAPED_DATA(word_from_site + "in", data.phon_en + "in", data.phon_am + "in", data.website)
