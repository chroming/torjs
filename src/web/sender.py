

from src.brower.base import BaseBrowser, BasePage
from src.engine.base import BasePage as EnginePage


class BaseSender(object):
    def __init__(self):
        self.browser = BaseBrowser().browser()

    def send(self, url, future):
        return BasePage(self.browser, url).page(future)


class EngineSender(object):
    def send(self, url, future):
        return EnginePage(url, future).run()