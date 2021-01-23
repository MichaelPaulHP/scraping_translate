from models.GoogleScraper import GoogleScraper
from models.GoogleTranslate import GoogleTranslate


class TranslatorVM:

    @staticmethod
    def do_scraping(text: str) -> GoogleTranslate:
        scrap = GoogleScraper()
        google_translate = scrap.scraping(text)
        # trans =google_translate.get_translations()
        return google_translate
