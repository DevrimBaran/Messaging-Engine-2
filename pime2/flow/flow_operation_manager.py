from typing import List

from pime2.entity import FlowEntity
from pime2.node import NodeEntity


class FlowOperationManager:

    def detect_next_step(self, flow: FlowEntity) -> (str, List[NodeEntity]):
        pass

    def detect_second_step(self, flow: FlowEntity) -> (str, List[NodeEntity]):
        pass

    def detect_nodes_of_step(self, flow: FlowEntity) -> List[NodeEntity]:
        pass
