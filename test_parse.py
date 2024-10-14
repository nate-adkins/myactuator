from msgs import *
import can
speed = SpeedClosedLoopControlMsg()

# testing out parse
# 0x010E -> 270 degrees
# 0x0064 -> 100 degrees per second
# 0x000A -> 10 amps
# 0x32 -> 50 degrees C
fake_recv_msg = can.Message(
    arbitration_id=0x141,
    data=b'\xA2\x32\x0A\x00\x64\x00\x0E\x01',
    )

id, params = speed.parse_msg(fake_recv_msg)
print(id,params)