from myactuator import SpeedClosedLoopControlMsg, AbsolutePositionClosedLoopControlMsg
import serial, time, can, csv

port = serial.Serial(
    port        = "/dev/ttyUSB0",
    baudrate    = 115200,
    timeout     = 3
)

speed = 10
id = 0x141
repeats = 15

currents = []

for n in range(repeats):
    port.write(AbsolutePositionClosedLoopControlMsg.make_uart_msg(id,speed,goal_angle))
    time.sleep(2)
    print(f'bytes: {recv}')
    id, data = SpeedClosedLoopControlMsg.parse_uart_msg(recv)
    print(data)
    time.sleep(1)
    currents.append(data('current_amps'))

    speed += 10


port.write(SpeedClosedLoopControlMsg.make_uart_msg(id,0))
port.close()


