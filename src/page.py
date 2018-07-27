
import asyncio
from pyppeteer import launch
from config import BROWSER_OPTIONS
import time

from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWebEngineCore import QWebEngineHttpRequest
from PyQt5.QtCore import QUrl
from selenium import webdriver


class EnginePage(QWebEnginePage):
    def __init__(self, url, future, html=None, method='get', **kwargs):
        super(EnginePage, self).__init__()
        self.url = url
        self.qurl = QUrl(url)
        self.future = future
        self.method = method
        self.kwargs = kwargs
        self.html = html
        self.page = self
        self.page.loadFinished.connect(self._on_load_finished)

    def run(self):
        self._prepare()
        self._make_request()

    def _prepare(self):
        pass

    def _make_request(self):
        if self.html:
            self.page.setHtml(self.html, self.qurl)
        else:
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
        return req

    def _on_load_finished(self):
        self.page.toHtml(self._send_html)

    def _get_html_with_js(self):
        return self.runJavaScript('document.documentElement.outerHtml', self._send_html)

    def _send_html(self, html):
        """
        Since toHtml is async, this callback method should send html to future.
        :param html:
        :return:
        """
        try:
            self.future.set_result(html)
        except:
            print('1')


class BaseBrowser(object):

    @staticmethod
    def browser():
        global_loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(launch(**BROWSER_OPTIONS))
        finally:
            # return old state to not affect outer code:
            asyncio.set_event_loop(global_loop)


class BasePage(object):

    def __init__(self, url, future=None, **kwargs):
        # self.browser = BaseBrowser().browser()
        self.future = future
        self.url = url

    async def run(self):
        await self.page(self.future)

    async def page(self, future=None):
        # page = await self.get_page(self.browser)
        browser = await launch(**BROWSER_OPTIONS)
        page = await browser.newPage()
        await page.goto(self.url)
        return page.content()
        #await page.close()
        # future.set_result(html)

    @staticmethod
    def get_page(browser):
        return browser.newPage()

    @staticmethod
    def load_url(page, url):
        return page.goto(url)


class SeleniumPage(object):

    def __init(self, url, future):
        self.url = url
        self.future = future
        self.driver = webdriver.Chrome()

    def run(self):
        self.driver.get(self.url)
        self.future.set_result(self.driver.page_source)