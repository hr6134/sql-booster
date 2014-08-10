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
        self.entry.bind('<Control-d>', self.insert_and)
        self.entry.bind('<Control-f>', self.insert_or)
        self.entry.bind('<Control-s>', self.insert_like)

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

    def insert_or(self, event):
        index = self.entry.index('insert')
        splited = self.entry.get()[index:].split()
        if splited and splited[0] == 'and':
            tmp = 'or' + self.entry.get()[index+3:]
            self.entry.delete(index, len(self.entry.get()))
            self.entry.insert(index, tmp)
        else:
            self.entry.insert(index, 'or')
        self.entry.icursor(index)
        return 'break'

    def insert_and(self, event):
        index = self.entry.index('insert')
        splited = self.entry.get()[index:].split()
        if splited and splited[0] == 'or':
            tmp = 'and' + self.entry.get()[index+2:]
            self.entry.delete(index, len(self.entry.get()))
            self.entry.insert(index, tmp)
        else:
            self.entry.insert(index, 'and')
        self.entry.icursor(index)
        return 'break'

    def insert_like(self, event):
        index = self.entry.index('insert')
        splited = self.entry.get()[index:].split()
        if splited and splited[0] in ('=', '>', '<'):
            tmp = 'like' + self.entry.get()[index+1:]
            self.entry.delete(index, len(self.entry.get()))
            self.entry.insert(index, tmp)
        else:
            self.entry.insert(index, 'like')
        self.entry.icursor(index)
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
        print tmp
        print tmp.split(' ')

        n = 0
        self.string_gaps.append(0)
        for i in tmp.split(' '):
            n += len(i) + 1
            self.string_gaps.append(n)
        self.string_gaps[-1] = self.string_gaps[-1] - 1

        print self.string_gaps
        self.string_gaps.append(len(tmp))