
import sys
import asyncio
from asyncio import Future, set_event_loop

from sanic import Sanic, response
from PyQt5.Qt import QApplication

from src.sender import EngineSender, PageSender
from quamash import QEventLoop
from page import BasePage

QT_app = QApplication(sys.argv)

asyncio_loop = QEventLoop(QT_app)
set_event_loop(asyncio_loop)

app = Sanic()
# app.config.KEEP_ALIVE = False

engine_sender = EngineSender()

ENGINE = 'QT'


def get_async_html(url, engine):
    if engine == 'QT':
        future = Future()
        engine_sender.send(url, future)
        return future
    else:
        return BasePage(url).page()


@app.route('/render.html', methods=['GET', 'POST'])
async def index(request):
    url = request.json.get('url')
    # html = await BasePage(url).page()
    html = await get_async_html(url, ENGINE)
    return response.text(html)


if __name__ == '__main__':
    server = app.create_server(host='0.0.0.0', port=8015)
    task = asyncio.ensure_future(server)
    asyncio_loop.run_forever()