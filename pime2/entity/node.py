# pylint: disable=invalid-name
from dataclasses import dataclass

from pime2.config import get_me_conf


@dataclass
class NodeEntity:
    """
    class to represent a node, a "neighbor"
    """
    name: str
    ip: str
    port: int


class NodeManager:

    def is_node_remote(self, node: NodeEntity) -> bool:
        return node.name != get_me_conf().instance_id
