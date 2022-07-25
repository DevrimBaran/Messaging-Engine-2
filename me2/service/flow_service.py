from json import JSONDecodeError
from typing import List
from me2.database import get_db_connection
from me2.entity import FlowEntity
from me2.repository.flow_repository import FlowRepository
from me2.mapper.flow_mapper import FlowMapper



class FlowService:
    """Implements flow service class"""

    def __init__(self):
        """Initialize FlowRepository and FlowMapper"""
        self.flow_repository = FlowRepository(get_db_connection())
        self.flow_mapper = FlowMapper()

    def put_flow(self, flow):
        """Save a flow in the database"""
        if isinstance(flow, FlowEntity):
            self.flow_repository.create_flow(flow)
        elif isinstance(flow, str):
            flow = self.flow_mapper.json_to_flow_entity(flow)
            self.flow_repository.create_flow(flow)
        else:
            raise TypeError("Bad Input")

    def remove_flow(self, flow) -> bool:
        """Removes a flow from the database"""
        if isinstance(flow, FlowEntity):
            self.flow_repository.delete_flow_by_name(flow.name)
            return True
        if isinstance(flow, str):
            try:
                flow = self.flow_mapper.json_to_flow_entity(flow)
                self.flow_repository.delete_flow_by_name(flow.name)
                return True
            except JSONDecodeError:
                return False
        return False

    def get_all_flows(self) -> List[FlowEntity]:
        """
        Method to return all flows of this me2 instance
        :return:
        """
        flow_list = self.flow_repository.read_all_flows()
        return flow_list

    def get_all_flows_as_json(self) -> str:
        """Get all flows as a json string"""
        flow_list = self.flow_repository.read_all_flows()
        flows_json_string = self.flow_mapper.flow_entity_list_to_json(flow_list)
        return flows_json_string

    def delete_all_flows(self):
        """Deletes all flows from the database"""
        self.flow_repository.delete_all()
