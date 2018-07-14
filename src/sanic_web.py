
import sys
import asyncio
from asyncio import Future, set_event_loop

from sanic import Sanic, response
from PyQt5.Qt import QApplication

from src.sender import EngineSender
from quamash import QEventLoop

QT_app = QApplication(sys.argv)

asyncio_loop = QEventLoop(QT_app)
set_event_loop(asyncio_loop)

app = Sanic()

engine_sender = EngineSender()


@app.route('/render.html', methods=['GET', 'POST'])
async def index(request):
    url = request.json.get('url')
    future = Future()
    engine_sender.send(url, future)
    html = await future
    return response.text(html)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8015)
    server = app.create_server(host='0.0.0.0', port=8015)
    task = asyncio.ensure_future(server)
    asyncio_loop.run_forever()