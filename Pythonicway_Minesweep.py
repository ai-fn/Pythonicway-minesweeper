import os.path
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import random
import logging

logger = logging.getLogger(__name__)


def main():
    Minesweeper()


class Minesweeper:

    def __init__(self, level='beginner'):
        self.flags = 0
        self.mines_num = 0
        self.square_size = 0
        self.grid_size = 0
        self.score = 0
        self.record = 0
        self.root = Tk()
        self.clicked = set()
        self.level = level
        self.__set_level(self.level.lower())
        self.mines = set(random.sample(range(1, self.grid_size ** 2 + 1), self.mines_num))
        self.__create_window()
        self.__draw_field()
        self.root.mainloop()

    def __draw_field(self) -> None:
        """ Draw rectangles on game field """
        self.c = Canvas(
            self.canvas_frame, width=self.grid_size * self.square_size, height=self.grid_size * self.square_size
        )
        self.c.bind("<Button-1>", self.__click)
        self.c.bind("<Button-3>", self.__mark_mine)
        self.c.pack()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.c.create_rectangle(
                    i * self.square_size, j * self.square_size,
                    i * self.square_size + self.square_size,
                    j * self.square_size + self.square_size,
                    fill='gray'
                )

    def __create_window(self) -> None:
        """ Build root window """
        self.root.title("Pythonicway Minesweeper")
        self.root_size = self.grid_size * self.square_size
        self.x = (self.root.winfo_screenwidth() - self.root_size) / 2.2
        self.y = (self.root.winfo_screenheight() - self.root_size) / 2.3
        self.root.wm_geometry("+%d+%d" % (self.x, self.y))
        self.frame = Frame(self.root)
        self.canvas_frame = Frame(self.root)
        self.frame.pack()
        self.canvas_frame.pack()

        if os.path.isfile(f'Minesweeper_record_{self.level}.txt'):
            with open(f'Minesweeper_record_{self.level}.txt', 'r') as rd:
                self.record = int(rd.read())

        self.flags_l = Label(self.frame, text=f'Flags: {self.flags}')
        self.record_l = Label(self.frame, text=f'Record: {self.record}')
        self.score_l = Label(self.frame, text='Score: 0')
        self.score_l.pack(side='left', padx=20.0)
        self.record_l.pack(side='right', padx=20.0)
        self.flags_l.pack(side='top')
        self.main_menu = Menu(self.root)
        self.root.config(menu=self.main_menu)
        self.menu = Menu(self.main_menu, tearoff=0)
        self.lvl_menu = Menu(self.menu, tearoff=0)
        self.lvl_menu.add_command(label='Beginner', command=lambda: self.__change_level("beginner"))
        self.lvl_menu.add_command(label='Middle', command=lambda: self.__change_level("middle"))
        self.lvl_menu.add_command(label='Pro', command=lambda: self.__change_level("pro"))
        self.menu.add_cascade(label='Set Level', menu=self.lvl_menu)
        self.main_menu.add_cascade(label='Settings', menu=self.menu)

    def __check_mines(self, neighbors) -> int:
        """ Return mines count around neighbours"""
        return len(self.mines.intersection(neighbors))

    def __generate_neighbors(self, square) -> set[int]:
        """ Return neighbours """
        if square == 1:
            data = {self.grid_size + 1, 2, self.grid_size + 2}
        elif square == self.grid_size ** 2:
            data = {square - self.grid_size, square - 1, square - self.grid_size - 1}
        elif square == self.grid_size:
            data = {self.grid_size - 1, self.grid_size * 2, self.grid_size * 2 - 1}
        elif square == self.grid_size ** 2 - self.grid_size + 1:
            data = {square + 1, square - self.grid_size, square - self.grid_size + 1}
        elif square < self.grid_size:
            data = {square + 1, square - 1, square + self.grid_size,
                    square + self.grid_size - 1, square + self.grid_size + 1}
        elif square > self.grid_size ** 2 - self.grid_size:
            data = {square + 1, square - 1, square - self.grid_size,
                    square - self.grid_size - 1, square - self.grid_size + 1}
        elif square % self.grid_size == 0:
            data = {square + self.grid_size, square - self.grid_size, square - 1,
                    square + self.grid_size - 1, square - self.grid_size - 1}
        elif square % self.grid_size == 1:
            data = {square + self.grid_size, square - self.grid_size, square + 1,
                    square + self.grid_size + 1, square - self.grid_size + 1}
        else:
            data = {square - 1, square + 1, square - self.grid_size, square + self.grid_size,
                    square - self.grid_size - 1, square - self.grid_size + 1,
                    square + self.grid_size + 1, square + self.grid_size - 1}
        return data

    def __clearance(self, ids) -> None:
        """ Iterative field cleaning function """
        self.clicked.add(ids)
        ids_neigh = self.__generate_neighbors(ids)
        around = self.__check_mines(ids_neigh)
        self.c.itemconfig(ids, fill="green")

        if around == 0:
            self.score += 10
            neigh_list = list(ids_neigh)
            while len(neigh_list) > 0:
                item = neigh_list.pop()
                self.score += 10
                self.c.itemconfig(item, fill="green")
                item_neigh = self.__generate_neighbors(item)
                item_around = self.__check_mines(item_neigh)
                if item_around > 0:
                    if item not in self.clicked:
                        # try:
                        x1, y1, x2, y2 = self.c.coords(item)
                        # except Exception:
                            # x1, y1 = self.c.coords(item)
                        self.c.create_text(x1 + self.square_size / 2,
                                           y1 + self.square_size / 2,
                                           text=str(item_around),
                                           font="Arial {}".format(int(self.square_size / 2)),
                                           fill='yellow')
                else:
                    neigh_list.extend(set(item_neigh).difference(self.clicked))
                    neigh_list = list(set(neigh_list))
                self.clicked.add(item)
        else:
            x1, y1, x2, y2 = self.c.coords(ids)
            self.c.create_text(x1 + self.square_size / 2,
                               y1 + self.square_size / 2,
                               text=str(around),
                               font="Arial {}".format(int(self.square_size / 2)),
                               fill='yellow')
            self.score += 10
        if len(self.clicked) == self.grid_size ** 2:
            if messagebox.askyesno(message='YOU WON!!!\nDo you wont restart?', title='Congratulations!'):
                self.root.destroy()
                Minesweeper(self.level)
            else:
                self.root.destroy()

    def __click(self, event) -> None:
        """ Left mouse button click handler """
        ids = self.c.find_overlapping(event.x, event.y, event.x, event.y)[0]
        if ids in self.mines:
            if self.score > self.record:
                main.record = self.score
                with open(f'Minesweeper_record_{self.level}.txt', 'w') as file:
                    file.write(f'{main.record}')
            self.score = 0
            self.c.itemconfig(CURRENT, fill="red")
            self.__restart_game(message='Do you wont to restart?', title='GAME OVER')
        elif ids not in self.clicked:
            self.__clearance(ids)
            self.score_l.config(text=f'Score: {self.score}')
            self.c.itemconfig(CURRENT, fill="green")
        self.c.update()

    def __mark_mine(self, event) -> None:
        """ Right mouse button click handler """
        ids = self.c.find_overlapping(event.x, event.y, event.x, event.y)[0]
        if ids not in self.clicked:
            self.flags -= 1
            self.flags_l.config(text=f'Flags: {self.flags}')
            self.clicked.add(ids)
            self.c.itemconfig(CURRENT, fill="yellow")
        else:
            self.flags += 1
            self.flags_l.config(text=f'Flags: {self.flags}')
            self.clicked.remove(ids)
            self.c.itemconfig(CURRENT, fill="gray")
        if len(self.clicked) == self.grid_size ** 2:
            self.__restart_game(message='YOU WON!!!\nDo you wont restart?', title='CONGRATULATIONS!')

    def __set_level(self, level: str) -> None:
        """ Set specified game level """
        levels = {
            'beginner': (10, 20, 16),
            'middle': (16, 20, 40),
            'pro': (23, 20, 99)
        }

        try:
            self.grid_size, self.square_size, self.mines_num = levels[level]
        except KeyError:
            logger.debug("Unknown level '%s', set default: beginner" % level)
            self.grid_size, self.square_size, self.mines_num = levels['beginner']
        self.flags = self.mines_num

    def __change_level(self, level: str = 'beginner'):
        self.root.destroy()
        Minesweeper(level)

    def __restart_game(self, message: str, title: str):
        if messagebox.askyesno(message, title):
            self.root.destroy()
            Minesweeper(self.level)
        else:
            self.root.destroy()


if __name__ == '__main__':
    main()
