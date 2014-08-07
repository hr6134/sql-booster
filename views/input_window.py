from Tkinter import *


class InputWindowType(object):
    DEFAULT = 0
    WHERE = 1


class InputWindow(object):
    def __init__(self, controller, type=InputWindowType.DEFAULT, manual_input=True):
        self.controller = controller
        self.window = Tk()

        self.frame = Frame(self.window)
        self.frame.pack()

        self.entry = Entry(self.frame)
        self.entry.bind('<KeyPress>', self.key)
        self.entry.bind('<Control-k>', self.move_right)
        self.entry.bind('<Control-j>', self.move_left)

        self.entry['width'] = 100
        self.entry.focus()
        self.entry.pack()

        self.manual_input = manual_input
        self.string_gaps = []

    def add(self, string):
        self.entry.insert(0, string.strip())

    def move_right(self, event):
        index = self.entry.index('insert')
        self.calculate_string_gaps()
        i = self.string_gaps.index(index)
        if i < (len(self.string_gaps) - 1):
            self.entry.icursor(self.string_gaps[i + 1])
        return 'break'

    def move_left(self, event):
        index = self.entry.index('insert')
        self.calculate_string_gaps()
        i = self.string_gaps.index(index)
        if i > 0:
            self.entry.icursor(self.string_gaps[i - 1])
        return 'break'

    def key(self, event):
        if event.keysym == 'Return':
            self.controller.set_tmp_data(self.entry.get())
            self.window.destroy()
            return 'break'
        if event.keysym == 'Escape':
            self.window.destroy()
            return 'break'
        if event.keysym == 'grave':
            self.manual_input = not self.manual_input
            return 'break'

        if not self.manual_input:
            index = self.entry.index('insert')
            self.calculate_string_gaps()
            l = self.entry.get().split(', ')
            try:
                i = self.string_gaps.index(index)
            except ValueError:
                return 'break'
            if i > len(l)-1:
                return 'break'

            # aggregate functions
            if event.keysym == 's':
                l[i] = 'sum(' + l[i] + ')'
            if event.keysym == 'c':
                l[i] = 'count(' + l[i] + ')'
            if event.keysym == 'a':
                l[i] = 'avg(' + l[i] + ')'
            if event.keysym == 'd':
                l[i] = 'max(' + l[i] + ')'
            if event.keysym == 'f':
                l[i] = 'min(' + l[i] + ')'

            self.entry.delete(0, len(self.entry.get()))
            self.entry.insert(0, ', '.join(l))
            return 'break'

    def calculate_string_gaps(self):
        self.string_gaps = []
        tmp = self.entry.get()
        for i in tmp.split(', '):
            self.string_gaps.append(tmp.find(i))
        self.string_gaps.append(len(tmp))