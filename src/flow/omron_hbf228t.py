"""Defines communication flow for HB281."""

import logging
from iotble.access.gatt_tool_wrapper import GattToolWrapper
from iotble.util import read_yaml
from iotble.const import HBF228T_DEV_ADDRESS, UUID_LIST

def body_composition_monitor() -> None:
    """Runs flow for BCM

    Runs workflow for  Bluetooth standard protocol for Body Composition Monitor

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    logger_ = logging.getLogger(__name__)
    logger_.info('Start sequence flow.')

    try:
        # Read uuid list
        data = read_yaml(UUID_LIST)

        # Init Device
        gatt = GattToolWrapper()
        gatt.start()
        gatt.connect(HBF228T_DEV_ADDRESS)

        # Read characteristics for Device Information
        for key, val in data['di'].items():
            logging.info('key: {}, uuid: {}, char_val: {}',\
                key, val['uuid'], gatt.read_char_as_str(val['uuid']))

        # Read characteristics for Weight scale feature
        logger_.info('key: {}, uuid: {}, char_val: {}',\
            'ws', data['ws']['wsf']['uuid'], gatt.read_char_as_str(data['ws']['wsf']['uuid']))

        # Read characteristics for Body Composition
        logger_.info('key: {}, uuid: {}, char_val: {}',\
            'bc', data["bc"]["bcf"]["uuid"], gatt.read_char_as_str(data["bc"]["bcf"]["uuid"]))
    finally:
        gatt.stop()