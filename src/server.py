
import sys

from tornado.web import Application
from tornado.ioloop import IOLoop

from src.handles import HtmlHandler

from quamash import QEventLoop
from PyQt5.Qt import QApplication
from asyncio import set_event_loop

QT_app = QApplication(sys.argv)

asyncio_loop = QEventLoop(QT_app)
set_event_loop(asyncio_loop)

ROUTER = [
    (r'/render.html', HtmlHandler)
]


if __name__ == '__main__':
    app = Application(ROUTER)
    app.settings['debug'] = True
    app.listen(8015)
    loop = IOLoop.current().start()
    loop.start()