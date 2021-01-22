from bs4 import Tag, ResultSet

from models.Translation import Translation
from models.TypeTranslation import TypeTranslation


class TranslationScraper:

    @staticmethod
    def scraping(element: Tag):
        t_bodys = element.table.find_all("tbody")
        types = []
        for body in t_bodys:
            title = body.tr.th.get_text()
            bodyTr: ResultSet = body.find_all("tr")
            result = []
            for index in range(len(bodyTr)):
                tr = bodyTr[index]
                worlds = tr.get_text('|').split('|')
                worlds = map(lambda t: t.strip(), worlds)
                worlds = list(filter(lambda t: len(t) > 1, list(worlds)))
                if index != 0:
                    word, translations = TranslationScraper.check_word(worlds, 0)
                    result.append(Translation(word, translations))
                else:
                    word, translations = TranslationScraper.check_word(worlds, 1)
                    result.append(Translation(word, translations))
            types.append(TypeTranslation(title, result))
        return types

    @staticmethod
    def check_word(words, firstIndex):
        first_word = words[firstIndex]
        word = ""
        translations = None
        if len(first_word) <= 3:
            word = " ".join(words[firstIndex:firstIndex + 2])
            translations = words[firstIndex + 3:]
        else:
            word = words[firstIndex]
            translations = words[firstIndex + 1:]
        return word, translations
