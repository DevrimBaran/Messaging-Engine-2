import asyncio
import datetime
import json
import logging
from typing import List, Optional

import aiocoap

from pime2 import MESSAGE_SENDING_REMOTE_TIMEOUT
from pime2.coap_client import send_message
from pime2.common import base64_decode
from pime2.database import get_db_connection
from pime2.flow.flow_message_builder import FlowMessageBuilder
from pime2.flow.flow_operation_manager import FlowOperationManager
from pime2.flow.flow_validation import is_flow_valid, is_flow_step_executable
from pime2.entity import FlowEntity, FlowOperationEntity, FlowMessageEntity, NodeEntity
from pime2.repository.execution_repository import ExecutionRepository
from pime2.sensor.sensor import SensorType
from pime2.service.node_service import NodeService


class FlowManager:
    """
    This class encapsulates logic around processing and handling flows.
    Flow step operations are executed by FlowOperationManager.
    """

    def __init__(self, node_service: NodeService):
        self.node_service = node_service
        self.execution_repository = ExecutionRepository(get_db_connection())

    def get_nodes(self) -> List[NodeEntity]:
        """
        This method provides a list of currently known nodes.

        :return:
        """
        return self.node_service.get_all_nodes()

    def get_flows(self) -> List[FlowEntity]:
        """
        This methods provides a list of currently known nodes.
        FIXME: This method will be replaced with a db access in a later step. (ME-46)

        :return:
        """
        flows = FlowEntity("raspi_flow1_", [
            FlowOperationEntity(name="sensor_read", input="sensor_temperature", where="*"),
            FlowOperationEntity(name="beep_call", output="actuator_speaker", where="*")
        ])
        return [flows]

    async def start_flow(self, flow: FlowEntity, result: dict):
        """
        Method to initiate a flow start

        :param flow:
        :param result:
        :return:
        """
        neighbors = self.get_nodes()

        # validate
        is_valid = await self.validate_flow(flow, None)
        if not is_valid:
            return

        # detect first step
        first_step = flow.ops[0].name if len(flow.ops) >= 1 else None
        if first_step is None:
            logging.error("Problem: Cannot find first step in given flow. %s", flow)
            return

        # detect next step
        step_name = FlowOperationManager.detect_second_step(flow)
        if step_name is None:
            logging.error("Could not detect second step of flow: %s", flow.name)
            return
        # detect nodes of next step and send new flow message
        nodes = FlowOperationManager.detect_nodes_of_step(flow, step_name, neighbors)

        if nodes is None or len(nodes) == 0:
            logging.error("No nodes can be found for the next flow operation '%s'. Cancelling flow.", step_name)
            return

        # build flow message
        msg = FlowMessageBuilder.build_start_message(flow, first_step, result)

        logging.info("START FLOW: %s:%s", msg.flow_name, msg.flow_id)

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
        is_valid = await self.validate_flow(flow)
        if not is_valid:
            return

        # detect current step and execute
        current_step = FlowOperationManager.detect_current_step(flow, flow_message)
        if current_step is None:
            logging.error("Problem detecting current step of flow '%s'", flow.name)
            return
        if FlowOperationManager.is_last_step(flow, current_step):
            return await self.finish_flow(flow, flow_message)

        is_done, result = await self.execute_step(flow, flow_message, current_step, neighbors)
        if not is_done:
            logging.info("Flow is not executed locally.")
            return

        if result is None:
            self.cancel_flow(flow, flow_message, "CEP invalid!")
            return

        # detect next step and delegate
        next_step = FlowOperationManager.detect_next_step(flow, current_step)
        if next_step is None:
            logging.error("Could not detect next step of flow: %s", flow.name)
            return
        # detect nodes of next step and send new flow message
        nodes = FlowOperationManager.detect_nodes_of_step(flow, next_step, neighbors)
        if nodes is None or len(nodes) == 0:
            logging.error("No nodes can be found for the next flow operation '%s'. Cancelling flow.", next_step)
            return

        # build flow message
        next_msg = FlowMessageBuilder.build_next_message(flow, flow_message,
                                                         result if result is not None else "",
                                                         current_step)

        await self.send_message_to_nodes(flow, next_msg, nodes)

    async def validate_flow(self, flow: FlowEntity, flow_message: Optional[FlowMessageEntity] = None):
        """
        If this method returns False, the execution of this flow (message) can be stopped

        :param flow_message:
        :param flow:
        :return:
        """
        is_valid, validation_msgs = is_flow_valid(flow)
        if not is_valid:
            logging.warning("INVALID FLOW '%s': %s", flow.name, validation_msgs)
            self.cancel_flow(flow, flow_message)
            return False

        return True

    async def finish_flow(self, flow: FlowEntity, flow_message: FlowMessageEntity):
        """
        Method to execute the last operation of a flow

        :param flow:
        :param flow_message:
        :return:
        """
        # validate
        is_valid = await self.validate_flow(flow)
        if not is_valid:
            return

        # detect current step and execute
        final_step = FlowOperationManager.detect_current_step(flow, flow_message)
        if final_step is None:
            logging.error("Problem detecting current step of flow '%s'", flow.name)
            return
        # check if this is really the last step
        if not FlowOperationManager.is_last_step(flow, final_step):
            self.cancel_flow(flow, flow_message, "step is not final")
            return

        # check if the flow is executable
        if not is_flow_step_executable(flow, final_step, self.node_service):
            logging.warning("CANNOT EXECUTE FLOW '%s'. Neighbors or skills are missing in final step '%s'.",
                            flow.name, final_step)
            self.cancel_flow(flow, flow_message)
            return False

        result = None
        if final_step == "exit":
            pass
        else:
            result = await FlowOperationManager.execute_operation(flow, flow_message, final_step,
                                                                  self.execution_repository)
        logging.info("FINISHED FLOW %s:%s, result: %s", flow.name, flow_message.flow_id,
                     base64_decode(result) if result is not None else "")

    async def send_flow_message(self, flow_message: FlowMessageEntity, node: NodeEntity):
        """
        Method to send a flow message to another ME2 instance.

        :param flow_message:
        :param node:
        :return:
        """
        logging.info("Send FlowMessage to %s:%s", node.ip, node.port)

        def default_encoder(obj):
            if isinstance(obj, FlowMessageEntity):
                tl_msg = obj.__dict__
                history_list = []
                for history_msg in obj.history:
                    history_list.append(history_msg)

                tl_msg["history"] = history_list
                return tl_msg
            if isinstance(obj, datetime.datetime):
                return str(obj)
            return json.JSONEncoder().default(obj)

        current_payload = json.dumps(flow_message.__dict__, default=default_encoder)
        logging.debug("Flow-Message payload to send: %s", current_payload)
        success = await send_message(f"{node.ip}:{node.port}", "flow-messages",
                                     current_payload, aiocoap.Code.PUT)

        if not success:
            logging.error("PROBLEM Sending FlowMessage to %s:%s/flow-messages", node.ip, node.port)
        else:
            logging.info("SUCCESS Sending FlowMessage to %s:%s/flow-messages", node.ip, node.port)

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

    async def execute_step(self, flow: FlowEntity, flow_message: FlowMessageEntity, step: str,
                           nodes: List[NodeEntity]) -> (bool, Optional[str]):
        """
        Helper method to execute a single step (= flow operation) locally and remote.
        If the execution was also locally, the first return value is true, else false.
        Remote executions do not have a result.

        :param flow:
        :param flow_message:
        :param step:
        :param nodes:
        :return:
        """
        nodes_of_step = FlowOperationManager.detect_nodes_of_step(flow, step, nodes)

        message = FlowMessageBuilder.build_redirection_message(flow_message)
        await self.send_message_to_nodes(flow, message, nodes_of_step, False)

        is_executed_locally = len(list(filter(lambda x: not self.node_service.is_node_remote(x), nodes_of_step))) > 0
        if is_executed_locally:
            # check if the flow is executable
            if not is_flow_step_executable(flow, step, self.node_service):
                logging.warning("CANNOT EXECUTE FLOW '%s'. Neighbors or skills are missing in step '%s'.",
                                flow.name, step)
                self.cancel_flow(flow, flow_message)
                return False, None

            result = await FlowOperationManager.execute_operation(flow, flow_message, step, self.execution_repository)
            return True, result
        return False, None

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
        await asyncio.wait(node_tasks, return_when=asyncio.ALL_COMPLETED, timeout=MESSAGE_SENDING_REMOTE_TIMEOUT)

    def cancel_flow(self, flow: FlowEntity, flow_message: Optional[FlowMessageEntity] = None, additional_msg: str = ""):
        """
        Method to cancel a flow
        :param additional_msg:
        :param flow:
        :param flow_message:
        :return:
        """
        logging.info("Cancelled flow %s with message %s. %s", flow, flow_message, additional_msg)
