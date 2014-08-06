#coding: utf-8
from Tkinter import *
from tkintertable.Tables import TableCanvas

import config


class MainWindow(object):
    def __init__(self, controller):
        self.controller = controller
        self.window = Tk()
        # self.window.geometry('1600x' + str(self.window.winfo_screenheight()))
        self.window.geometry(config.MAIN_WINDOW_DEFAULT_WIDTH + 'x' + config.MAIN_WINDOW_DEFAULT_HEIGHT)
        self.window.bind_all('<Key>', self.key)
        self.frame = Frame(self.window, width=200, height=200, bd=11)
        self.frame.pack(expand=True, fill=BOTH)
        self.label_value = StringVar()
        self.label_value.set('test')
        self.label = Label(self.frame, textvariable=self.label_value, anchor=NW, justify=CENTER, wraplength=398)
        # don't mix grid and pack
        self.label.grid(row=0)
        self.table = TableCanvas(self.frame, cols=0, rows=0)
        self.table.createTableFrame()

        self.sort_order = 0
        # self.window.mainloop()

    def key(self, event):
        if event.keysym == 'Escape':
            self.window.destroy()
            return
        elif event.keysym == 'Return':
            return
        else:
            # self.label_value.set(self.controller.query_builder.get_query_for_label())
            self.controller.key_pressed_event(event.keysym)
            return

    def set_data_to_table(self, dct, sortColumn=''):
        self.table.model.createEmptyModel()
        self.table.model.importDict(dct)
        self.table.sortTable(columnName=sortColumn)
        self.table.redrawTable()

    def sort_table(self, sortColumn):
        self.table.sortTable(columnName=sortColumn, reverse=self.sort_order)
        if self.sort_order == 0:
            self.sort_order = 1
        else:
            self.sort_order = 0