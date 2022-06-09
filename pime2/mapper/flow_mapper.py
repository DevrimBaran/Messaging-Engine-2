import datetime
import json
import logging
from typing import List
from dacite import from_dict
from pime2.entity import FlowEntity, FlowMessageEntity, FlowOperationEntity
from pime2.flow.flow_message_builder import FlowMessageBuilder



class FlowMapper:
    """
    Message to map objects around flows
    """

    def flow_entity_to_json(self, flow: FlowEntity) -> str:
        """
        Method which converts a flow entity to a json string
        :param flow:
        :return:
        """
        seriazable_flow_dict = flow.__dict__
        flow_operations_array = seriazable_flow_dict['ops']
        seriazable_flow_operation_array = []
        for flow_op in flow_operations_array:
            seriazable_flow_operation_array.append(flow_op.__dict__)
        seriazable_flow_dict['ops'] = seriazable_flow_operation_array
        return json.dumps(seriazable_flow_dict)

    def json_to_flow_entity(self, json_str: str) -> FlowEntity:
        """
        Method which converts a json string to a flow entity
        :param json_str:
        :return:
        """
        json_obj = json.loads(json_str)
        flow_name = json_obj['name']
        json_flow_ops_array = json_obj['ops']
        flow_ops_list = self.json_to_flow_operation(json.dumps(json_flow_ops_array))
        flow = FlowEntity(flow_name, flow_ops_list)
        return flow

    def json_to_flow_operation(self, json_str: str):
        """
        Method which converts a json string to a flow operation entity
        :param json_str:
        :return:
        """
        json_obj = json.loads(json_str)
        result = []
        if len(json_obj) == 1 and isinstance(json_obj, list):
            result.append(from_dict(data_class=FlowOperationEntity, data=json_obj[0]))
        elif len(json_obj) > 1 and isinstance(json_obj, list):
            for obj in json_obj:
                result.append(from_dict(data_class=FlowOperationEntity, data=obj))
        elif isinstance(json_obj, dict):
            result = from_dict(data_class=FlowOperationEntity, data=json_obj)
        return result

    def flow_operation_to_json(self, flow_ops) -> str:
        """
        Method which converts a flow operation entity to a json string
        :param flow_ops:
        :return:
        """
        result = []
        if isinstance(flow_ops, FlowOperationEntity):
            result = json.dumps(flow_ops.__dict__)
        elif isinstance(flow_ops, List):
            for flow_op in flow_ops:
                result.append(flow_op.__dict__)
            result = json.dumps(result)
        return result

    def flow_entity_list_to_json(self, flow_list: List[FlowEntity]) -> str:
        """
        Method which converts a list of flow entities to a json string
        :param flow_list:
        :return:
        """
        result = []
        for flows in flow_list:
            result.append(json.loads(self.flow_entity_to_json(flows)))
        flow_list_json = json.dumps(result)
        logging.info("Entity list to json : <%s>", flow_list_json)
        return flow_list_json

    def json_to_message_entity(self, flow: dict) -> FlowMessageEntity:
        """
        The input node dict needs to be a valid flow message entity

        :param flow:
        :return:
        """
        return FlowMessageBuilder().from_valid_dict(flow)
