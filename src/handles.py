
import json

from tornado import web
from tornado.concurrent import Future

from src.sender import EngineSender


class BaseHandler(web.RequestHandler):

    async def get(self):
        future = Future()
        sender = EngineSender()
        await sender.send(self.url, future)
        html = await future
        await self.write(html)

    async def post(self):
        sender = EngineSender()
        body = self._json_body(self.request.body)
        url = body.get('url')
        future = Future()
        sender.send(url, future)
        html = await future
        self.write(html)

    def _json_body(self, json_body):
        return json.loads(json_body)

    def initialize(self):
        print('%s is connected!' % self.request)

    def on_finish(self):
        print('%s is finished!' % self.request)

    @property
    def url(self):
        return self.get_argument('url')

    def ___getattr__(self, name):
        """
        :param name:
        :return:
        """
        return self.get_argument(name)


class HtmlHandler(BaseHandler):

    def get(self):
        super(HtmlHandler, self).get()

