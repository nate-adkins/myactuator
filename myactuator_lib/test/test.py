from myactuator_lib.msgs import SpeedClosedLoopControlMsg, MotorShutdownMsg, ReadMotorStatus1Msg,ReadMotorStatus2Msg, ReadMotorStatus3Msg
import serial, time, can, csv

speed_msg_mkr = SpeedClosedLoopControlMsg()
speed_msg = speed_msg_mkr.make_uart_msg(0x141,150)
stop_msg_mkr = MotorShutdownMsg()
stop_msg = stop_msg_mkr.make_uart_msg(0x141)

status_mkr = ReadMotorStatus3Msg()
status_msg = status_mkr.make_uart_msg(0x141)

port = serial.Serial(
    port        = "COM5",
    baudrate    = 115200,
    timeout     = 2
)

responses = []
for n in range(200):
    port.write(ReadMotorStatus3Msg.make_uart_msg(0x141))
    time.sleep(0.1)
    responses.append(bytearray(port.read(13)))

port.write(stop_msg)

for response in responses:
    new_can_msg = can.Message(
        arbitration_id= 1 + 0x140,
        data = response[3:10],
    )
    id, val = ReadMotorStatus3Msg.parse_can_msg(new_can_msg)
    print(id, val)

filename = 'myactuator_lib/status_3_output.csv'

# Write data to the CSV file
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(responses)
