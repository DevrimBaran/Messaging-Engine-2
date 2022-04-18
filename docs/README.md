# PIME 2 Documentation

## Processes

- **PIME Deployment:** The whole software is getting rolled out
- **Data Flow Model Deployment:** A Data Flow Model is rolled out
- **Ping Request:** Connecting to "Hello" endpoint
- **Neighbour Provisioning:** The system gets information about a (new) PIME2-neighbour-instance
- **Operation Provisioning:** The system gets information about the operation(s) it should work with
- **[Message Sending](./concepts/Messaging.md):** The system receives a message with (arbitrary) payload
- **System Health Metrics:** The system provides information about its state

## Concepts

### Multi-Sensor-Support

### Messaging
#### (Discrete) Message Payloads
#### Message-Validation (syntactic + semantic)
#### Message Prioritization

### Neighbour Discovery/Dynamic Network

"Heartbeat"


### Monitoring, Observability

### Availability

### Integration with MEConfigurator, MBP + Data Flow Modelling Tool

### Simulation / Benchmarking

### Failover-Concepts

## Diagrams

Download `plantuml.jar` [here](https://github.com/plantuml/plantuml/releases).

To (re-)generate the diagrams copy a `plantuml.jar` in `./diagrams` and execute `generate_diagrams.sh`.

- [PlantUML](http://plantuml.com)
- [PlantUML cli usage](http://plantuml.com/de/command-line)
