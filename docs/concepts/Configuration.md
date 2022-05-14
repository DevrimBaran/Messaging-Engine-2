# App Configuration

The configuration of a ME 2 instance is done via a configuration file in yaml format.
The configuration file should be placed alongside the central `main.py` of this repository.

## Example configuration

```yaml
instance_id: 123456678
loglevel: INFO
is_debug: false
sensors:
  - name: "Button-Sensor"
    type: button
    pin1: 12
    pin2: 13
    is_test_mode: true
actuators:
  - name: "LED-Actuator"
    type: led
    pin1: 12
    pin2: 13
    is_test_mode: false
```

- `instance_id`: (Required) A unique ID of this ME2 instance. Note: ME2 does not work correctly if there are several ME2
  instances
  with the same id in the same network.
- `loglevel`: (Required) The loglevel. Possible values
  are [these](https://docs.python.org/3/library/logging.html#logging-levels).
- `is_debug`: (Optional) Flag to indicate the debug mode of the application
- `sensors`: (Optional) The available sensors of ME2 are configured here. Array of sensor objects. Each sensor object
  has the
  following mandatory fields: `name, type, pin1` and optionally `is_test_mode`, `pin2` ..
- `actuators`: (Optional) The available actuators of ME2 are configured here. Array of actuator objects. Each sensor
  object has
  the following mandatory fields: `name, type, pin1` and optionally `is_test_mode`, `pin2` ..

### Operator description in yaml

- **`name`** (required, string)
- **`type`** (required, case-insensitive)
    - For sensors, one of: `TEMPERATURE`, `BUTTON`, `HALL`
    - For actuators: TODO
- **`pin1`** (required, integer)
- **`pin2`** (required for dual pin operator types, integer)
- **`is_test_mode`** (required, boolean)
