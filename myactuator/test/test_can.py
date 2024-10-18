from myactuator import SpeedClosedLoopControlMsg, SystemResetMsg
import matplotlib.pyplot as plt
import time, can, math

# from myactuator_lib import Motor
# hi = Motor(0x141)
# spd_msg = hi.Speed_Closed_loop_Control_Command(-100)
# print(spd_msg)

temps = []
amps = []
speeds = []
angles = []

bus = can.Bus(
    interface       = 'socketcan', 
    channel         = 'can0', 
    is_extended_id  = False, 
    bitrate         = 1000000, 
)

def generate_sine_wave(amplitude=150, frequency=1, num_samples=100):
    sine_wave = []
    for i in range(num_samples):
        t = i / num_samples
        sine_value = amplitude * math.sin(2 * math.pi * frequency * t)
        sine_wave.append(int(sine_value))

    return sine_wave

samples = 100
executed_speeds = generate_sine_wave(num_samples=samples)
id = 0x141
sleep_time = 0.1

bus.send(SystemResetMsg.make_can_msg(id))

try:
    for speed in executed_speeds:
        print(f'send speed dps: {speed}')
        msg = SpeedClosedLoopControlMsg.make_can_msg(id,speed)
        bus.send(msg,timeout=0.01)
        print(f'sent: {msg.data}')
        time.sleep(sleep_time)
        recv = bus.recv(timeout=0.01)
        arb_id_val, clean_data = SpeedClosedLoopControlMsg.parse_can_msg(recv)
        print(f'recv: {clean_data}\n')
        time.sleep(0.01)

        temps.append(clean_data.get('motor_temperature_c'))
        amps.append(clean_data.get('current_amps'))
        speeds.append(clean_data.get('speed_dps'))
        angles.append(clean_data.get('angle_degrees'))

except KeyboardInterrupt:
    print('\nKeyboardInterrupt: sending zero speed and shutdown')
    bus.send(SystemResetMsg.make_can_msg(id))

bus.send(SystemResetMsg.make_can_msg(id))
bus.shutdown()


xs = list(range(1, samples+1))
plt.figure(figsize=(10, 6))
plt.plot(xs, temps, label='temperature (c)', marker='.')
plt.plot(xs, amps, label='current draw (amps)', marker='.')
plt.plot(xs, executed_speeds, label='commanded speed (dps)', marker='.')
plt.plot(xs, speeds, label='measured speed (dps)', marker='.')
plt.plot(xs, angles, label='motor multiturn angle (degrees)', marker='.')

plt.title(f'Motor Data for Sinusoidal Speed Input')
plt.legend()
plt.show()
