
import asyncio

from pyppeteer import launch

from ..config import BROWSER_OPTIONS


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

    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    async def page(self, future):
        # page = await self.get_page(self.browser)
        page = await self.browser.newPage()
        await page.goto(self.url)
        html = await page.content()
        await page.close()
        future.set_result(html)

    @staticmethod
    def get_page(browser):
        return browser.newPage()

    @staticmethod
    def load_url(page, url):
        return page.goto(url)


