import json

# Registry to keep track of message classes
message_classes = {}

class MsgBase:
    def __init__(self):
        # Protocol name
        self.protoName = ""

    @staticmethod
    def Encode(msgBase):
        """Encode the message object to a JSON string and then to bytes."""
        # Serialize the message object's dictionary to a JSON string
        s = json.dumps(msgBase.__dict__)
        # Encode the JSON string to bytes using UTF-8 encoding
        return s.encode('utf-8')

    @staticmethod
    def Decode(protoName, bytes_data, offset, count):
        """Decode bytes to a message object based on the protoName."""
        # Decode the specified portion of bytes to a JSON string
        s = bytes_data[offset:offset+count].decode('utf-8')
        # Deserialize the JSON string to a dictionary
        data = json.loads(s)

        # Retrieve the message class from the registry
        cls = message_classes.get(protoName)
        if cls is None:
            print(f"Class {protoName} not found")
            return None

        # Create an instance of the message class and update its attributes
        msgBase = cls()
        msgBase.__dict__.update(data)
        return msgBase

    @staticmethod
    def EncodeName(msgBase):
        """Encode the protocol name with a 2-byte length prefix."""
        # Encode the protocol name to bytes using UTF-8
        name_bytes = msgBase.protoName.encode('utf-8')
        length = len(name_bytes)
        # Pack the length as a 2-byte little-endian integer
        length_bytes = length.to_bytes(2, byteorder='little')
        # Return the combined length and name bytes
        return length_bytes + name_bytes

    @staticmethod
    def DecodeName(bytes_data, offset):
        """Decode the protocol name from bytes starting at the given offset."""
        # Must have at least 2 bytes for the length
        if offset + 2 > len(bytes_data):
            return "", 0

        # Read the 2-byte length prefix (little-endian)
        length_bytes = bytes_data[offset:offset+2]
        length = int.from_bytes(length_bytes, byteorder='little')

        # Ensure there's enough data for the name
        if offset + 2 + length > len(bytes_data):
            return "", 0

        # Extract and decode the protocol name
        name_bytes = bytes_data[offset+2:offset+2+length]
        name = name_bytes.decode('utf-8')
        count = 2 + length  # Total bytes read (length prefix + name)
        return name, count
if __name__ == "__main__":    
    # Example message class inheriting from MsgBase
    class MyMessage(MsgBase):
        def __init__(self):
            super().__init__()
            self.protoName = "MyMessage"
            self.content = ""

    # Register the message class
    message_classes['MyMessage'] = MyMessage
    
    # Create a message instance
    msg = MyMessage()
    msg.content = "Hello, World!"

    # Encode the message
    encoded_msg = MsgBase.Encode(msg)
    print(f"Encoded message bytes: {encoded_msg}")

    # Encode the message name
    encoded_name = MsgBase.EncodeName(msg)
    print(f"Encoded name bytes: {encoded_name}")

    # Combine name and message bytes to form the full message
    full_message = encoded_name + encoded_msg
    print(f"Full message bytes: {full_message}")

    # Simulate receiving the message
    received_bytes = full_message

    # Decode the message name
    proto_name, name_count = MsgBase.DecodeName(received_bytes, 0)
    print(f"Decoded protoName: {proto_name}, Bytes read for name: {name_count}")

    # Decode the message body
    msg_base = MsgBase.Decode(proto_name, received_bytes, name_count, len(received_bytes) - name_count)
    if msg_base:
        print(f"Decoded message content: {msg_base.content}")