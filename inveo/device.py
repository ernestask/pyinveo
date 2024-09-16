from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from functools import partial
import struct
import time

import hid

from . import buzzer
from . import model
from . import led
from . import usb

_READ_OFFSET = 4
_READ_SIZE = 32

VENDOR_ID = 0x04D8
PRODUCT_ID = 0xFC27

class Command(int, Enum):
    READ = 0,
    WRITE = 1,

@dataclass(frozen=True)
class Report:
    report: int = field(default=0, init=False)
    cmd: Command
    address: bytearray
    arg: bytes | None = None

    def serialize(self) -> bytes:
        buf = bytearray(struct.pack('>BBH', self.report, self.cmd, self.address))

        if self.arg is not None:
            buf.extend(self.arg)

        return buf

class Device:
    def __init__(self, dev: hid.device):
        self._dev = dev

    def _send_report(self, report: Report) -> list[int]:
        self._dev.write(report.serialize())

        res = self._dev.read(_READ_SIZE)
        if res[0] != 2 and res[31] != 85:
            pass

        return res[_READ_OFFSET:]

    @classmethod
    @contextmanager
    def open(cls):
        dev = hid.device()

        dev.open(VENDOR_ID, PRODUCT_ID)

        try:
            yield cls(dev)
        finally:
            dev.close()

    @property
    def mode(self) -> int:
        report = Report(Command.READ, 0x0, b'\x01')
        res = self._send_report(report)

        return res[0]

    @property
    def usb_mode(self) -> usb.Mode:
        report = Report(Command.READ, led.ADDRESS_1, b'\x01')
        res = self._send_report(report)

        return usb.Mode(res[0])

    @usb_mode.setter
    def usb_mode(self, mode: usb.Mode):
        report = Report(Command.WRITE, usb.ADDRESS, struct.pack('>BB', 1, mode))

        self._send_report(report)

    @property
    def led1_mode(self) -> led.Mode:
        report = Report(Command.READ, led.ADDRESS_1, b'\x01')
        res = self._send_report(report)

        return led.Mode(res[0])

    @led1_mode.setter
    def led1_mode(self, mode: led.Mode):
        report = Report(Command.WRITE, led.ADDRESS_1, struct.pack('>BB', 1, mode))

        self._send_report(report)

    @property
    def led2_mode(self) -> led.Mode:
        report = Report(Command.READ, led.ADDRESS_2, b'\x01')
        res = self._send_report(report)

        return led.Mode(res[0])

    @led2_mode.setter
    def led2_mode(self, mode: led.Mode):
        report = Report(Command.WRITE, led.ADDRESS_2, struct.pack('>BB', 1, mode))

        self._send_report(report)

    @property
    def led3_mode(self) -> led.Mode:
        report = Report(Command.READ, led.ADDRESS_3, b'\x01')
        res = self._send_report(report)

        return led.Mode(res[0])

    @led3_mode.setter
    def led3_mode(self, mode: led.Mode):
        report = Report(Command.WRITE, led.ADDRESS_3, struct.pack('>BB', 1, mode))

        self._send_report(report)

    @property
    def read_delay(self) -> float:
        report = Report(Command.READ, 0x6, b'\x01')
        res = self._send_report(report)

        return res[0] * 0.1

    @read_delay.setter
    def read_delay(self, multiplier: int):
        report = Report(Command.WRITE, 0x6, struct.pack('>BB', 1, multiplier))

        self._send_report(report)

    @property
    def buzzer_mode(self) -> buzzer.Mode:
        report = Report(Command.READ, buzzer.ADDRESS, b'\x01')
        res = self._send_report(report)

        return buzzer.Mode(res[0])

    @buzzer_mode.setter
    def buzzer_mode(self, mode: buzzer.Mode):
        report = Report(Command.WRITE, buzzer.ADDRESS, struct.pack('>BB', 1, mode))

        self._send_report(report)

    @property
    def model(self) -> model.Model:
        report = Report(Command.READ, model.ADDRESS, b'\x02')
        res = self._send_report(report)

        return model.Model(res[0] << 8 | res[1])

    @property
    def software_version(self) -> str:
        report = Report(Command.READ, 0x101, b'\x02')
        res = self._send_report(report)

        return '.'.join(map(str, res[0:2]))

    @property
    def hardware_version(self) -> str:
        report = Report(Command.READ, 0x102, b'\x02')
        res = self._send_report(report)

        return '.'.join(map(str, res[0:2]))

    @property
    def last_tag(self) -> str:
        report = Report(Command.READ, 0x10B, b'\x12')
        res = self._send_report(report)
        uid_len = res[16]

        return '-'.join(map(lambda b: '{:02x}'.format(b), res[0:uid_len]))

    def beep(self):
        report = Report(Command.WRITE, 0xFE00)

        self._send_report(report)

    def reset(self):
        report = Report(Command.WRITE, 0xFE01)

        self._dev.write(report.serialize())
