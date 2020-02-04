# """Example for GatewayScanner."""
# import asyncio

# from xknx import XKNX
# from xknx.io import GatewayScanner, Connect, UDPClient, ConnectionConfig, ConnectionType
# from xknx.knxip import (
#     HPAI, ConnectRequestType, ConnectResponse, ErrorCode, KNXIPFrame,
#     KNXIPServiceType)

# async def get_gateway():
#     # gatewayscanner = GatewayScanner(xknx)
        
#     # gateways = await gatewayscanner.scan()
#     """Test connecting to KNX bus via proxy."""
#     loop = asyncio.get_event_loop()
#     xknx = XKNX(loop=loop)
#     udp_client = UDPClient(
#         xknx,
#         ("172.17.0.2", 0),
#         ("10.0.1.21", 3671),
#         proxy_addr=("10.0.1.217", 3671))
#     connect = Connect(xknx, udp_client)
#     connect.timeout_in_seconds = 0


#     # Expected KNX/IP-Frame:
#     exp_knxipframe = KNXIPFrame(xknx)
#     exp_knxipframe.init(KNXIPServiceType.CONNECT_REQUEST)
#     exp_knxipframe.body.control_endpoint = HPAI(
#         ip_addr='10.0.1.217', port=3671)
#     exp_knxipframe.body.data_endpoint = HPAI(
#         ip_addr='10.0.1.217', port=3671)
#     exp_knxipframe.body.request_type = ConnectRequestType.TUNNEL_CONNECTION
#     exp_knxipframe.normalize()

#     # loop.run_until_complete(asyncio.Task(connect.start()))

# async def try_nat():
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#     loop.close()
#     xknx = XKNX(loop=loop)
#     config = ConnectionConfig(
#         connection_type=ConnectionType.TUNNELING,
#         gateway_ip="10.0.1.21",
#         gateway_port="3671",
#         local_ip="172.17.0.2",
#         proxy_ip="10.0.1.217"
#     )
#     await xknx.start(connection_config=config)
#     await xknx.loop_until_sigint()



# def main():
#     try_nat()

# pylint: disable=invalid-name
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()

# async def main():
#     """Connect to a tunnel, send 2 telegrams and disconnect."""
#     xknx = XKNX()
#     gatewayscanner = GatewayScanner(xknx)
#     gateways = await gatewayscanner.scan()

#     if not gateways:
#         print("No Gateways found")
#         return

#     gateway = gateways[0]
#     src_address = PhysicalAddress("15.15.249")

#     print("Connecting to {}:{} from {}".format(
#         gateway.ip_addr,
#         gateway.port,
#         gateway.local_ip))

#     tunnel = Tunnel(
#         xknx,
#         src_address,
#         local_ip=gateway.local_ip,
#         gateway_ip=gateway.ip_addr,
#         gateway_port=gateway.port)

#     await tunnel.connect_udp()
#     await tunnel.connect()

#     await tunnel.send_telegram(Telegram(GroupAddress('1/0/15'), payload=DPTBinary(1)))
#     await asyncio.sleep(2)
#     await tunnel.send_telegram(Telegram(GroupAddress('1/0/15'), payload=DPTBinary(0)))
#     await asyncio.sleep(2)

#     await tunnel.connectionstate()
#     await tunnel.disconnect()

# # pylint: disable=invalid-name
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()

"""Example for switching a light on and off."""
import asyncio
import logging
import os
import socket
from xknx import XKNX
from xknx.io import ConnectionConfig, ConnectionType
from xknx.devices import Light


async def main():
    """Connect to KNX/IP bus, switch on light, wait 2 seconds and switch of off again."""
    gateway_ip = "10.0.1.213"
    gateway_port = 3671
    docker_host_ip = "10.0.1.217"
    # container_ip =
    local_port = 3671
    # ga_switch = "0/"
    # ga_state = os.environ['TEST_GROUP_ADDRESS_STATE']
    ga_switch = "3/1/4"
    ga_state = "3/5/4"

    logging.basicConfig(level=logging.DEBUG)

    xknx = XKNX()
    connection_config = ConnectionConfig(
        connection_type=ConnectionType.TUNNELING,
        gateway_ip=gateway_ip,
        # gateway_port=gateway_port,
        # local_ip=container_ip,
        # local_port=local_port,
        proxy_ip=docker_host_ip)
    #connection_config = ConnectionConfig(local_port=local_port, proxy_ip=docker_host_ip)
    light = Light(xknx,
                  name='TestLight',
                  group_address_switch=ga_switch)

    await xknx.start(connection_config=connection_config)
    for x in range(2):
        await light.set_off()
        await asyncio.sleep(2)
        await light.set_on()
        await asyncio.sleep(2)
    await xknx.stop()


# pylint: disable=invalid-name
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
