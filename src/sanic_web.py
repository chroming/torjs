
import sys
from asyncio import Future, set_event_loop

from sanic import Sanic, response
from PyQt5.Qt import QApplication

from src.web.sender import BaseSender, EngineSender
from quamash import QEventLoop

QT_app = QApplication(sys.argv)

asyncio_loop = QEventLoop(QT_app)
set_event_loop(asyncio_loop)

app = Sanic()

sender = BaseSender()
engine_sender = EngineSender()


@app.route('/render.html', methods=['GET', 'POST'])
async def index(request):
    url = request.json.get('url')
    future = Future()
    # page = await sender.send(url)
    # html = await page.content()
    # await page.close()
    # return response.text(html)
    engine_sender.send(url, future)
    html = await future
    return response.text(html)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8015)