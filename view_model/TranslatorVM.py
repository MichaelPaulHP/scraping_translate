from models.GoogleScraper import GoogleScraper
from models.GoogleTranslate import GoogleTranslate
from models.Listener import Listener
from models.options.OptionEnEs import OptionEnEs
from models.options.OptionEsEn import OptionEsEn


class TranslatorVM:

    def __init__(self, listener: Listener):
        self.listener = listener
        self.google_translate = None
        self.scrap = None

    def init_scraping(self):
        self.scrap = GoogleScraper()
        self.scrap.listener = self.listener

    def do_scraping_eng_es(self, text: str):
        self.google_translate = self.scrap.scraping(OptionEnEs(text))
        # trans =google_translate.get_translations()

    def do_scraping_es_eng(self, text: str):
        self.google_translate = self.scrap.scraping(OptionEsEn(text))

    def translations(self):
        return self.google_translate.get_translations()

    def principal_result(self):
        return self.google_translate.principal

    def definitions(self):
        return self.google_translate.definitions
