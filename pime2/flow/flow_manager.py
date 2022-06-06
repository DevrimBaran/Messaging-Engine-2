import asyncio
import json
import logging
from typing import List

import aiocoap

from pime2.coap_client import send_message
from pime2.config import get_me_conf
from pime2.flow.flow_message_builder import FlowMessageBuilder
from pime2.flow.flow_operation_manager import FlowOperationManager
from pime2.entity import FlowEntity, FlowOperationEntity, FlowMessageEntity, NodeEntity
from pime2.flow.flow_validation_service import is_flow_valid
from pime2.sensor.sensor import SensorType
from pime2.service.node_service import NodeService


class FlowManager:
    """
    This class encapsulates logic around processing and handling flows.
    Flow step operations are executed by FlowOperationManager.
    """

    def __init__(self, flow_operation_manager: FlowOperationManager,
                 flow_message_builder: FlowMessageBuilder, node_service: NodeService):
        self.flow_operation_manager = flow_operation_manager
        self.flow_message_builder = flow_message_builder
        self.node_service = node_service
        self.startup()

    def get_nodes(self) -> List[NodeEntity]:
        """
        This methods provides a list of currently known nodes.

        :return:
        """
        return self.node_service.get_all_nodes()

    def get_flows(self) -> List[FlowEntity]:
        """
        This methods provides a list of currently known nodes.
        FIXME: This method will be replaced with a db access in a later step.

        :return:
        """
        flow = FlowEntity("test_flow1", [
            FlowOperationEntity("first_step", "sensor_temperature", None, None),
            FlowOperationEntity("second_step", None, "log", None),
            FlowOperationEntity("last_step", None, None, "exit"),
        ])
        return [flow]

    async def start_flow(self, flow: FlowEntity, result: dict):
        """
        Method to initiate a flow start

        :param flow:
        :param result:
        :return:
        """
        neighbors = self.get_nodes()

        # validate
        is_valid, validation_msgs = is_flow_valid(flow)
        if not is_valid:
            logging.error("Problem with flow '%s'", flow.name)
            for i in validation_msgs:
                logging.error("Validation message: %s", i)
            return
        # detect first step
        first_step = flow.ops[0].name if len(flow.ops) >= 1 else None
        if first_step is None:
            logging.error("Problem: Cannot find first step in given flow. %s", flow)
            return

        # detect next step
        step = self.flow_operation_manager.detect_second_step(flow)
        if step is None:
            logging.error("Could not detect second step of flow: %s", flow.name)
            return
        # detect nodes of next step and send new flow message
        nodes = self.flow_operation_manager.detect_nodes_of_step(flow, step, neighbors)

        if nodes is None or len(nodes) == 0:
            logging.error("No nodes can be found for the next flow operation. Cancelling flow.")
            return

        # build flow message
        msg = self.flow_message_builder.build_start_message(flow, first_step, step, result)
        # and send message to nodes
        await self.send_message_to_nodes(flow, msg, nodes)

    async def execute_flow(self, flow: FlowEntity, flow_message: FlowMessageEntity, neighbors: List[NodeEntity]):
        """
        This method executes a single step. If the step is the last one of the flow, finish_flow() is called.

        :param flow:
        :param flow_message:
        :param neighbors:
        :return:
        """
        # validate
        is_valid, validation_msgs = is_flow_valid(flow)
        if not is_valid:
            logging.error("Problem with flow '%s'")
            for i in validation_msgs:
                logging.error("Validation message: '%s'", i)
            return

        # detect current step and execute
        current_step = self.flow_operation_manager.detect_current_step(flow, flow_message)
        if current_step is None:
            logging.error("Problem detecting current step of flow '%s'", flow.name)
            return
        if self.flow_operation_manager.is_last_step(flow, current_step):
            return await self.finish_flow(flow, flow_message)

        is_done, result = await self.execute_step(flow, flow_message, current_step, neighbors)
        if not is_done:
            logging.info("Flow is not executed locally.")
            return

        # detect next step and delegate
        next_step = self.flow_operation_manager.detect_next_step(flow, flow_message)
        if next_step is None:
            logging.error("Could not detect next step of flow: %s", flow.name)
            return
        # detect nodes of next step and send new flow message
        nodes = self.flow_operation_manager.detect_nodes_of_step(flow, next_step, neighbors)
        if nodes is None or len(nodes) == 0:
            logging.error("No nodes can be found for the next flow operation. Cancelling flow.")
            return

        # build flow message
        next_msg = self.flow_message_builder.build_next_message(flow, flow_message, result, current_step, next_step)

        await self.send_message_to_nodes(flow, next_msg, nodes)

    async def finish_flow(self, flow: FlowEntity, flow_message: FlowMessageEntity):
        """
        Method to execute the last operation of a flow

        :param flow:
        :param flow_message:
        :return:
        """
        # validate
        is_valid, validation_msgs = is_flow_valid(flow)
        if not is_valid:
            logging.error("Problem with flow '%s'")
            for i in validation_msgs:
                logging.error("Validation message: '%s'", i)
            return

        # detect current step and execute
        final_step = self.flow_operation_manager.detect_current_step(flow, flow_message)
        if final_step is None:
            logging.error("Problem detecting current step of flow '%s'", flow.name)
            return
        # TODO: Check if this is really the last step

        self.flow_operation_manager.execute_operation(flow, flow_message, final_step)
        logging.info("Finished flow")
        return

    async def send_flow_message(self, flow_message: FlowMessageEntity, node: NodeEntity):
        """
        Method to send a flow message to another ME2 instance.

        :param flow_message:
        :param node:
        :return:
        """
        logging.info("Send FlowMessage to %s:%s", node.ip, node.port)

        await send_message(f"{node.ip}:{node.port}", "flow-message",
                           json.dumps(flow_message.__dict__, default=str), aiocoap.Code.GET)

        logging.info("Send FlowMessage finished")

    def get_available_flows_for_sensor(self, sensor_type: SensorType) -> List[FlowEntity]:
        """
        Method to check which flows are related to this sensor_read type

        :param sensor_type:
        :return:
        """
        flows = self.get_flows()
        out = []
        for f in flows:
            is_affected = False
            for operation in f.ops:
                if operation.input is not None and operation.input == ("sensor_" + str(sensor_type).lower()):
                    is_affected = True
            if is_affected:
                out.append(f)
        return out

    def startup(self):
        """
        This method is called at the end of the constructor to do prepare the flow managers work.
        :return:
        """
        node = self.node_service.get_own_node()
        if node is None:
            # Create own entry
            logging.info("FlowManager: Creating self node")
            me_conf = get_me_conf()
            self.node_service.put_node(NodeEntity(me_conf.instance_id, me_conf.host, me_conf.port))
        else:
            logging.info("FlowManager: Self node exists")

    async def execute_step(self, flow: FlowEntity, flow_message: FlowMessageEntity, step: str,
                           nodes: List[NodeEntity]) -> (bool, dict):
        """
        Helper method to execute a single step locally and remote.
        If the execution was also locally, the return value is true, else false.
        :param flow:
        :param flow_message:
        :param step:
        :param nodes:
        :return:
        """
        nodes_of_step = self.flow_operation_manager.detect_nodes_of_step(flow, step, nodes)

        message = self.flow_message_builder.build_redirection_message(flow_message)
        await self.send_message_to_nodes(flow, message, nodes_of_step, False)

        is_executed_locally = len(list(filter(lambda x: not self.node_service.is_node_remote(x), nodes_of_step))) > 0
        if is_executed_locally:
            result = self.flow_operation_manager.execute_operation(flow, flow_message, step)
            return True, result
        return False, {}

    async def send_message_to_nodes(self, flow: FlowEntity, message: FlowMessageEntity, nodes: List[NodeEntity],
                                    execute_local=True):
        """
        Method to send a single message to remote nodes.

        """
        node_tasks = []
        for neighbor in nodes:
            if self.node_service.is_node_remote(neighbor):
                node_tasks.append(asyncio.create_task(self.send_flow_message(message, neighbor)))
            else:
                if execute_local:
                    await self.execute_flow(flow, message, nodes)
        if len(node_tasks) == 0:
            return
        await asyncio.wait(node_tasks, return_when=asyncio.ALL_COMPLETED, timeout=20)
