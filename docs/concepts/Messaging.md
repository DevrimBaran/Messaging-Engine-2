# Messaging concept

This document is about:

1. *Messaging* in ME 2 in general and
2. about a single `/message` endpoint
   which can be used to exchange messages between instances of ME 2.

ME 2 uses the [CoAp protocol](https://coap.technology/) as a replacement for HTTP in IoT environments
to provide both resource and other messaging endpoints. ME 2 could receive and send arbitrary JSON objects - in theory.
But in ME2 these objects need to be (well-)defined for their specific purpose.

A list and more information about the CoAp endpoints of ME 2 (and 1) can be found [here](./Endpoints.md).

Note: In theory one could use more dynamic (process-specific and with well-defined data exchange schemata) in these
*Message*s as described here.

## Message exchange scenarios

Example: Happens between instances of ME 2 or other CoAp clients.

1. Message is sent by a sender to a receiver which takes the message and confirms it.
   The sender receives this confirmation. (Happy case)
2. Message is sent by a sender to a receiver, but never receives a response

#### The Message sending process is implemented this way:

1. Sending a message to a CoAp endpoint
2. If there is a response in a given time box, then ok -> success
3. If there is **no** response in a given time box, the message is sent again one time
   and a `NeighbourUpdateRequired` network event is thrown to update the network/availability status of the neighbours.
   As long as the neighbour with the target CoAp endpoint is considered online for the ME 2 sender instance, it will
   repeat sending the same message within an interval of *n* seconds. But there is also a general `resend_limit` for
   messages
   which means that a single message is sent at most `y` times.

#### Also

- Each operation of ME 2 has its own (universally) unique ID
- Each message has a unique ID
- Each flow has a unique ID
- Each device has its own universally unique ID
    - Neighbours will know it in combination
      with the device's IP address

#### (Possible) Problems
- **Message duplicates:** No problem for ME 2, because operations (messages with the same `action_id`, see below) 
are only executed once by a single ME 2 instance within 12 hours.
- **Network availability:** ME 2 uses mechanisms to discover other ME 2 instances in the same subnet (TBD).

## "/message" Endpoint

In this project this works technically with a
CoAp server endpoint `/messages` where messages of other instances of the ME 2 (or *any* other
Third-Party software which deals with the `/messages` endpoint) can be received and dynamically processed
with a well-defined payload.

- *Messages* - as defined here for this endpoint - are never dealing with the
  management of the `nodes`, `flows` and `operations` resources. This is done by other specific CoAp endpoints in ME 2.

**ME Version 1 (PIME)**: The system receives a message with (arbitrary) payload and executes it on a shell.

**ME Version 2**: The system receives a message and triggers a defines operation.

### Idea

- No (arbitrary) payload on console.
- Support of a few base operations which are clearly defined.

### Operations

There is an operation for each `NetworkEvent` listed [here](./Network%20Events.md):

- NeighbourRegister
- NeighbourUnregister
- NeighbourUpdateRegular
- NeighbourUpdateRequired

### Implementation Details

- The CoAp `/messages` endpoint of ME 2 endpoint receives a POST-Request, stores and processes the message immediately -
  if possible
- Message Type Definition:

```json
{
  "created_at": "string,datetime ISO 8601",
  "id": "uuid",
  "action_id": "uuid",
  "flow_id": "uuid",
  "payload": "string, to be defined for each operation/action type, Base64 encoded",
  "rescheduling_number": "uint",
  "src_device_id": "uuid",
  "src_created_at": "string,datetime ISO 8601"
}
```

- *NOTE*: The **old** type definition in **PIME** (ME 1):

```json
{
  "flow_id": "string",
  "payload": "string",
  "oiid": "string",
  "direction": "string"
}
```