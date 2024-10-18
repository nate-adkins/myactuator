from myactuator import SpeedClosedLoopControlMsg, SystemResetMsg
import matplotlib.pyplot as plt
import time, serial, math


port = serial.Serial(
    port        = "/dev/ttyUSB0",
    baudrate    = 115200,
    timeout     = 3
)

temps = []
amps = []
speeds = []
angles = []

def generate_sine_wave(amplitude=150, frequency=1, num_samples=100):
    sine_wave = []
    for i in range(num_samples):
        t = i / num_samples
        sine_value = amplitude * math.sin(2 * math.pi * frequency * t)
        sine_wave.append(int(sine_value))

    return sine_wave

samples = 100
executed_speeds = generate_sine_wave(num_samples=samples)# [0,25,50,75,100,75,50,25,0] # generate_sine_wave(num_samples=samples)
id = 0x141
sleep_time = 0.1

port.write(SystemResetMsg.make_uart_msg(id))
print(port.read(13))

try:
    for speed in executed_speeds:
        print(f'send speed dps: {speed}')
        msg = SpeedClosedLoopControlMsg.make_uart_msg(id,speed)
        port.write(msg)
        print(f'sent: {msg}')
        recv = port.readline()
        print(f'received bytes: {recv}')
        arb_id_val, clean_data = SpeedClosedLoopControlMsg.parse_uart_msg(recv)
        print(f'recv: {arb_id_val, clean_data}\n')
        time.sleep(0.1)

        temps.append(clean_data.get('motor_temperature_c'))
        amps.append(clean_data.get('current_amps'))
        speeds.append(clean_data.get('speed_dps'))
        angles.append(clean_data.get('angle_degrees'))

except Exception as e:
    print(e.with_traceback())
    port.write(SystemResetMsg.make_uart_msg(id))

port.write(SystemResetMsg.make_uart_msg(id))
port.close()


xs = list(range(1, len(executed_speeds)+1))
plt.figure(figsize=(10, 6))
plt.plot(xs, temps, label='temperature (c)', marker='.')
plt.plot(xs, amps, label='current draw (amps)', marker='.')
plt.plot(xs, executed_speeds, label='commanded speed (dps)', marker='.')
plt.plot(xs, speeds, label='measured speed (dps)', marker='.')
plt.plot(xs, angles, label='motor multiturn angle (degrees)', marker='.')

plt.title(f'Motor Data for Sinusoidal Speed Input')
plt.legend()
plt.show()
