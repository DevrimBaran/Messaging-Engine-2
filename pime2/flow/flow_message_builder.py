import copy
import json
import uuid
from datetime import datetime

from pime2.common import base64_encode
from pime2.entity import FlowMessageEntity, FlowEntity


class FlowMessageBuilder:
    """
    A helper class to create FlowMessage instances
    """

    def build_start_message(self, flow: FlowEntity, last_operation: str, next_operation: str,
                            sensor_result: dict) -> FlowMessageEntity:
        """Build first message of a flow"""
        started_at = datetime.now()
        payload = base64_encode(json.dumps(sensor_result))
        return FlowMessageEntity(uuid.uuid4().hex, flow.name, uuid.uuid4().hex, started_at, started_at, last_operation,
                                 next_operation, payload, payload, 1, [])

    def build_next_message(self, flow: FlowEntity, flow_message: FlowMessageEntity, result: str, last_operation: str,
                           next_operation: str):
        """Build next message of a flow"""
        old_history = list(flow_message.history)
        hist_msg = copy.copy(flow_message)
        hist_msg.history = []
        old_history.append(hist_msg)

        return FlowMessageEntity(uuid.uuid4().hex, flow.name, flow_message.flow_id, flow_message.src_created_at,
                                 datetime.now(), last_operation, next_operation, result,
                                 str(flow_message.original_payload), 1, old_history)

    def build_redirection_message(self, flow_message: FlowMessageEntity):
        """Build a redirection/copy message and append current flow message"""
        old_history = list(flow_message.history)
        old_history.append(flow_message)

        return FlowMessageEntity(uuid.uuid4().hex, flow_message.flow_name, flow_message.flow_id,
                                 flow_message.src_created_at, datetime.now(),
                                 flow_message.last_operation, flow_message.next_operation,
                                 flow_message.payload, flow_message.original_payload, 1, old_history)
