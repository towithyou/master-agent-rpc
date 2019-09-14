import zerorpc
from aiohttp import web
from config.conf import SERVER_URL

class Web:
    def __init__(self):
        self.app = web.Application()
        self.app.add_routes([
            web.get('/', self.agents_handle),
            web.post('/add_task', self.add_task)
        ])

        self.client = zerorpc.Client()
        self.client.connect(SERVER_URL)

    async def agents_handle(self, request:web.Request):
        agents = self.client.agents()
        # await request.json(agents)
        # return web.Response(text='123')

        return web.json_response(agents)

    async def add_task(self, request:web.Request):
        j = await request.json()
        task_id = self.client.add_task(j)
        # await request.json(agents)
        # return web.Response(text='123')
        return web.json_response(task_id)

    def start(self):
        web.run_app(self.app, host='127.0.0.1', port=8888)