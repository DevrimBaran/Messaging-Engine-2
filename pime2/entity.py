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

    def has_skill(self, skill_name: str) -> bool:
        """
        Check if a Node can execute a single string.
        :param skill_name:
        :return:
        """
        # TODO implement
        return True


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
    args: str = ""

    def is_input(self) -> bool:
        """utility"""
        return self.input is not None and self.process is None and self.output is None

    def is_process(self) -> bool:
        """utility"""
        return self.input is None and self.process is not None and self.output is None

    def is_output(self) -> bool:
        """utility"""
        return self.input is None and self.process is None and self.output is not None


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
    This class represents a flow message entity.
    """
    id: str
    flow_name: str
    flow_id: str
    src_created_at: datetime.datetime
    sent_at: datetime.datetime
    last_operation: str
    payload: str
    original_payload: str
    history: List['FlowMessageEntity']
