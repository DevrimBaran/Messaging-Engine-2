# pylint: disable=invalid-name
from dataclasses import dataclass


@dataclass
class NodeEntity:
    """
    class to represent a node, a "neighbor"
    """
    id: int
    name: str
    ip: str
    port: int
