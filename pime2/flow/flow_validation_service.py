from typing import List

from pime2.entity import FlowEntity


class FlowValidationService:

    def is_flow_valid(self, flow: FlowEntity) -> (bool, List[str]):
        return True
