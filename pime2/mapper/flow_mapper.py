import datetime

from pime2.entity import FlowMessageEntity


class FlowMapper:
    """
    Message to map objects around flows
    """

    def json_to_message_entity(self, node: dict) -> FlowMessageEntity:
        """
        The input node dict needs to be a valid flow message entity

        :param node:
        :return:
        """
        return FlowMessageEntity(str(node["id"]).strip(), str(node["flow_name"]).strip(),
                                 str(node["flow_id"]).strip(),
                                 datetime.datetime.fromisoformat(node["src_created_at"]),
                                 datetime.datetime.fromisoformat(node["sent_at"]),
                                 str(node["last_operation"]).strip(),
                                 str(node["payload"]).strip(), str(node["original_payload"]).strip(),
                                 int(node["count"]),
                                 node["history"] if "history" in node else [])
