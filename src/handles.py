
import json

from tornado import web
from tornado.concurrent import Future

from src.sender import EngineSender


class HtmlHandler(web.RequestHandler):
    sender = EngineSender()

    async def _handle_req(self, url, method, **kwarg):
        html = await self._send_to_engine(url, method)
        self.write(html)

    async def get(self):
        url = self.get_argument('url')
        self._handle_req(url, 'get')

    async def post(self):
        body = self._json_body(self.request.body)
        url = body.get('url')
        self._handle_req(url, 'post')

    async def _send_to_engine(self, url, method, **kwargs):
        future = Future()
        self.sender.send(url, future, method=method, **kwargs)
        return await future

    def _json_body(self, json_body):
        return json.loads(json_body)

    def initialize(self):
        print('%s is connected!' % self.request)

    def on_finish(self):
        print('%s is finished!' % self.request)

    def ___getattr__(self, name):
        """
        :param name:
        :return:
        """
        return self.get_argument(name)

