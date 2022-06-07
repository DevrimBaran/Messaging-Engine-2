from dataclasses import dataclass

from abc import ABC
from enum import Enum

from pime2.entity import NodeEntity, FlowMessageEntity
from pime2.sensor.sensor import SensorType


class MessageType(Enum):
    """
    Internal message have one of the following types
    """
    SENSOR_RESULT = "SENSOR_RESULT"
    NODE_CREATE = "NODE_CREATE"
    FLOW_MESSAGE = "FLOW_MESSAGE"


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


@dataclass
class FlowMessageResultMessage(InternalMessage):
    """
    class to represent an incoming flow_message on the internal queue

    """

    def __init__(self, node: FlowMessageEntity):
        super().__init__(MessageType.FLOW_MESSAGE.value, node.__dict__)
