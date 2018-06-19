
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWebEngineCore import QWebEngineHttpRequest
from PyQt5.QtCore import QUrl


class EnginePage(QWebEnginePage):
    def __init__(self, url, future, method='get', **kwargs):
        super(EnginePage, self).__init__()
        self.url = url
        self.future = future
        self.method = method
        self.kwargs = kwargs
        self.loadFinished.connect(self._on_load_finished)

    def run(self):
        self._prepare()
        self._make_request()

    def _prepare(self):
        pass

    def _make_request(self):
        self.load(self._request(self.url, self.method, **self.kwargs))

    @staticmethod
    def _set_headers(headers):
        return headers

    @staticmethod
    def _set_postdata(data):
        return data

    def _request(self, url, method='get', **kwargs):
        req = QWebEngineHttpRequest(QUrl(url))
        req.setMethod(QWebEngineHttpRequest.Post if method == 'post' else QWebEngineHttpRequest.Get)
        if 'headers' in kwargs:
            req.setHeader(self._set_headers(kwargs.get('headers')))
        if 'body' in kwargs:
            req.setPostData(self._set_postdata(kwargs.get('body')))

    def _on_load_finished(self):
        self.toHtml(self._send_html)

    def _send_html(self, html):
        """
        Since toHtml is async, this callback method should send html to future.
        :param html:
        :return:
        """
        self.future.set_result(html)



