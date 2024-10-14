from myactuator_lib.msgs import *
import can

# testing out parse
# 0x32 -> 50 degrees C
# 0x000A -> 10 amps
# 0x0064 -> 100 degrees per second
# 0x010E -> 270 degrees
parsed_msg = can.Message(arbitration_id=0x141,data=b'\xA2\x32\x0A\x00\x64\x00\x0E\x01')
print(SpeedClosedLoopControlMsg.parse_can_msg(parsed_msg))


hi = WriteAccelerationRAMROMMsg.make_can_msg(0x141, 1, 1000)
print(hi.arbitration_id, hi.data)
