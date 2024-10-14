import can
from pymodbus.utilities import computeCRC

BYTE_ORDER = 'little'

class _CanMsgParam():
    def __init__(self, name, start_index, byte_length, transform_func):
        self.name: str = name
        self.start_index: int = start_index
        self.byte_length: int = byte_length
        self.transform_func = transform_func

class _BaseMsg:
    def __init__(self):
        self.cmd_byte = None
        self.sent_parameters: list[_CanMsgParam] = []
        self.received_parameters: list[_CanMsgParam] = []

    def make_uart_msg(self,arb_id, *args)-> bytearray:
        can_msg = self.make_can_msg(arb_id, *args)
        crc = computeCRC(bytes([0x3e, can_msg.arbitration_id - 0x140, 0x08] + can_msg.data))          
        return bytearray([0x3e, can_msg.arbitration_id - 0x140, 0x08] + can_msg.data + [crc>>8, crc&0xFF])
  
    def make_can_msg(self, arb_id, *args) -> can.Message:

        if len(args) != len(self.sent_parameters):
            raise ValueError(f'{len(args)} arguments were given, requires {len(self.sent_parameters)} {[param.name for param in self.sent_parameters]}')

        new_msg = can.Message()
        new_msg.arbitration_id = arb_id


        new_data = [0] * 8
        for i, param in enumerate(self.sent_parameters):
            param_val: int = param.transform_func(args[i])
            new_bytes = list(param_val.to_bytes(param.byte_length,BYTE_ORDER))
            new_data[param.start_index:param.start_index + param.byte_length] = new_bytes

        new_data[0] = self.cmd_byte
        new_msg.data = new_data
        return new_msg
    
    def parse_uart_msg(self, bytes: bytes) -> tuple[int, dict[str, int]]:
        new_can_msg = can.Message(
            arbitration_id= 1 + 0x140,
            data = bytes[3:10],
        )
        return self.parse_can_msg(new_can_msg)

    def parse_can_msg(self, recv_msg: can.Message) -> tuple[int, dict[str, int]]:

        returned_params: dict[str, int]= {}

        arb_id = recv_msg.arbitration_id
        for i, param in enumerate(self.received_parameters):
            new_param_val = int.from_bytes(recv_msg.data[param.start_index:param.start_index + param.byte_length],byteorder=BYTE_ORDER, signed=False)
            returned_params[param.name] = new_param_val  # Change this line

        return arb_id, returned_params


def int_to_byte_array(int_values, starting_indices, byte_lengths, transform_fns):
    byte_array = bytearray(8)
    occupied_bytes = [0] * 8
    for index, length in zip(starting_indices, byte_lengths):
        if index < 0 or index + length > 8:
            raise ValueError("Integer placement exceeds the available 8-byte range.")
        for i in range(index, index + length):
            if occupied_bytes[i]:
                raise ValueError(f"Byte overlap detected at index {i}.")
            occupied_bytes[i] = 1
    for value, index, length, transform_fn in zip(int_values, starting_indices, byte_lengths, transform_fns):
        transformed_value = transform_fn(value)
        max_value = (1 << (length * 8)) - 1
        if transformed_value < 0 or transformed_value > max_value:
            raise ValueError(f"Transformed value {transformed_value} is too large for {length} bytes.")
        byte_representation = transformed_value.to_bytes(length, byteorder='big', signed=False)
        byte_array[index:index + length] = byte_representation
    return list(byte_array)

def byte_array_to_int(uint8_list, indices, byte_lengths, labels, transform_fns):
    int_label_map = {}
    byte_array = bytearray(uint8_list)
    for label, index, length, transform_fn in zip(labels, indices, byte_lengths, transform_fns):
        byte_slice = byte_array[index:index + length]
        integer_value = int.from_bytes(byte_slice, byteorder='big', signed=False)
        transformed_value = transform_fn(integer_value)
        int_label_map[label] = transformed_value
    return int_label_map