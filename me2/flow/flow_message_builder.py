import copy
import json
import uuid
from datetime import datetime

from me2.common import base64_encode
from me2.entity import FlowMessageEntity, FlowEntity


class FlowMessageBuilder:
    """
    A helper class to create FlowMessage instances
    """

    @staticmethod
    def build_start_message(flow: FlowEntity, last_operation: str, sensor_result: dict) -> FlowMessageEntity:
        """Build first message of a flow"""
        started_at = datetime.now()
        payload = base64_encode(json.dumps(sensor_result, default=str))
        return FlowMessageEntity(uuid.uuid4().hex, flow.name, uuid.uuid4().hex, started_at, started_at, last_operation,
                                 payload, payload, [])

    @staticmethod
    def build_next_message(flow: FlowEntity, flow_message: FlowMessageEntity, result: str, last_operation: str):
        """Build next message of a flow"""
        old_history = list(flow_message.history)
        hist_msg = copy.copy(flow_message)
        hist_msg.history = []
        old_history.append(hist_msg)

        return FlowMessageEntity(uuid.uuid4().hex, flow.name, flow_message.flow_id, flow_message.src_created_at,
                                 datetime.now(), last_operation, result,
                                 str(flow_message.original_payload), old_history)

    @staticmethod
    def build_redirection_message(flow_message: FlowMessageEntity):
        """Build a redirection/copy message and append current flow message"""
        old_history = list(flow_message.history)
        old_history.append(flow_message)

        return FlowMessageEntity(flow_message.id, flow_message.flow_name, flow_message.flow_id,
                                 flow_message.src_created_at, datetime.now(),
                                 flow_message.last_operation,
                                 flow_message.payload, flow_message.original_payload, old_history)

    @staticmethod
    def from_valid_dict(node: dict) -> FlowMessageEntity:
        """Build a FlowMessage from a valid dictionary (e.g. from json)"""
        return FlowMessageEntity(str(node["id"]).strip(), str(node["flow_name"]).strip(),
                                 str(node["flow_id"]).strip(),
                                 datetime.fromisoformat(node["src_created_at"]),
                                 datetime.fromisoformat(node["sent_at"]),
                                 str(node["last_operation"]).strip(),
                                 str(node["payload"]).strip(), str(node["original_payload"]).strip(),
                                 node["history"] if "history" in node else [])
