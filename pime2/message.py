from dataclasses import dataclass

from abc import ABC
from enum import Enum

from pime2.model.node import NodeEntity
from pime2.sensor.sensor import SensorType


class MessageType(Enum):
    """
    Internal message have one of the following types
    """
    SENSOR_RESULT = "SENSOR_RESULT"
    NODE_CREATE = "NODE_CREATE"


@dataclass
class InternalMessage(ABC):
    """
    Internal abstract class for messages exchanged via the internal queue

    """
    message_type: MessageType
    message_content: dict


@dataclass
class SensorResultMessage(InternalMessage):
    """
    class to represent a single sensor result on the internal queue
    """
    sensor_type: SensorType

    def __init__(self, sensor_type: SensorType, message_content: dict):
        super().__init__(MessageType.SENSOR_RESULT.value, message_content)
        self.sensor_type = sensor_type


@dataclass
class NodeCreateResultMessage(InternalMessage):
    """
    class to represent a node create event - if one node is received via the endpoint
    """

    def __init__(self, node: NodeEntity):
        super().__init__(MessageType.NODE_CREATE.value, node.__dict__)
