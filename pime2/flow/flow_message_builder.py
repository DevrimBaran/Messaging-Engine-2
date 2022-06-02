import base64
import json
import uuid
from datetime import datetime

from pime2.entity import FlowMessageEntity, FlowEntity


class FlowMessageBuilder:
    """
    A helper class to create FlowMessage instances
    """

    def build_start_message(self, flow: FlowEntity, last_operation: str, next_operation: str,
                            sensor_result: dict) -> FlowMessageEntity:
        """Build first message of a flow"""
        started_at = datetime.now()
        return FlowMessageEntity(uuid.uuid4().hex, flow.name, started_at, started_at, last_operation, next_operation,
                                 self.base64_encode(json.dumps(sensor_result)), 1, [])

    def base64_encode(self, raw_text: str) -> str:
        """base64 utility"""
        return str(base64.b64encode(raw_text.encode("ascii")))

    def base64_decode(self, raw_text: str) -> str:
        """base64 utility"""
        return str(base64.b64decode(raw_text.encode("ascii")))

    def build_next_message(self, flow: FlowEntity, flow_message: FlowMessageEntity, result: dict, last_operation: str,
                           next_operation: str):
        """Build next message of a flow"""
        old_history = list(flow_message.history)
        old_history.append(flow_message)

        return FlowMessageEntity(uuid.uuid4().hex, flow.name, flow_message.src_created_at, datetime.now(),
                                 last_operation, next_operation,
                                 self.base64_encode(json.dumps(result)), 1, old_history)

    def build_redirection_message(self, flow_message: FlowMessageEntity):
        """Build a redirection/copy message and append current flow message"""
        old_history = list(flow_message.history)
        old_history.append(flow_message)

        return FlowMessageEntity(uuid.uuid4().hex, flow_message.flow_name, flow_message.src_created_at, datetime.now(),
                                 flow_message.last_operation, flow_message.next_operation,
                                 flow_message.payload, 1, old_history)
