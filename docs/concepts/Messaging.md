# Messaging concept

**PIME Version 1**: The system receives a message with (arbitrary) payload and executes it on a shell.

**PIME Version 2**: The system receives a message and triggers a defines operation.

## Purpose/Target

- No arbitrary payload on console.
- Support of a few base operations which are clearly defined.

## Operations

- Echo Ping
- Heartbeat-Trigger (?)

## Implementation

- The CoAp `/messages` endpoint of PIME 2 endpoint receives a POST-Request, stores and processes the message immediately - if possible
