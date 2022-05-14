# Health Endpoint
When the health endpoint is called following payload will be send:
## System Health JSON Payload

```
{
    "version": The version of pime which is currently running on the device,
    "cpu_core_count": The count of the cpu cores which the cpu on the device has,
    "cpu_usage": The usage of cpu in percentage,
    "ram_total" : The total amount of RAM on the device,
    "ram_available": The available RAM on the device given in bytes,
    "ram_used": The used RAM on the device given in bytes,
    "ram_used_percentage": The used RAM on the device in percentage,
    "neighbour_count": The total amount of neigbhours in the current pime network,
    "sensor_count": The total amount of sensors on the current device,
    "actuator_count": The total coamountunt of acutators on the current device
}
```