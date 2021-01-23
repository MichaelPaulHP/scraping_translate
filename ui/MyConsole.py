import curses
from curses import textpad

from ui.GoogleTranslatePrinter import GoogleTranslatePrinter
from ui.Position import Position
from ui.Size import Size
from view_model.TranslatorVM import TranslatorVM


class MyConsole:
    def __init__(self):
        self.translator_print = GoogleTranslatePrinter()
        self.vm = TranslatorVM()
        self.windows_one = None
        self.windows_two = None
        self.windows = None
        self.state = "ready"
        self.sh = 0
        self.sw = 0

    def show_main(self, stdscr):
        self.windows = stdscr
        curses.curs_set(1)
        stdscr.nodelay(1)
        self.sh, self.sw = stdscr.getmaxyx()
        self.start_color()
        self.print_options()
        self.print_state(state="Ready")

        text = None
        text = self.print_input_box(stdscr)
        self.create_win_result(stdscr)
        self.print_state(state="Loading")
        while True:
            try:
                if self.is_valid_text(text):
                    self.print_state(state="I find " + text[:10])
                    # google_translate = do_scraping(text)
                    self.print_state(state="I Found " + text[:10])

                    # print_principal_result(stdscr, google_translate)
                    stdscr.refresh()

                    # print_translations(two, google_translate)
                    # print_definitions(one, google_translate)

                    curses.curs_set(0)

                curses.curs_set(0)
                key = stdscr.getch()
                if key == ord('q'):
                    break
                if key == ord('t'):
                    curses.flushinp()
                    curses.curs_set(1)
                    text = self.print_input_box(stdscr, text)

            except curses.error:
                pass

    def is_valid_text(self, text):
        return text is not None and len(text) >= 2

    def refresh_results(self):
        if self.windows_one is not None and self.windows_two is not None:
            self.windows_one.refresh()
            self.windows_two.refresh()

    def create_win_result(self, windows):
        sh, sw = windows.getmaxyx()
        win_result = curses.newwin(sh - 7, sw, 6, 0)
        self.windows_one, self.windows_two = self.divide_window(win_result)

    def start_color(self):

        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def print_state(self, state):
        self.state = state
        sh, sw = self.windows.getmaxyx()
        self.windows.addstr(sh - 1, 10, "                           ")
        self.windows.addstr(sh - 1, 10, self.state)

    def print_options(self):
        sh, sw = self.windows.getmaxyx()
        keys = {"key": "q", "option": "exit"}

        self.windows.addstr(sh - 1, sw - 20, " t ", curses.color_pair(1))
        self.windows.addstr(sh - 1, sw - 16, "New translation")
        self.windows.addstr(sh - 1, sw - 40, " q ", curses.color_pair(1))
        self.windows.addstr(sh - 1, sw - 36, "Exit")

    def my_raw_input(self, stdscr, pos: Position, prompt_string, prev_text) -> str:
        curses.echo()

        stdscr.addstr(pos.y, pos.x, prompt_string)
        # stdscr.move(pos.y, len(prompt_string) + pos.x)
        self.windows.addstr(pos.y, len(prompt_string) + pos.x, len(prev_text) * " ")
        input = stdscr.getstr(pos.y, len(prompt_string) + pos.x, 50)
        stdscr.refresh()

        return input.decode("utf-8")

    def print_box(self, stdscr, pos: Position, size: Size):
        box = [[pos.y, pos.x], [pos.y + size.height, pos.x + size.width]]
        textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    def print_input_box(self, stdscr, text=""):
        # print_box(stdscr, Position(3, 3), Size(2, int(sw / 2)))
        text = self.my_raw_input(stdscr, Position(4, 4), "Search: ", text)
        return text

    def divide_window(self, windows):
        sh, sw = windows.getmaxyx()
        oy, ox = windows.getbegyx()
        w_one = curses.newwin(sh, int(sw / 2) - 2, oy, ox)
        w_two = curses.newwin(sh, int(sw / 2) - 4, oy, int(sw / 2) + 2)
        return w_one, w_two
