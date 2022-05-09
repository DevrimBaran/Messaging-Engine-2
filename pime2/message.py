from __future__ import annotations

from enum import Enum

from pime2.sensor.sensor import SensorType


class MessageType(Enum):
    SENSOR_RESULT = "SENSOR_RESULT"


class InternalMessage:
    def __init__(self, message_type: MessageType, message_content: dict):
        self.message_type = message_type.name
        self.message_content = message_content


class SensorResult(InternalMessage):
    def __init__(self, sensor_type: SensorType, result: dict):
        super().__init__(MessageType.SENSOR_RESULT, result)
        self.sensor_type = sensor_type
