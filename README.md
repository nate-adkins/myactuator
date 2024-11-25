# pyactuator
Python library for creating or parsing can/uart messages into base units values for [MYACTUATOR RMD-X](https://www.myactuator.com/downloads-x-series) motors <i><b> (last supported protocol: V3.9-240415)</b></i>

## To Do
- [x] package message metadata in standard format
- [x] can create and parse
- [x] uart create and parse
- [ ] publish to Python Package Index

## Usage

### Creating a can message
```python
from pyactuator import SpeedClosedLoopControlMsg

speed_dps = 1000 # goal speed of can message 
id = 0x141 # can arbitration id of intended motor

speed_can_msg = SpeedClosedLoopControlMsg.make_can_msg(can_arbitration_id,speed_dps)

# send can message...
```

### Creating a uart message
```python
from pyactuator import SpeedClosedLoopControlMsg

speed_dps = 1000 # goal speed of can message 
id = 0x141 # can arbitration id of intended motor

speed_uart_msg = SpeedClosedLoopControlMsg.make_uart_msg(can_arbitration_id,speed_dps)

# send uart message...
```

### Parsing a can message
```python
from pyactuator import SpeedClosedLoopControlMsg

recieved_message: can.Message # read from a can interface

recieved_data = SpeedClosedLoopControlMsg.parse_can_msg(recieved_message)

temp = recieved_data.get('motor_temperature_c')
current = recieved_data.get('current_amps')
speed = recieved_data.get('speed_dps')
angle = recieved_data.get('angle_degrees')
```

### Parsing a uart message
```python
from pyactuator import SpeedClosedLoopControlMsg

recieved_message: bytes # read from a uart interface

recieved_data = SpeedClosedLoopControlMsg.parse_uart_msg(recieved_message)

temp = recieved_data.get('motor_temperature_c')
current = recieved_data.get('current_amps')
speed = recieved_data.get('speed_dps')
angle = recieved_data.get('angle_degrees')
```
