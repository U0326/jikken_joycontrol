import argparse
import asyncio

from joycontrol.memory import FlashMemory
from joycontrol.controller import Controller
from joycontrol import utils
from joycontrol.protocol import controller_protocol_factory
from joycontrol.server import create_hid_server

async def start(args):
    spi_flash = FlashMemory()
    controller = Controller.from_arg('PRO_CONTROLLER')

    with utils.get_output(path=None, default=None) as capture_file:
        factory = controller_protocol_factory(controller, spi_flash=spi_flash)
        ctl_psm, itr_psm = 17, 19
        transport, protocol = await create_hid_server(factory, reconnect_bt_addr=args.reconnect_bt_addr,
                                                      ctl_psm=ctl_psm,
                                                      itr_psm=itr_psm, capture_file=capture_file,
                                                      device_id=args.device_id)

        controller_state = protocol.get_controller_state()
        controller_state.connect()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--plugin-options', nargs='*', help='joycontrol plugin options')
    parser.add_argument('-d', '--device_id')
    parser.add_argument('-r', '--reconnect_bt_addr', type=str, default=None,
                        help='The Switch console Bluetooth address, for reconnecting as an already paired controller')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(args))
