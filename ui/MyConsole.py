import curses
from curses import textpad

from models.Listener import Listener
from ui.GoogleTranslatePrinter import GoogleTranslatePrinter
from ui.Position import Position
from ui.Size import Size
from view_model.TranslatorVM import TranslatorVM


class MyConsole(Listener):
    def __init__(self):
        self.vm = TranslatorVM(self)
        self.windows_one = None
        self.windows_two = None
        self.window_status = None
        self.windows = None
        self.state = "ready"
        self.sh = 0
        self.sw = 0
        self.prev_text = " "

    def show_main(self, stdscr):
        self.windows = stdscr
        self.windows.nodelay(False)
        curses.curs_set(1)

        self.sh, self.sw = stdscr.getmaxyx()
        self.start_color()
        self.print_options()
        self.print_state(state="Starting ...")
        self.vm.init_scraping()
        self.print_state(state="Ready")
        text = self.print_input_box(stdscr)
        self.create_win_result(stdscr)
        self.print_state(state="Loading")
        while True:
            try:
                if self.is_valid_text(text):
                    # self.print_state(state="I find " + text[:10])
                    self.clear_results()
                    self.vm.do_scraping(text)
                    translate_printer = GoogleTranslatePrinter(self.vm)

                    translate_printer.print_principal_result(self.windows)
                    stdscr.refresh()
                    translate_printer.print_translations(self.windows_two)
                    translate_printer.print_definitions(self.windows_one)
                    self.refresh_results()
                    self.prev_text = text
                    curses.curs_set(0)
                else:
                    self.print_state("Please input ")
                curses.curs_set(0)
                key = stdscr.getch()
                if key == -1:
                    self.print_state("no input")
                if key == ord('q'):
                    break
                if key == ord('t'):
                    curses.flushinp()
                    curses.curs_set(1)
                    text = self.print_input_box(stdscr, text)

            except curses.error:
                pass

    def on_message(self, message: str):
        self.print_state(message)

    def on_error(self, message: str):
        self.print_state(message)

    def is_valid_text(self, text: str):
        if text is not None:
            text = text.strip()
            return len(text) >= 2 and self.prev_text != text
        return False

    def clear_results(self):
        if self.windows_one is not None and self.windows_two is not None:
            self.windows_one.clear()
            self.windows_two.clear()

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
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def print_state(self, state):
        self.state = state
        sh, sw = self.window_status.getmaxyx()
        self.window_status.addstr(0, 10, "                           ")
        self.window_status.addstr(0, 10, self.state)
        self.window_status.refresh()

    def print_options(self):
        sh, sw = self.windows.getmaxyx()
        keys = {"key": "q", "option": "exit"}
        self.window_status = curses.newwin(1, sw - 3, sh - 1, 1)
        sh, sw = self.window_status.getmaxyx()
        #self.window_status.addstr(0, 1, (sw - 10) * " ", curses.color_pair(1))
        self.window_status.addstr(0, sw - 20, " t ", curses.color_pair(1))
        self.window_status.addstr(0, sw - 16, "New translation")
        self.window_status.addstr(0, sw - 40, " q ", curses.color_pair(1))
        self.window_status.addstr(0, sw - 36, "Exit")
        self.windows.refresh()
        self.window_status.refresh()

    def my_raw_input(self, stdscr, pos: Position, prompt_string, prev_text) -> str:
        curses.echo()

        stdscr.addstr(pos.y, pos.x, prompt_string)
        # stdscr.move(pos.y, len(prompt_string) + pos.x)
        self.windows.addstr(pos.y, len(prompt_string) + pos.x, len(prev_text) * " ")
        input = stdscr.getstr(pos.y, len(prompt_string) + pos.x, 100)
        stdscr.refresh()

        return input.decode("utf-8")

    def print_box(self, stdscr, pos: Position, size: Size):
        box = [[pos.y, pos.x], [pos.y + size.height, pos.x + size.width]]
        textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    def print_input_box(self, stdscr, text=""):
        sh, sw = stdscr.getmaxyx()
        self.print_box(stdscr, Position(3, 3), Size(2, int(sw / 2)))
        text = self.my_raw_input(stdscr, Position(4, 4), "Search: ", text)
        return text

    def divide_window(self, windows):
        sh, sw = windows.getmaxyx()
        oy, ox = windows.getbegyx()
        w_one = curses.newwin(sh, int(sw / 2) - 2, oy, ox + 1)
        w_two = curses.newwin(sh, int(sw / 2) - 4, oy, int(sw / 2) + 2)
        return w_one, w_two
