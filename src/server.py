
import sys


from tornado.web import Application
from tornado.ioloop import IOLoop

from src.handles import HtmlHandler

from quamash import QEventLoop
from PyQt5.Qt import QApplication
from asyncio import set_event_loop


ROUTER = [
    (r'/render.html', HtmlHandler)
]


def main():
    QT_app = QApplication(sys.argv)
    asyncio_loop = QEventLoop(QT_app)
    asyncio_loop.set_debug(enabled=True)
    set_event_loop(asyncio_loop)
    app = Application(ROUTER)
    app.settings['debug'] = True
    app.listen(8015)
    loop = IOLoop.current()
    loop.start()


if __name__ == '__main__':
    main()
