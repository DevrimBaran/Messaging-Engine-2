# Flow Message

## Message Type

```json
{
  "id": "message_uuid",
  "flow_name": "flow_name",
  "src_created_at": "datetime",
  "last_operation": "last_op_name",
  "next_operation": "next_op_name",
  "sent_at": "datetime",
  "payload": "payload_base64",
  "count": "i",
  "history": FlowMessage[]
}
```

- `next_operation` must be validated by the receiver
- `history` is optional and only required in the top level `FlowMessage` object in the payload
