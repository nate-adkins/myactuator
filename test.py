from msgs import SpeedClosedLoopControlMsg, AbsolutePositionClosedLoopControlMsg


speed = AbsolutePositionClosedLoopControlMsg()

hi = speed.make_msg(10, 10, 10)

print(hi.arbitration_id, hi.data)