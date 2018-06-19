

from src.page import EnginePage


class BaseSender(object):
    def __init__(self, page_cls):
        self.page_cls = page_cls

    def send(self, url, future, **kwargs):
        return self.page_cls(url, future, **kwargs).run()


class EngineSender(BaseSender):
    def __init__(self):
        BaseSender.__init__(self, EnginePage)
