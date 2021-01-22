class TypeTranslation:
    def __init__(self, title, translations):
        self.title = title
        self.translations = translations

    def __str__(self):
        strs = list(map(str, self.translations))
        return "\n".join(strs)
