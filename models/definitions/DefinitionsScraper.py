from bs4 import Tag

from models.definitions.Definition import Definition


class DefinitionScraper:
    @staticmethod
    def scraping(element: Tag) -> [Definition]:
        types = element.find_all("div", class_="KWoJId")
        examples = element.find_all("div", class_="eqNifb")
        definitions = []
        for numType in range(len(types)):
            type = types[numType].get_text()
            example = examples[numType].get_text("|").split('|')
            title = example[1]
            sub_title = ""
            synonyms = ""
            if len(example) >= 3:
                sub_title = example[2]
                synonyms = example[3:]
            definition = Definition(type, title, sub_title, synonyms)
            definitions.append(definition)
        return definitions
