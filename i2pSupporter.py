import asyncio
import i2plib


def i2pServerTunnel(port, dest):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    tunnel = i2plib.ServerTunnel(("127.0.0.1", port), session_name="TroikadMainSession", destination=dest, loop=loop, options={"inbound.nickname":"Troikad", "inbound.length":2, "outbound.length":2, "inbound.lengthVariance":1, "outbound.lengthVariance":1, "inbound.quantity":3, "outbound.quantity":3})
    asyncio.ensure_future(tunnel.run())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

def i2pClientTunnel(port, dest):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    tunnel = i2plib.ClientTunnel(dest, ("127.0.0.1", port), session_name="TroikadMainSession", options={"inbound.nickname":"Troikad", "inbound.length":2, "outbound.length":2, "inbound.lengthVariance":1, "outbound.lengthVariance":1, "inbound.quantity":3, "outbound.quantity":3})
    asyncio.ensure_future(tunnel.run())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

def getFreePort():
    unusedPort = i2plib.utils.get_free_port()
    return unusedPort

def new_Destination():
    loop = asyncio.get_event_loop()
    destination = loop.run_until_complete(i2plib.new_destination())
    return destination