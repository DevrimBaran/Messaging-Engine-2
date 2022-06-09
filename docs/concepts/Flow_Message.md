# Flow Message

## Message Type

```json
{
  "id": "message_uuid",
  "flow_name": "flow_name",
  "flow_id": "flow_id",
  "src_created_at": "datetime",
  "last_operation": "last_op_name",
  "next_operation": "next_op_name",
  "sent_at": "datetime",
  "payload": "payload_base64",
  "original_payload": "payload_base64",
  "count": "i",
  "history": FlowMessage[]
}
```

- `next_operation` must be validated by the receiver
- `history` is optional and only required in the top level `FlowMessage` object in the payload
- `payload` usually contains the result of the latest step, while `original_payload` always contains the original sensor
  result

### Validation

- Check if message is a valid JSON
- Check if `last_operation` exists
- Check if `next_operation` exists
- Check if `id` already exists
- Check if all necessary fields are given
- Check if name-like fields match following regex: `r"^[a-zA-Z0-9_.-]{3,128}$"`
- Check if date-like fields have correct date format
- Check if `count` is an integer
- Check if `payload` is a valid base64 string (ascii chars + strlen == 0 mod 4)
- Check if decoded `payload` is a valid JSON
- Check if `last-operation` exists
- Check if `next-operation` exists