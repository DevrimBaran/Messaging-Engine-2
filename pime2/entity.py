# pylint: disable=C0103
import datetime
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class NodeEntity:
    """
    class to represent a node, a "neighbor"
    """
    name: str
    ip: str
    port: int
    sensor_skills: List[str] = field(default_factory=lambda: [])
    actuator_skills: List[str] = field(default_factory=lambda: [])


@dataclass
class FlowOperationEntity:
    """
    This class represents a flow operation aka a flow step
    """
    name: str
    # one of "input", "process" and "output" are not blank
    input: Optional[str]
    process: Optional[str]
    output: Optional[str]
    where: str = "*"
    args: dict = {}


@dataclass
class FlowEntity:
    """
    This class represents a datastructure to store a flow which can be handled by ME2
    """
    name: str
    ops: List[FlowOperationEntity]


@dataclass
class FlowMessageEntity:
    """
    This class represents a flow message entity
    """
    id: str
    flow_name: str
    flow_id: str
    src_created_at: datetime.datetime
    sent_at: datetime.datetime
    last_operation: str
    next_operation: str
    payload: str
    original_payload: str
    count: int
    history: List['FlowMessageEntity']
