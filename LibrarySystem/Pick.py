
   ### -------------------------------------------------------------------------
   #   For more information, please read https://github.com/wong2/pick
   #   This is a fork script from https://github.com/wong2/pick
   ### -------------------------------------------------------------------------

'''LICENCE

The MIT License (MIT)

Copyright (c) 2016 Wang Dàpéng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''


import curses
import os
import platform

from dataclasses import dataclass, field
from typing import Generic, Callable, List, Optional, Dict, Union, Tuple, TypeVar

from .Constants import ASCII_ART, KNOWN_BUG
from .Exceptions import UserResizeTerminalException


__all__ = ["Picker", "pick"]


KEYS_ENTER = (curses.KEY_ENTER, ord("\n"), ord("\r"))
KEYS_UP = (curses.KEY_UP, ord("k"))
KEYS_DOWN = (curses.KEY_DOWN, ord("j"))
KEYS_SELECT = (curses.KEY_RIGHT, ord(" "))
KEYS_RESIZE = (curses.KEY_RESIZE, ord("ƚ"))

CUSTOM_HANDLER_RETURN_T = TypeVar("CUSTOM_HANDLER_RETURN_T")
KEY_T = int
OPTIONS_MAP_VALUE_T = TypeVar("OPTIONS_MAP_VALUE_T")
PICK_RETURN_T = Tuple[OPTIONS_MAP_VALUE_T, int]


@dataclass
class Picker(
    Generic[CUSTOM_HANDLER_RETURN_T,
            OPTIONS_MAP_VALUE_T]
    ):
    """The :class:`Picker <Picker>` object
    :param options: a list of options to choose from
    :param title: (optional) a title above options list
    :param multiselect: (optional) if true its possible to select multiple values by hitting SPACE, defaults to False
    :param indicator: (optional) custom the selection indicator
    :param default_index: (optional) set this if the default selected option is not the first one
    :param options_map_func: (optional) a mapping function to pass each option through before displaying
    :param print_ctrl_c: (optional) whether to print ctrl-c to return to last screen
    """

    options: List[OPTIONS_MAP_VALUE_T]
    title: Optional[str] = None
    indicator: str = "*"
    default_index: int = 0
    multiselect: bool = False
    min_selection_count: int = 0
    options_map_func: Callable[[OPTIONS_MAP_VALUE_T], Optional[str]] = str
    print_ctrl_c: bool = False
    print_ascii_art: bool = True
    selected_indexes: List[int] = field(
        init = False, default_factory = list
        )
    custom_handlers: Dict[KEY_T, Callable[["Picker"], CUSTOM_HANDLER_RETURN_T]] = field(
        init = False, default_factory = dict
        )
    index: int = field(
        init = False, default = 0
        )
    scroll_top: int = field(
        init = False, default = 0
        )

    def __post_init__(self) -> None:
        if len(self.options) == 0:
            raise ValueError(
                "options should not be an empty list"
                )

        if self.default_index >= len(self.options):
            raise ValueError(
                "default_index should be less than the length of options"
                )

        if self.multiselect and self.min_selection_count > len(self.options):
            raise ValueError(
                "min_selection_count is bigger than the available options, you will not be able to make any selection"
                )

        if not callable(self.options_map_func):
            raise ValueError(
                "options_map_func must be a callable function"
                )

        self.index = self.default_index

    def register_custom_handler(
        self,
        key: KEY_T,
        func: Callable[
            ["Picker"],
            CUSTOM_HANDLER_RETURN_T
            ]
        ) -> None:

        self.custom_handlers[key] = func


    def move_up(self) -> None:

        self.index -= 1
        if self.index < 0:
            self.index = len(self.options) - 1


    def move_down(self) -> None:

        self.index += 1
        if self.index >= len(self.options):
            self.index = 0


    def mark_index(self) -> None:

        if self.multiselect:
            if self.index in self.selected_indexes:
                self.selected_indexes.remove(self.index)
            else:
                self.selected_indexes.append(self.index)


    def get_selected(self) -> Union[List[PICK_RETURN_T], PICK_RETURN_T]:
        """return the current selected option as a tuple: (option, index)
        or as a list of tuples (in case multiselect==True)
        """

        if self.multiselect:
            return_tuples = []
            for selected in self.selected_indexes:
                return_tuples.append((self.options[selected], selected))
            return return_tuples
        else:
            return self.options[self.index], self.index


    def get_title_lines(self) -> List[str]:

        if self.print_ascii_art:
            init_title = ASCII_ART

            if platform.system() == "Windows":
                init_title += KNOWN_BUG

            if self.print_ctrl_c:
                init_title = init_title + "\n\tPress >CTRL+C< to return\n"

        elif not self.print_ascii_art:
            init_title = ""

            if platform.system() == "Windows":
                init_title += '\n' + KNOWN_BUG

            if self.print_ctrl_c:
                init_title += "\n\tPress >CTRL+C< to return\n"

        if self.title:
            return (init_title + self.title).split("\n") + [""]

        elif not self.title and not self.print_ascii_art and not self.print_ctrl_c:
            if platform.system() == "Windows":
                return ('\n' + KNOWN_BUG).split("\n") + [""]
            else:
                return []

        return (init_title).split("\n") + [""]


    def get_option_lines(self) -> Union[List[str], List[Tuple[str, int]]]:

        lines: Union[List[str], List[Tuple[str, int]]] = []  # type: ignore[assignment]
        for index, option in enumerate(self.options):
            option_as_str = self.options_map_func(option)

            if index == self.index:
                prefix = self.indicator
            else:
                prefix = len(self.indicator) * " "

            line: Union[Tuple[str, int], str]
            if self.multiselect and index in self.selected_indexes:
                format = curses.color_pair(1)
                line = ("{0} {1}".format(prefix, option_as_str), format)
            else:
                line = "{0} {1}".format(prefix, option_as_str)
            lines.append(line)  # type: ignore[arg-type]

        return lines


    def get_lines(self) -> Tuple[List, int]:

        title_lines = self.get_title_lines()
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines  # type: ignore[operator]
        current_line = self.index + len(title_lines) + 1
        return lines, current_line


    def draw(self,
             screen
             ) -> None:
        """draw the curses ui on the screen, handle scroll if needed"""

        screen.clear()

        # Trying to reset the environment variables, but I know it might be useless ...
        os.environ['LINES'] = ''
        os.environ['COLUMNS'] = ''

        x, y = 1, 1  # start point
        max_y, max_x = screen.getmaxyx()
        max_rows = max_y - y  # the max rows we can draw

        lines, current_line = self.get_lines()

        # calculate how many lines we should scroll, relative to the top
        if current_line <= self.scroll_top:
            self.scroll_top = 0
        elif current_line - self.scroll_top > max_rows:
            self.scroll_top = current_line - max_rows

        lines_to_draw = lines[self.scroll_top : self.scroll_top + max_rows]

        for line in lines_to_draw:
            if type(line) is tuple:
                screen.addnstr(y, x, line[0], max_x - 2, line[1])
            else:
                screen.addnstr(y, x, line, max_x - 2)
            y += 1

        screen.refresh()


    def run_loop(
        self,
        screen
        ) -> Union[List[PICK_RETURN_T], PICK_RETURN_T, CUSTOM_HANDLER_RETURN_T]:

        while True:
            self.draw(screen)
            c = screen.getch()
            if c == 3:
                raise KeyboardInterrupt
            elif c in KEYS_RESIZE:
                if platform.system() == "Windows":
                    pass # Nevermind them ...
                    # raise UserResizeTerminalException("Don't ever try to RESIZE THE TERMINAL !!!")
            elif c in KEYS_UP:
                self.move_up()
            elif c in KEYS_DOWN:
                self.move_down()
            elif c in KEYS_ENTER:
                if (
                    self.multiselect
                    and len(self.selected_indexes) < self.min_selection_count
                ):
                    continue
                return self.get_selected()
            elif c in KEYS_SELECT and self.multiselect:
                self.mark_index()
            elif c in self.custom_handlers:
                ret = self.custom_handlers[c](self)
                if ret:
                    return ret


    def config_curses(self) -> None:

        try:
            # use the default colors of the terminal
            curses.use_default_colors()
            # hide the cursor
            curses.curs_set(0)
            # add some color for multi_select
            # @todo make colors configurable
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)
        except:
            # Curses failed to initialize color support, eg. when TERM=vt100
            curses.initscr()


    def _start(
        self,
        screen
        ) -> Union[List[PICK_RETURN_T], PICK_RETURN_T, CUSTOM_HANDLER_RETURN_T]:

        self.config_curses()
        return self.run_loop(screen)


    def start(
        self,
        ) -> Union[List[PICK_RETURN_T], PICK_RETURN_T, CUSTOM_HANDLER_RETURN_T]:

        return curses.wrapper(self._start)


def pick(
    options: List[OPTIONS_MAP_VALUE_T],
    title: Optional[str] = None,
    indicator: str = "*",
    default_index: int = 0,
    multiselect: bool = False,
    min_selection_count: int = 0,
    options_map_func: Callable[[OPTIONS_MAP_VALUE_T], Optional[str]] = str,
    print_ctrl_c: bool = False,
    print_ascii_art: bool = True,
    ) -> Union[List[PICK_RETURN_T], PICK_RETURN_T]:
    """Construct and start a :class:`Picker <Picker>`.
    Usage::
      >>> from pick import pick
      >>> title = 'Please choose an option: '
      >>> options = ['option1', 'option2', 'option3']
      >>> option, index = pick(options, title)
    """

    picker = Picker(
        options,
        title,
        indicator,
        default_index,
        multiselect,
        min_selection_count,
        options_map_func,
        print_ctrl_c,
        print_ascii_art
    )

    return picker.start()
