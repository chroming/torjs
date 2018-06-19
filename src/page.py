
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtCore import QUrl


class EnginePage(QWebEnginePage):
    def __init__(self, url, future):
        super(EnginePage, self).__init__()
        self.url = url
        self.future = future
        self.loadFinished.connect(self._on_load_finished)

    def run(self):
        self._prepare()
        self._make_request()

    def _prepare(self):
        pass

    def _make_request(self):
        self.load(QUrl(self.url))

    def _on_load_finished(self):
        self.toHtml(self._send_html)

    def _send_html(self, html):
        """
        Since toHtml is async, this callback method should send html to future.
        :param html:
        :return:
        """
        self.future.set_result(html)



