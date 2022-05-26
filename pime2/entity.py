import datetime
from dataclasses import dataclass
from typing import List, Optional, Iterable


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
    src_created_at: datetime.datetime
    sent_at: datetime.datetime
    last_operation: Optional[str]
    next_operation: str
    payload: str
    count: int
    history: Iterable['FlowMessageEntity']
