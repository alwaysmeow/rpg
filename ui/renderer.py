import pyglet

from ui.log_window import LogWindow

class Renderer:
    def __init__(self, width=800, height=600, title="Combat Log"):
        self.window = LogWindow(width=width, height=height, caption=title, resizable=True)

    def get_sink(self):
        return self.window.sink

    def run(self):
        pyglet.app.run()