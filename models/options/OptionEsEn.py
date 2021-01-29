from models.options.OptionTranslate import OptionTranslate


class OptionEsEn(OptionTranslate):

    def __init__(self, word: str):
        super().__init__(word)

    def get_url(self) -> str:
        url = "https://translate.google.com/?sl=es&tl=en&op=translate&text=" + self.word
        return url
