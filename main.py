#!/usr/bin/env python
from controllers import window_chooser


class Main(object):
    def start(self):
        window_chooser.WindowChooser()


if __name__ == "__main__":
    Main().start()
