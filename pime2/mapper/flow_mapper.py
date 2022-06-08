from pime2.entity import FlowMessageEntity
from pime2.flow.flow_message_builder import FlowMessageBuilder


class FlowMapper:
    """
    Message to map objects around flows
    """

    def json_to_message_entity(self, flow: dict) -> FlowMessageEntity:
        """
        The input node dict needs to be a valid flow message entity

        :param flow:
        :return:
        """
        return FlowMessageBuilder().from_valid_dict(flow)
