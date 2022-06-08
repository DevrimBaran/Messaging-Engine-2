import datetime
import json
import logging
from typing import List
from pime2.entity import FlowEntity, FlowMessageEntity, FlowOperationEntity
from dacite import from_dict

class FlowMapper:
    """
    Message to map objects around flows
    """

    def flow_entity_to_json(self, flow: FlowEntity) -> str:
        seriazable_flow_dict = flow.__dict__
        flow_operations_array = seriazable_flow_dict['ops']
        seriazable_flow_operation_array = []
        for flow_op in flow_operations_array:
            seriazable_flow_operation_array.append(flow_op.__dict__)
        seriazable_flow_dict['ops'] = seriazable_flow_operation_array
        return json.dumps(seriazable_flow_dict)

    def json_to_flow_entity(self, json_str: str) -> FlowEntity:
        json_obj = json.loads(json_str)
        flow_name = json_obj['name'] 
        json_flow_ops_array = json_obj['ops']
        flow_ops_list = self.json_to_flow_operation(json.dumps(json_flow_ops_array))
        flow = FlowEntity(flow_name, flow_ops_list)
        return flow

    def json_to_flow_operation(self, json_str: str) -> FlowOperationEntity | List[FlowOperationEntity]:
        json_obj = json.loads(json_str)
        result=[]
        if len(json_obj) == 1 and isinstance(json_obj, list):
            result.append(from_dict(data_class=FlowOperationEntity, data=json_obj[0]))
        elif len(json_obj) > 1 and isinstance(json_obj, list):
            for obj in json_obj:
                result.append(from_dict(data_class=FlowOperationEntity, data=obj))
        elif isinstance(json_obj, dict):
            result = from_dict(data_class=FlowOperationEntity, data=json_obj)
        
        return result

    def flow_operation_to_json(self, flow_ops: FlowOperationEntity | List[FlowOperationEntity]) -> str:
        result = []
        if isinstance(flow_ops, FlowOperationEntity):
            result = json.dumps(flow_ops)
        elif isinstance(flow_ops, List[FlowOperationEntity]):
            for flow_op in flow_ops:
                result.append(flow_op.__dict__)
            result = json.dumps(result)
        return result


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
                                 str(node["last_operation"]).strip(), str(node["next_operation"]).strip(),
                                 str(node["payload"]).strip(), str(node["original_payload"]).strip(),
                                 int(node["count"]),
                                 node["history"] if "history" in node else [])
