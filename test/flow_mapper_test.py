import json
import unittest

from typing import List

from pime2.entity import FlowEntity, FlowOperationEntity
from pime2.mapper.flow_mapper import FlowMapper


class FlowMapperTest(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.flow_mapper = FlowMapper()

    def get_flow_list(self) -> List[FlowEntity]:
        return [
            FlowEntity("flow1",[FlowOperationEntity(name='Flow_op_one', input='Input', process='Process', output='Output', where='*', join = "join", args='Args'),FlowOperationEntity(name='Flow_op_two', input='Input', process='Process', output='Output', where='*', join = "join", args='Args'),FlowOperationEntity(name='Flow_op_three', input='Input', process='Process', output='Output', where='*', join = "join", args='Args')]),
            FlowEntity("flow2",[FlowOperationEntity(name='Flow_op_two', input='Input', process='Process', output='Output', where='*', join = "join", args='Args'),FlowOperationEntity(name='Flow_op_three', input='Input', process='Process', output='Output', where='*', join = "join", args='Args')]),
            FlowEntity("flow3",[FlowOperationEntity(name='Flow_op_one', input='Input', process='Process', output='Output', where='*', join = "join", args='Args')]),
            FlowEntity("flow4",[]),
            FlowEntity("flow5"),
            FlowEntity("flow6",[FlowOperationEntity(name='Flow_op_one', input='Input', process='Process', output='Output', where='*', join = "join", args='Args'),FlowOperationEntity(name='Flow_op_two', input='Input', process='Process', output='Output', where='*', join = "join", args='Args'),FlowOperationEntity(name='Flow_op_three', input='Input', process='Process', output='Output', where='*', join = "join", args='Args')]),
            FlowEntity("flow7",[FlowOperationEntity(name='Flow_op_one', input='Input', process='Process', output='Output', where='*', join = "join", args='Args'),FlowOperationEntity(name='Flow_op_two', input='Input', process='Process', output='Output', where='*', join = "join", args='Args'),FlowOperationEntity(name='Flow_op_three', input='Input', process='Process', output='Output', where='*', join = "join", args='Args')])]

    def get_flow_list_json(self) -> List[str]:
        return [
            '{"name": "flow1", "ops": [{"name": "Flow_op_one", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}, {"name": "Flow_op_two", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}, {"name": "Flow_op_three", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}]}',
            '{"name": "flow2", "ops": [{"name": "Flow_op_two", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}, {"name": "Flow_op_three", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}]}',
            '{"name": "flow3", "ops": [{"name": "Flow_op_one", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}]}',
            '{"name": "flow4", "ops": []}',
            '{"name": "flow5", "ops": []}',
            '{"name": "flow6", "ops": [{"name": "Flow_op_one", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}, {"name": "Flow_op_two", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}, {"name": "Flow_op_three", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}]}',
            '{"name": "flow7", "ops": [{"name": "Flow_op_one", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}, {"name": "Flow_op_two", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}, {"name": "Flow_op_three", "input": "Input", "process": "Process", "output": "Output", "join": "join", "args": "Args", "where": "*"}]}',
        ]

    def get_flow_op_list(self) -> List[FlowOperationEntity]:
        return [
            FlowOperationEntity(name = "Flow_op_1",  input = "Input", where = "*"),
            FlowOperationEntity(name = "Flow_op_2",  input = "Input", process = "Process", where = "*"),
            FlowOperationEntity(name = "Flow_op_3",  input = "Input", output = "Output", where = "*"),
            FlowOperationEntity(name = "Flow_op_4",  input = "Input", join="join", where = "*"),
            FlowOperationEntity(name = "Flow_op_5",  input = "Input", args = "Args", where = "*"),
            FlowOperationEntity(name = "Flow_op_6",  input = "Input", process = "Process", output = "Output", where = "*"),
            FlowOperationEntity(name = "Flow_op_7",  input = "Input", process = "Process", join="join", where = "*"),
            FlowOperationEntity(name = "Flow_op_8",  input = "Input", process = "Process", output = "Output", join="join", args = "Args", where = "*"),
            FlowOperationEntity(name = "Flow_op_9",  input = "Input", process = "Process", args = "Args", where = "*"),
            FlowOperationEntity(name = "Flow_op_10", input = "Input", output = "Output", join="join", where = "*"),
            FlowOperationEntity(name = "Flow_op_11", input = "Input", output = "Output", args = "Args", where = "*"),
            FlowOperationEntity(name = "Flow_op_12", input = "Input", join="join", args = "Args", where = "*"),
            FlowOperationEntity(name = "Flow_op_13", input = "Input", process = "Process", output = "Output", join="join", where = "*"),
            FlowOperationEntity(name = "Flow_op_14", input = "Input", process = "Process", output = "Output", args = "Args", where = "*"),
            FlowOperationEntity(name = "Flow_op_15", input = "Input", process = "Process", join="join", args = "Args", where = "*"),
            FlowOperationEntity(name = "Flow_op_16", input = "Input", process = "Process", output = "Output", join="join", args = "Args", where = "*"),
        ]

    def get_flow_op_list_json(self) -> str:
        return """[ 
        {
            "name":"Flow_op_1",
            "input":"Input",
            "process": null,
            "output": null,
            "join": null,
            "args": null,
            "where":"*"
        },
        {
            "name":"Flow_op_2",
            "input":"Input",
            "process":"Process",
            "output": null,
            "join": null,
            "args": null,
            "where":"*"
        },
        {
            "name":"Flow_op_3",
            "input":"Input",
            "process": null,
            "output":"Output",
            "join": null,
            "args": null,
            "where":"*"
        },
        {
            "name":"Flow_op_4",
            "input":"Input",
            "process": null,
            "output": null,
            "join":"join",
            "args": null,
            "where":"*"
        },
        {
            "name":"Flow_op_5",
            "input":"Input",
            "process": null,
            "output": null,
            "join": null,
            "args":"Args",
            "where":"*"
        },
        {
            "name":"Flow_op_6",
            "input":"Input",
            "process":"Process",
            "output":"Output",
            "join": null,
            "args": null,
            "where":"*"
        },
        {
            "name":"Flow_op_7",
            "input":"Input",
            "process":"Process",
            "output": null,
            "join":"join",
            "args": null,
            "where":"*"
        },
        {
            "name":"Flow_op_8",
            "input":"Input",
            "process":"Process",
            "output":"Output",
            "join":"join",
            "args":"Args",
            "where":"*"
        },
        {
            "name":"Flow_op_9",
            "input":"Input",
            "process":"Process",
            "output": null,
            "join": null,
            "args":"Args",
            "where":"*"
        },
        {
            "name":"Flow_op_10",
            "input":"Input",
            "process": null,
            "output":"Output",
            "join":"join",
            "args": null,
            "where":"*"
        },
        {
            "name":"Flow_op_11",
            "input":"Input",
            "process": null,
            "output":"Output",
            "join": null,
            "args":"Args",
            "where":"*"
        },
        {
            "name":"Flow_op_12",
            "input":"Input",
            "process": null,
            "output": null,
            "join":"join",
            "args":"Args",
            "where":"*"
        },
        {
            "name":"Flow_op_13",
            "input":"Input",
            "process":"Process",
            "output":"Output",
            "join":"join",
            "args": null,
            "where":"*"
        },
        {
            "name":"Flow_op_14",
            "input":"Input",
            "process":"Process",
            "output":"Output",
            "join": null,
            "args":"Args",
            "where":"*"
        },
        {
            "name":"Flow_op_15",
            "input":"Input",
            "process":"Process",
            "output": null,
            "join":"join",
            "args":"Args",
            "where":"*"
        },
        {
            "name":"Flow_op_16",
            "input":"Input",
            "process":"Process",
            "output":"Output",
            "join":"join",
            "args":"Args",
            "where":"*"
        }
    ]"""

    def test_json_to_flow_entity(self):
        flow_list_json = self.get_flow_list_json()
        flow_list_read = self.get_flow_list()
        for ind in range(len(flow_list_json)):
            self.assertEqual(flow_list_read[ind], self.flow_mapper.json_to_flow_entity(flow_list_json[ind]))

    def test_flow_entity_to_json(self):
        flow_list_json = self.get_flow_list_json()
        flow_list_read = self.get_flow_list()
        for ind in range(len(flow_list_json)):
            self.assertEqual(self.flow_mapper.flow_entity_to_json(flow_list_read[ind]),flow_list_json[ind])

    def test_json_to_flow_operation(self):
        flow_op_list_json = json.loads(self.get_flow_op_list_json())
        flow_op_list = self.get_flow_op_list()
        for ind in range(len(flow_op_list_json)):
            self.assertEqual(flow_op_list[ind], self.flow_mapper.json_to_flow_operation(json.dumps(flow_op_list_json[ind])))

    #def test_list_flow_operation_to_json(self):

    #def test_entity_flow_operation_to_json(self):




if __name__ == '__main__':
    unittest.main()
