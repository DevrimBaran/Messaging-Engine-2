 # Flow Message

## Message Type

```json
{
  "id": "message_uuid",
  "flow_name": "flow_name",
  "flow_id": "flow_id",
  "src_created_at": "datetime",
  "last_operation": "last_op_name",
  "sent_at": "datetime",
  "payload": "payload_base64",
  "original_payload": "payload_base64",
  "history": FlowMessage[]
}
```

### Validation

- Check if message is a valid JSON
- Check if `flow_name` is the name of a [Flow](./Flows.md)
- Check if `last_operation` exists
- Check if `id` already exists
- Check if all necessary fields are given
- Check if name-like fields match following regex: `r"^[a-zA-Z0-9_.-]{3,128}$"`
- Check if date-like fields have correct date format
- Check if `payload` is a valid base64 string (ascii chars + strlen == 0 mod 4)
- Check if decoded `payload` is a valid JSON
- Check if `last-operation` exists

## Messaging concept

This document is about:

1. *Messaging* in ME 2 in general and
2. about a single `/flow-messages` endpoint
   which can be used to exchange messages between instances of ME 2.

ME 2 uses the [CoAp protocol](https://coap.technology/) as a replacement for HTTP in IoT environments
to provide both resource and other messaging endpoints. ME 2 could receive and send arbitrary JSON objects - in theory.
But in ME2 these objects need to be (well-)defined for their specific purpose.

A list and more information about the CoAp endpoints of ME 2 (and 1) can be found [here](./Endpoints.md).

Note: In theory one could use more dynamic (process-specific and with well-defined data exchange schemata) in these
*Message*s as described here.

[Flow Execution Sequence Diagram](./../diagrams/sd_flow_execution.plantuml)

#### Also

- Each operation of ME 2 has its own (universally) unique ID
- Each message has a unique ID
- Each flow has a unique ID
- Each device has its own universally unique ID
    - Neighbors will know it in combination
      with the device's IP address

#### (Possible) Problems

- **Message duplicates:** No problem for ME 2, because operations (messages with the same `flow_id` + `id`)
  are only executed once by a single ME 2 instance within 12 hours.
- **Network availability:** ME 2 uses mechanisms to discover other ME 2 instances in the same subnet, which is
  described [here](./Neighbor%20Discovery.md).

## "/flow-messages" Endpoint

In this project this works technically with a
CoAp server endpoint `/flow-messages` where messages of other instances of the ME 2 (or *any* other
Third-Party software which deals with the `/flow-messages` endpoint) can be received and dynamically processed
with a well-defined payload.

- *Messages* - as defined here for this endpoint - are never dealing with the
  management of the `nodes`, `flows` and `operations` resources. This is done by other specific CoAp endpoints in ME 2.

**ME Version 1 (PIME)**: The system receives a message with (arbitrary) payload and executes it on a shell.

**ME Version 2**: The system receives a message and triggers a defines operation.

### Idea

- No (arbitrary) payload on console.
- Support of a few base operations which are clearly defined.

### Implementation Details

- The CoAp `/flow-messages` endpoint of ME 2 endpoint receives a POST-Request, stores and processes the message immediately -
  if possible
- Message Type Definition of FlowMessage: See above

- *NOTE*: The **old** type definition in **PIME** (ME 1):

```json
{
  "flow_id": "string",
  "payload": "string",
  "oiid": "string",
  "direction": "string"
}
```
