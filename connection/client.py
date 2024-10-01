from enum import Enum
import time

import pymodbus.client as ModbusClient
from pymodbus import (
    FramerType,
    pymodbus_apply_logging_config,
)

from core.config import logging_level


pymodbus_apply_logging_config(logging_level)


class ClientType(Enum):
    TCP = "Tcp"
    UDP = "Udp"
    RTU = "Serial"


class FunctionCodes(Enum):

    READ_COILS = 1
    READ_DISCRETE_INPUTS = 2
    READ_HOLDING_REGISTERS = 3
    READ_INPUT_REGISTERS = 4

    WRITE_SINGLE_COIL = 5
    WRITE_SINGLE_REGISTER = 6

    WRITE_MULTIPLE_COILS = 15
    WRITE_MULTIPLE_REGISTERS = 16


class PollRange:

    def __init__(
        self,
        function_code: int,
        address: int,
        count: int,
        poll_interval: int,
    ):
        self.function_code = function_code
        self.address = address
        self.count = count
        self.poll_interval = poll_interval
        self._next_poll = time.time() + poll_interval

    def should_poll(self):
        return time.time() >= self._next_poll

    def poll(self, data):
        self._next_poll = time.time() + self.poll_interval
        self._data = data


class Client:

    def __init__(
        self,
        type: ClientType,
        host: str,
        port: int,
        timeout=10,
        retries=3,
        framer=FramerType.SOCKET,
    ):
        kwargs = {
            "host": host,
            "port": port,
            "timeout": timeout,
            "retries": retries,
            "framer": framer,
        }
        if type == ClientType.RTU:
            kwargs["port"] = str(port)

        self.client = getattr(ModbusClient, f"AsyncModbus{type.value}Client")(**kwargs)

        self.poll_ranges = []

    def add_poll_range(self, function_code, address, count, poll_interval):
        self.poll_ranges.append(PollRange(function_code, address, count, poll_interval))
