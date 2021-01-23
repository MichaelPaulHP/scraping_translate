from models.GoogleScraper import GoogleScraper
from models.GoogleTranslate import GoogleTranslate
from models.Listener import Listener


class TranslatorVM:

    def __init__(self, listener: Listener):
        self.listener = listener
        self.google_translate = None

    def do_scraping(self, text: str):
        scrap = GoogleScraper()
        scrap.listener = self.listener
        self.google_translate = scrap.scraping(text)
        # trans =google_translate.get_translations()

    def translations(self):
        return self.google_translate.get_translations()

    def principal_result(self):
        return self.google_translate.principal

    def definitions(self):
        return self.google_translate.definitions
