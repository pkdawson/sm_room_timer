import websockets
import asyncio
import json

class WebsocketClient(object):
  def __init__(self, name, addr='127.0.0.1', port='23074'):
    self.connect(name, addr, port)

  async def connect_async(self, name, addr, port):
    uri = 'ws://%s:%s' % (addr, port)
    self.ws = await websockets.connect(uri)
    await self.send_async("Name", name)
    devices = (await self.request_async("DeviceList"))['Results']
    await self.send_async("Attach", devices[0])
    info = await self.request_async("Info")

  def connect(self, name, addr, port):
    asyncio.get_event_loop().run_until_complete(self.connect_async(name, addr, port))

  async def send_async(self, op, *args):
    # TODO: flags?
    req = {
      "Opcode": op,
      "Space": "SNES",
      "Operands": args
    }
    await self.ws.send(json.dumps(req))

  async def request_async(self, op, *args):
    await self.send_async(op, *args)
    res = await self.ws.recv()
    return json.loads(res)

  async def read_core_ram_async(self, addr, size):
    full_addr = 0xF50000 + addr
    await self.send_async('GetAddress', '%X' % (full_addr), '%X' % size)
    res = await self.ws.recv()
    return [ c for c in res ]

  def read_core_ram(self, addr, size):
    return asyncio.get_event_loop().run_until_complete(self.read_core_ram_async(addr, size))
