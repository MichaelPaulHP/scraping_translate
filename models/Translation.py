class Translation:

    def __init__(self, word, translations):
        self.word: str = word
        self.translations: [str] = translations

    def __str__(self):
        return self.word + ": " + ", ".join(self.translations)
