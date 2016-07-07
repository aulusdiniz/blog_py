class Signals:

    def __init__(self, name):
        self.name = name
        self.handlers = []

    def connect(self, handler):
        if handler not in self.handlers:
            self.handlers.append(handler)
        return handler

    def trigger(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)

    def disconnect(self, handler):
        self.handlers = [f for f in self.handlers if f != handler]
