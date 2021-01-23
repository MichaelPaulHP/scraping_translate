import curses

from models.GoogleTranslate import GoogleTranslate


class GoogleTranslatePrinter:
    def print_definitions(self, window, google: GoogleTranslate):
        definitions = google.definitions
        if definitions is not None:
            for definition in definitions:
                window.addstr("\n" + str(definition.type) + "\n", curses.color_pair(1))
                window.addstr(str(definition))

    def print_principal_result(self, windows, google_translate):
        sh, sw = windows.getmaxyx()
        oy, ox = windows.getbegyx()
        result = google_translate.principal
        windows.addstr(4, int(sw / 2) + 5, result, curses.color_pair(1))

    def print_translations(self, window, google: GoogleTranslate):
        h, w = window.getmaxyx()
        translations = google.get_translations()
        if translations is not None:
            for type in translations:
                window.addstr("\n" + str(type.title), curses.color_pair(1))
                self.print_translations_detail(window, type.translations)

    def print_translations_detail(self, windows, translations):
        for translation in translations:
            word = translation.word
            windows.addstr("\n" + word, curses.A_UNDERLINE)
            windows.addstr(": ")
            windows.addstr(", ".join(translation.translations))
