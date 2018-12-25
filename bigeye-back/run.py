from domain.base import MultipleWsListener
from domain.ws.vkontakte import VkListener
import asyncio
from aiohttp import web
from aiohttp.web import Response
from aiohttp_sse import sse_response


async def hello(request):
    loop = request.app.loop
    l = VkListener(token="5ac516e15ac516e15ac516e1015aa3d1e455ac55ac516e1011237fda012082912d0f0c5")
    listener = MultipleWsListener(l)
    await listener.connect()
    async with sse_response(request) as resp:
        # resp.send
        await listener.recv(resp.send)
        await asyncio.sleep(100000)
    return resp


async def index(request):
    d = """
        <html>
        <body>
            <script>
                var evtSource = new EventSource("/hello");
                evtSource.onmessage = function(e) {
                    const div = document.getElementById('response')
                    var para = document.createElement("p");
                    para.innerHTML = e.data;
                    div.appendChild(para);
                }
            </script>
            <div id="response"></div>
        </body>
    </html>
    """
    return Response(text=d, content_type='text/html')


app = web.Application()
app.router.add_route('GET', '/hello', hello)
app.router.add_route('GET', '/', index)
web.run_app(app, host='127.0.0.1', port=8080)
