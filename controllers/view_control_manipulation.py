class Controlling(object):
    def __init__(self, view):
        self.view = view

    def key_pressed_event(self, key):
        if key == 'k':
            if self.view.current_active_pos < (self.view.resultList.size() - 1):
                self.view.current_active_pos += 1
            self.view.resultList.activate(self.view.current_active_pos)
            self.view.resultList.yview_scroll(-self.view.resultList.size(), 'units')
            self.view.resultList.yview_scroll(self.view.current_active_pos, 'units')
        if key == 'j':
            if self.view.current_active_pos > 0:
                self.view.current_active_pos -= 1
            self.view.resultList.activate(self.view.current_active_pos)
            self.view.resultList.yview_scroll(-self.view.resultList.size(), 'units')
            self.view.resultList.yview_scroll(self.view.current_active_pos, 'units')
        if key == 'c':
            self.view.resultList.select_clear(0, self.view.resultList.size())
