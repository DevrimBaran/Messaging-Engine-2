# Flows

*Idea*: Use one Flow object specification for ME2 and give it to each instance which acts as described in the flow.

## Flow Type Description

```json
{
  "name": "flow_name",
  "ops": FlowOperationObject[]
}
```

- A flow `name` and operation names in general has to match the following regular expression: `^[a-zA-Z0-9_.-]{3,128}$`

### Flow Operations

- Are of type `input`, `process` and `output`
- Available (currently supported) values are defined below for each operation type
- Operation names can be used only one time in `ops`

### Flow Operation Type

```json
{
  "name": "flow_operation_name",
  "[input | process | output]": "operation_name",
  "where": "where_spec",
  "args": "operation_arguments"
}
```

- `name`: Unique flow operation name
- `input|process|output` A flow operation type with a valid flow operation id
- `where`: A definition where the flow operation can be executed
- `args`: Flow operation id specific arguments

## Flow where_spec

- `*` (default): all available nodes
- `instance_id`: a specific instance_id
- `instance_id1,instance_id2,...`: multiple instances

##### Validation

- Check if `ops` has at least 2 elements
- Check if all operation names are known and defined in `ops`
- Check if an instance exists for each `where`
- Check if there exists exactly one `input` per `Flow`
- Check if an instance exists with a [skill](./Skills.md) for all input/process/output operations
- Check if each flow is executable
- TBD

## Example

### General Temperature log

```json
{
  "name": "general_temp_log",
  "ops": [
    {
      "name": "sensor_read",
      "input": "sensor_temperature",
      "where": "*"
    },
    {
      "name": "log",
      "process": "log",
      "where": "specific_me2_instance"
    },
    {
      "name": "actuator_call",
      "output": "exit"
    }
  ]
}
```

### Magnet Beep

```json
{
  "name": "magnet_beep_flow",
  "ops": [
    {
      "name": "sensor_read",
      "input": "sensor_hall",
      "where": "me2_first"
    },
    {
      "name": "log",
      "process": "log",
      "where": "me2_second"
    },
    {
      "name": "beep_call",
      "output": "actuator_speaker",
      "where": "me2_third"
    }
  ]
}
```

## Available Input Operation Names

- `sensor_*`: for all supported sensors
    - `temperature`
    - `hall`
    - `button`

## Available Process Operation Names

- `log`: Log the current message, useful for debugging and testing
- `cep_intercept`: Log the current message, useful for debugging and testing
  - `args`: CEP Flow expression

## Available Output Operation Names

- `exit`: exit flow without further action (the only case when no `where` is required, see in Example above)
- `actuator_* <args>`: for all supported actuators
  - `led` 
    - `args`: One optional argument (Default is `True` to turn on LED, `False` to turn in off)
  - `speaker`
    - `args`: Three optional arguments (Has one input for duration and two for the pitch. Default is `2.0` for duration in seconds and `0.0005` for both inputs for the pitch)