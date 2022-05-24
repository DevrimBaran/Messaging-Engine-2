# pylint: disable=invalid-name
from dataclasses import dataclass


@dataclass
class NodeEntity:
    """
    class to represent a node, a "neighbor"
    """
    name: str
    ip: str
    port: int
