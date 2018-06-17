
import asyncio

from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtCore import QUrl


class BasePage(QWebEnginePage):
    def __init__(self, url, future):
        print(asyncio.get_event_loop())

        super(BasePage, self).__init__()
        self.url = url
        # self.page = QWebEnginePage()
        self.page = self
        self.future = future
        self.page.loadFinished.connect(self._on_load_finished)

    def run(self):
        self._prepare()
        self._make_request()

    def _prepare(self):
        pass

    def _make_request(self):
        self.page.load(QUrl(self.url))

    def _on_load_finished(self):
        self.page.toHtml(self._send_html)

    def _send_html(self, html):
        """
        Since toHtml is async, this callback method should send html to receiver.
        :param html:
        :return:
        """
        self.future.set_result(html)



