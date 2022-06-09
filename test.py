from pime2.entity import FlowEntity, FlowOperationEntity
import json
from dacite import from_dict

from pime2.message import FlowCreateResultMessage

from pime2.mapper.flow_mapper import FlowMapper
def get_flow_op_list_json() -> str:
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
def get_flow_op_list():
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

flow_op1 = FlowOperationEntity("Flow_op_one","Input","Process", "Output", "*","Args")

flow_op2 = FlowOperationEntity("Flow_op_two","Input","Process", "Output", "*","Args")

flow_op3 = FlowOperationEntity("Flow_op_three","Input","Process", "Output", "*","Args")

flow_op_list = [flow_op1, flow_op2, flow_op3]

flow = FlowEntity("Hello", flow_op_list)

#print(flow.__dict__)

seriazable_flow_dict = flow.__dict__
flow_operations_array = seriazable_flow_dict['ops']
seriazable_flow_operation_array = []

for flow_op in flow_operations_array:
    seriazable_flow_operation_array.append(flow_op.__dict__) 
seriazable_flow_dict['ops'] = seriazable_flow_operation_array

#print(seriazable_flow_dict)
#print("\n")
#print(json.dumps(seriazable_flow_dict))

json_str = '{"name": "Hello", "ops": [{"name": "Flow_op_one", "input": "Input", "process": "Process", "output": "Output", "where": "*", "args": "Args"}, {"name": "Flow_op_two", "input": "Input", "process": "Process", "output": "Output", "where": "*", "args": "Args"}, {"name": "Flow_op_three", "input": "Input", "process": "Process", "output": "Output", "where": "*", "args": "Args"}]}'
json_obj = json.loads(json_str)
flow_name = json_obj['name'] 
json_flow_ops_array = json_obj['ops']
flow_ops_list = []
for flow_op in json_flow_ops_array:
     flow_ops_list.append(FlowOperationEntity(flow_op['name'], flow_op['input'], flow_op['process'], flow_op['output'], flow_op['where'], flow_op['args']))
flow = FlowEntity(flow_name, flow_ops_list)
#print(json_obj["hund"])
flow_op_list = get_flow_op_list()
flow_op_list_dict = []
for flow_op in flow_op_list:
    flow_op_list_dict.append(flow_op.__dict__)
flow_mapper = FlowMapper()
flow =  FlowEntity("flow3",[FlowOperationEntity(name='Flow_op_one', input='Input', process='Process', output='Output', where='*', join = "join", args='Args')])
print(flow)
print(json.dumps(FlowCreateResultMessage(flow)))
#for flow_op in flow_op_list_dict:
#    print(from_dict(data_class=FlowOperationEntity, data=flow_op))

#print(json.loads(get_flow_op_list_json()))