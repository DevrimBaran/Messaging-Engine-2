import base64
import json
import uuid
from datetime import datetime

from pime2.entity import FlowMessageEntity, FlowEntity


class FlowMessageBuilder:
    def build_start_message(self, flow: FlowEntity, next_operation: str, sensor_result: dict) -> FlowMessageEntity:
        started_at = datetime.now()
        return FlowMessageEntity(uuid.uuid4().hex, flow.name, started_at, started_at, None, next_operation,
                                 self.base64_encode(json.dumps(sensor_result)), 1, [])

    def base64_encode(self, input: str) -> str:
        return str(base64.b64encode(input.encode("ascii")))

    def base64_decode(self, input: str) -> str:
        return str(base64.b64decode(input.encode("ascii")))

    def build_next_message(self, flow: FlowEntity, flow_message: FlowMessageEntity, result: dict, last_operation: str,
                           next_operation: str):
        old_history = list(flow_message.history)
        old_history.append(flow_message)

        return FlowMessageEntity(uuid.uuid4().hex, flow.name, flow_message.src_created_at, datetime.now(),
                                 last_operation, next_operation,
                                 self.base64_encode(json.dumps(result)), 1, old_history)

    def build_redirection_message(self, flow_message: FlowMessageEntity):
        old_history = list(flow_message.history)
        old_history.append(flow_message)

        return FlowMessageEntity(uuid.uuid4().hex, flow_message.flow_name, flow_message.src_created_at, datetime.now(),
                                 flow_message.last_operation, flow_message.next_operation,
                                 flow_message.payload, 1, old_history)
