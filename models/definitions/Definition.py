class Definition:
    def __init__(self, type, title, sub_title, synonyms):
        self.type = type
        self.title = title
        self.sub_title = sub_title
        self.synonyms = synonyms

    def __str__(self):
        return self.title + "\n  " + self.sub_title + "\n  " + ", ".join(self.synonyms)
