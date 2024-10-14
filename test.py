from msgs import SpeedClosedLoopControlMsg, MotorShutdownMsg, ReadMotorStatus2Msg, ReadMotorStatus3Msg
import serial, time, can

speed_msg_mkr = SpeedClosedLoopControlMsg()
speed_msg = speed_msg_mkr.make_uart_msg(0x141,600)
stop_msg_mkr = MotorShutdownMsg()
stop_msg = stop_msg_mkr.make_uart_msg(0x141)

status_mkr = ReadMotorStatus3Msg()
status_msg = status_mkr.make_uart_msg(0x141)

port = serial.Serial(
    port        = "/dev/ttyUSB0",
    baudrate    = 115200,
    timeout     = 2
)

responses = []
for n in range(200):
    port.write(speed_msg)
    time.sleep(0.1)
    responses.append(bytearray(port.read(13)))

port.write(stop_msg)

for response in responses:
    new_can_msg = can.Message(
        arbitration_id= 1 + 0x140,
        data = response[3:10],
    )
    id, val = speed_msg_mkr.parse_can_msg(new_can_msg)
    print(id, val)
