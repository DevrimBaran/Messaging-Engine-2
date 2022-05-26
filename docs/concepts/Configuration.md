# App Configuration

The configuration of a ME 2 instance is done via a configuration file in yaml format.
The configuration file should be placed alongside the central `main.py` of this repository.

## Example configuration

```yaml
instance_id: 123456678
loglevel: INFO
is_debug: false
host: 127.0.0.1
port: 5683
read_interval: 3.0
sensors:
  - name: "Button-Sensor"
    type: button
    gpio1: 12
    gpio2: 13
    is_test_mode: true
actuators:
  - name: "LED-Actuator"
    type: led
    gpio1: 12
    gpio2: 13
    is_test_mode: false
# TODO: actuator support is not yet implemented
```

- `instance_id`: (Required) A unique ID of this ME2 instance. Note: ME2 does not work correctly if there are several ME2
  instances
  with the same id in the same network.
- `host`: (Required) An IP address, the host of the CoAp-Server. Default: `127.0.0.1`
- `port`: (Required) CoAp-Server port. Default: `5683`
- `read_interval`: (Required) The interval as float value in seconds sensors are read. Default is 1 Second: `1.0` (Range: 0.3-300)
- `loglevel`: (Required) The loglevel. Possible values
  are [these](https://docs.python.org/3/library/logging.html#logging-levels).
- `is_debug`: (Optional) Flag to indicate the debug mode of the application
- `sensors`: (Optional) The available sensors of ME2 are configured here. Array of sensor objects. Each sensor object
  has the
  following mandatory fields: `name, type, gpio1` and optionally `is_test_mode`, `gpio2` ..
- `actuators`: (Optional) The available actuators of ME2 are configured here. Array of actuator objects. Each sensor
  object has
  the following mandatory fields: `name, type, gpio1` and optionally `is_test_mode`, `gpio2` ..

### Operator description in yaml

- **`name`** (required, string)
- **`type`** (required, case-insensitive)
    - For sensors, one of: `TEMPERATURE`, `BUTTON`, `HALL`
    - For actuators: TODO
- **`gpio1`** (required, integer)
- **`gpio2`** (required for dual gpio operator types, integer)
- **`is_test_mode`** (required, boolean)

## Python

```python
pime2.config.get_me_conf()
```

