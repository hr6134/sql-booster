from Tkinter import *


class InputWindow(object):
    def __init__(self, controller):
        self.controller = controller
        self.window = Tk()

        self.frame = Frame(self.window)
        self.frame.pack()

        self.entry = Entry(self.frame)
        self.entry.bind('<KeyRelease>', self.key)
        self.entry['width'] = 100
        self.entry.focus()
        self.entry.pack()

        self.manual_input = True
        self.string_gaps = []

    def add(self, string):
        self.entry.insert(0, string.strip())

    def key(self, event):
        if event.keysym == 'Return':
            self.controller.set_tmp_data(self.entry.get())
            self.window.destroy()
            return
        if event.keysym == 'Escape':
            self.window.destroy()
            return
        if event.keysym == 'grave':
            tmp = self.entry.get().replace('`', '')
            self.entry.delete(0, len(self.entry.get()))
            self.entry.insert(0, tmp)
            self.manual_input = not self.manual_input
            return

        if not self.manual_input:
            index = self.entry.index('insert')

            tmp = self.entry.get()
            tmp = tmp[0:index - 1] + tmp[index:]
            self.entry.delete(0, len(self.entry.get()))
            self.entry.insert(0, tmp)
            self.calculate_string_gaps()

            if event.keysym == 'k':
                i = self.string_gaps.index(index - 1)
                if i < (len(self.string_gaps) - 1):
                    self.entry.icursor(self.string_gaps[i + 1])
            if event.keysym == 'j':
                i = self.string_gaps.index(index - 1)
                if i > 0:
                    self.entry.icursor(self.string_gaps[i - 1])

            # aggregate functions
            if event.keysym == 's':
                l = tmp.split(', ')
                i = self.string_gaps.index(index - 1)
                l[i] = 'sum(' + l[i] + ')'
                tmp = ', '.join(l)
                self.entry.delete(0, len(self.entry.get()))
                self.entry.insert(0, tmp)
            if event.keysym == 'c':
                l = tmp.split(', ')
                i = self.string_gaps.index(index - 1)
                l[i] = 'count(' + l[i] + ')'
                tmp = ', '.join(l)
                self.entry.delete(0, len(self.entry.get()))
                self.entry.insert(0, tmp)
            if event.keysym == 'a':
                l = tmp.split(', ')
                i = self.string_gaps.index(index - 1)
                l[i] = 'avg(' + l[i] + ')'
                tmp = ', '.join(l)
                self.entry.delete(0, len(self.entry.get()))
                self.entry.insert(0, tmp)
            if event.keysym == 'd':
                l = tmp.split(', ')
                i = self.string_gaps.index(index - 1)
                l[i] = 'max(' + l[i] + ')'
                tmp = ', '.join(l)
                self.entry.delete(0, len(self.entry.get()))
                self.entry.insert(0, tmp)
            if event.keysym == 'f':
                l = tmp.split(', ')
                i = self.string_gaps.index(index - 1)
                l[i] = 'min(' + l[i] + ')'
                tmp = ', '.join(l)
                self.entry.delete(0, len(self.entry.get()))
                self.entry.insert(0, tmp)

    def calculate_string_gaps(self):
        self.string_gaps = []
        tmp = self.entry.get()
        for i in tmp.split(', '):
            self.string_gaps.append(tmp.find(i))
        self.string_gaps.append(len(tmp))