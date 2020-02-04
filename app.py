import asyncio

from aiohttp import web
from xknx import XKNX
from xknx.io import GatewayScanner
from xknx.devices import Light

xknx = XKNX()
async def handle(request):
    name = request.match_info.get("name", "Anonymous")
    text = "Hello, " + name
    # """Connect to KNX/IP bus, switch on light, wait 2 seconds and switch it off again."""
    # xknx = XKNX()
    # await xknx.start()
    # light = Light(xknx, name="TestLight", group_address_switch="0/0/1")
    # await light.set_on()
    # await asyncio.sleep(2)
    # await light.set_off()
    # await xknx.stop()
    
    gatewayscanner = GatewayScanner(xknx)
    gateways = await gatewayscanner.scan()

    if not gateways:
        print("No Gateways found")

    else:
        for gateway in gateways:
            print(
                "Gateway found: {0} / {1}:{2}".format(
                    gateway.name, gateway.ip_addr, gateway.port
                )
            )
            if gateway.supports_tunnelling:
                print("- Device supports tunneling")
            if gateway.supports_routing:
                print(
                    "- Device supports routing, connecting via {0}".format(
                        gateway.local_ip
                    )
                )

    return web.Response(text=text)


app = web.Application()
app.add_routes([web.get("/", handle), web.get("/{name}", handle)])

if __name__ == "__main__":
    web.run_app(app)
