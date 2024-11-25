import can
BYTE_ORDER = 'little'


def compute_crc(data):
    crc16_table = []
    for byte in range(256):
        crc = 0x0000
        for _ in range(8):
            if (byte ^ crc) & 0x0001:
                crc = (crc >> 1) ^ 0xa001
            else: crc >>= 1
            byte >>= 1
        crc16_table.append(crc)
            
    crc = 0xffff
    for a in data:
        idx = crc16_table[(crc ^ a) & 0xff]
        crc = ((crc >> 8) & 0xff) ^ idx
    swapped = ((crc << 8) & 0xff00) | ((crc >> 8) & 0x00ff)
    return swapped


class _CanMsgParam:

    def __init__(self, name, start_index, byte_length, transform_func):
        self.name: str = name
        self.start_index: int = start_index
        self.byte_length: int = byte_length
        self.transform_func = transform_func


class _BaseMsg:


    @classmethod
    def make_can_msg(cls, arb_id, *args) -> can.Message:

        if len(args) != len(cls._sent_parameters):
            raise ValueError(f'{len(args)} arguments were given, requires {len(cls._sent_parameters)} {[param.name for param in cls._sent_parameters]}')

        new_data = [0] * 8
        for i, param in enumerate(cls._sent_parameters):
            param_val: int = param.transform_func(args[i])
            new_bytes = list(param_val.to_bytes(param.byte_length, BYTE_ORDER, signed=True))
            new_data[param.start_index:param.start_index + param.byte_length] = new_bytes
        new_data[0] = cls._cmd_byte

        new_msg = can.Message()
        new_msg.arbitration_id = arb_id
        new_msg.data = new_data
        new_msg.is_extended_id = False
        new_msg.dlc = 8
        return new_msg


    @classmethod
    def make_uart_msg(cls, arb_id, *args) -> bytearray:
        can_msg = cls.make_can_msg(arb_id, *args)
        crc = compute_crc(bytes([0x3e, can_msg.arbitration_id - 0x140, 0x08] + can_msg.data))
        return bytearray([0x3e, can_msg.arbitration_id - 0x140, 0x08] + can_msg.data + [crc >> 8, crc & 0xFF])


    @classmethod
    def parse_can_msg(cls, recv_msg: can.Message) -> tuple[int, dict[str, str|int]]:
        returned_params: dict[str, str|int] = {}
        arb_id = recv_msg.arbitration_id
        for param in cls._received_parameters:
            new_param_val = int.from_bytes(recv_msg.data[param.start_index:param.start_index + param.byte_length], byteorder=BYTE_ORDER, signed=True)
            returned_params[param.name] = param.transform_func(new_param_val)

        return arb_id, returned_params


    @classmethod
    def parse_uart_msg(cls, bytes: bytes) -> tuple[int, dict[str, str|int]]:
        new_can_msg = can.Message(
            arbitration_id= bytes[0] + 0x140,
            data=bytearray(bytes)[3:10],
        )
        return cls.parse_can_msg(new_can_msg)