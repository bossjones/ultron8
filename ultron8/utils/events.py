import asyncio


# SOURCE: aioredis
class CloseEvent:
    def __init__(self, on_close, loop=None):
        self._close_init = asyncio.Event(loop=loop)
        self._close_done = asyncio.Event(loop=loop)
        self._on_close = on_close
        self._loop = loop

    async def wait(self):
        await self._close_init.wait()
        await self._close_done.wait()

    def is_set(self):
        return self._close_done.is_set() or self._close_init.is_set()

    def set(self):
        if self._close_init.is_set():
            return

        task = asyncio.ensure_future(self._on_close(), loop=self._loop)
        task.add_done_callback(self._cleanup)
        self._close_init.set()

    def _cleanup(self, task):
        self._on_close = None
        self._close_done.set()
