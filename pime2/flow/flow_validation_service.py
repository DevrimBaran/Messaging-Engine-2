from typing import List

from pime2.entity import FlowEntity


class FlowValidationService:
    """
    This class validates flows and returns the result + validation messages.

    """

    def is_flow_valid(self, flow: FlowEntity) -> (bool, List[str]):
        """
        Method to check if a flow is valid.
        TODO: Not yet implemented

        :param flow:
        :return:
        """
        if len(flow.ops) == 0:
            return False, ["Got flow without operations!"]

        # TODO implement
        return True, []
