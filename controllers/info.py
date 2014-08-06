from views import info_window


class Info(object):
    def __init__(self, master):
        self.info_win = info_window.InfoWindow(master)
        self.info_win.window.mainloop()
