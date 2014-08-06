from Tkinter import *

from controllers import view_control_manipulation


class SearchTableView(object):
    current_active_pos = 0

    def __init__(self, controller, selectmode='multiple'):
        self.controller = controller
        self.window = Tk()
        # self.window.bind('<Key>', self.key)
        self.frame = Frame(self.window, width=100, height=100, bd=11)
        self.frame.pack()
        self.entry = Entry(self.frame)
        self.entry['width'] = 20
        self.entry.bind('<KeyRelease>', self.filter_list)
        self.entry.pack()
        self.entry.focus()
        self.resultList = Listbox(self.frame, selectmode=selectmode)
        self.resultList.bind('<KeyRelease>', self.key)
        self.resultList.pack()

    def add(self, l):
        self.list_content = l
        for i in self.list_content:
            self.resultList.insert(END, i)
        if self.resultList.size() < 10:
            self.resultList.focus()
        return self

    def key(self, event):
        if event.keysym == 'Escape':
            self.window.destroy()
            return
        if event.keysym == 'Return' or event.keysym == 'a':
            self.controller.set_tmp_data(self.resultList)
            self.window.destroy()
            return
        else:
            view_control_manipulation.Controlling(self).key_pressed_event(event.keysym)

    def filter_list(self, event):
        if event.keysym == 'Escape':
            self.window.destroy()
        if event.keysym != 'Tab':
            self.resultList.delete(0, self.resultList.size())
            for i in self.list_content:
                if type(i) == str:
                    j = i
                else:
                    j = i[0]
                if j.lower().find(self.entry.get().lower()) != -1:
                    self.resultList.insert(END, i)

            if self.resultList.size() == 0:
                tmp = self.entry.get()
                self.entry.delete(0, len(self.entry.get()))
                self.entry.insert(0, tmp[:-1])
                self.filter_list(event)
                print('\a')
