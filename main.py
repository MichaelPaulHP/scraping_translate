# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from curses.textpad import Textbox

from models.GoogleScraper import GoogleScraper
from models.GoogleTranslate import GoogleTranslate
from models.TranslationScraper import TranslationScraper
from models.definitions.DefinitionsScraper import DefinitionScraper

name = 'Michael'
# def print_hi(name):
# Use a breakpoint in the code line below to debug your script.
print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

from prompt_toolkit import prompt

import curses
from curses import textpad


class Size:
    def __init__(self, height, width):
        self.height = height
        self.width = width


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def my_raw_input(stdscr, pos: Position, prompt_string) -> str:
    curses.echo()

    stdscr.addstr(pos.y, pos.x, prompt_string)
    #stdscr.move(pos.y, len(prompt_string) + pos.x)
    input = stdscr.getstr(pos.y, len(prompt_string) + pos.x, 50)
    stdscr.refresh()

    return input.decode("utf-8")


def print_box(stdscr, pos: Position, size: Size):
    box = [[pos.y, pos.x], [pos.y + size.height, pos.x + size.width]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])


def print_input_box(stdscr, sh, sw):
    # print_box(stdscr, Position(3, 3), Size(2, int(sw / 2)))
    text = my_raw_input(stdscr, Position(4, 4), "search: ")
    return text


def print_translations(window, google: GoogleTranslate):
    h, w = window.getmaxyx()
    translations = google.get_translations()
    if translations is not None:
        for type in translations:
            window.addstr("\n" + str(type.title), curses.color_pair(1))
            print_translations_detail(window, type.translations)


def print_translations_detail(windows, translations):
    for translation in translations:
        word = translation.word
        windows.addstr("\n" + word, curses.A_UNDERLINE)
        windows.addstr(": ")
        windows.addstr(", ".join(translation.translations))


def divide_window(windows):
    sh, sw = windows.getmaxyx()
    oy, ox = windows.getbegyx()
    w_one = curses.newwin(sh, int(sw / 2) - 2, oy, ox)
    w_two = curses.newwin(sh, int(sw / 2) - 4, oy, int(sw / 2) + 2)
    return w_one, w_two


def print_definitions(window, google: GoogleTranslate):
    definitions = google.definitions
    if definitions is not None:
        for definition in definitions:
            window.addstr("\n" + str(definition.type) + "\n", curses.color_pair(1))
            window.addstr(str(definition))


def print_principal_result(windows, google_translate):
    sh, sw = windows.getmaxyx()
    oy, ox = windows.getbegyx()
    result = google_translate.principal
    windows.addstr(4, int(sw / 2) + 5, result, curses.color_pair(1))


def show_main(stdscr):
    curses.curs_set(1)
    stdscr.nodelay(1)
    start_color()
    print_options(stdscr)
    sh, sw = stdscr.getmaxyx()

    text = None
    text = print_input_box(stdscr, sh, sw)
    stdscr.addstr(0, 0, "text")
    while True:
        try:
            if text is not None:
                stdscr.addstr(4, 4, "Loading...")
                #google_translate = do_scraping(text)
                stdscr.addstr(4, 4, "Search:  ")
                win_result = curses.newwin(sh - 7, sw, 6, 0)
                win_result.getstr()

                #print_principal_result(stdscr, google_translate)
                stdscr.refresh()

                one, two = divide_window(win_result)
                #print_translations(two, google_translate)
                #print_definitions(one, google_translate)

                win_result.refresh()
                one.refresh()
                two.refresh()
                curses.curs_set(0)
            text = None
            key = stdscr.getch()
            curses.curs_set(0)
            if key == ord('q'):
                break
            if key == ord('t'):
                curses.flushinp()
                curses.curs_set(1)
                text = print_input_box(stdscr, sh, sw)

        except curses.error:
            pass


def start_color():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)


def do_scraping(text) -> GoogleTranslate:
    scrap = GoogleScraper()
    google_translate = scrap.scraping(text)
    # trans =google_translate.get_translations()
    return google_translate


def print_options(windows):
    sh, sw = windows.getmaxyx()
    windows.addstr(sh - 1, 5, " t ", curses.color_pair(1))
    windows.addstr(sh - 1, 9, "new translation")
    windows.addstr(sh - 1, 25, " q ", curses.color_pair(1))
    windows.addstr(sh - 1, 28, " exit ")


if __name__ == '__main__':
    curses.wrapper(show_main)

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# a[2] translation
