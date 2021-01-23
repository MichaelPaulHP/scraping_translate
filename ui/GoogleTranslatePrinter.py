import curses

from models.GoogleTranslate import GoogleTranslate


class GoogleTranslatePrinter:
    def __init__(self, vm):
        self.vm = vm

    def print_definitions(self, window):
        definitions = self.vm.definitions()
        if definitions is not None:
            for definition in definitions:
                window.addstr("\n" + str(definition.type) + "\n", curses.color_pair(1))
                window.addstr(str(definition))

    def print_principal_result(self, windows):
        sh, sw = windows.getmaxyx()
        result = self.vm.principal_result()
        windows.addstr(4, int(sw / 2) + 5, result, curses.color_pair(1))

    def print_translations(self, window):
        h, w = window.getmaxyx()
        translations = self.vm.translations()
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
