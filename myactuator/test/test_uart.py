from myactuator import SpeedClosedLoopControlMsg, SystemResetMsg
import serial, time

port = serial.Serial(
    port        = "/dev/ttyUSB0",
    baudrate    = 115200,
    timeout     = 3
)

speed = 50
id = 0x141
sleep_time = 0.5
repeats = 20

port.write(SystemResetMsg.make_uart_msg(id))

try:
    for n in range(repeats):
        msg = SpeedClosedLoopControlMsg.make_uart_msg(id,speed)
        port.write(msg)
        print(f'sent: {msg}')
        time.sleep(0.01)
        recv = port.read(13)
        print(f'response: {recv}')
        clean_data = SpeedClosedLoopControlMsg.parse_uart_msg(recv)
        print(clean_data)
        time.sleep(sleep_time)
        port.write(SpeedClosedLoopControlMsg.make_uart_msg(id,0))
        time.sleep(sleep_time)
except KeyboardInterrupt:
    print('\nKeyboardInterrupt: sending zero speed and shutdown')
    port.write(SpeedClosedLoopControlMsg.make_uart_msg(id,0))
    port.write(SystemResetMsg.make_uart_msg(id))
    port.close()

port.write(SpeedClosedLoopControlMsg.make_uart_msg(id,0))
port.write(SystemResetMsg.make_uart_msg(id))
port.close()