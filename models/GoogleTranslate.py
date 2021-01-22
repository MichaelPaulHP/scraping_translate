from models.TypeTranslation import TypeTranslation
from models.definitions.Definition import Definition


class GoogleTranslate:

    def __init__(self):
        self.translations: [TypeTranslation] = None
        self.principal: str = None
        self.definitions: [Definition] = None

    def get_translations(self) -> [TypeTranslation]:
        return self.translations
