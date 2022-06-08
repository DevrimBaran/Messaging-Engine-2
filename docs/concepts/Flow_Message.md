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

- `id` is unique per message
- `flow_name` is the name of a [Flow](./Flows.md)
- `flow_id` is unique per flow instance (set once in the `input` operation of the flow)
- `last_operation` gives the receiver the information what to do next, must be validated by the receiver
- `history` is optional and only required in the top level `FlowMessage` object in the payload
- `payload` usually contains the result of the latest step, while 
- `original_payload` always contains the original sensor result
- 