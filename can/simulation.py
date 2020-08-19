import can
import control
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# matplotlib settings
matplotlib.rcParams['toolbar'] = 'None'
matplotlib.use('Qt5Agg')
OPTIONS = {'update_time': 200/1000}

# Create Node 0
node0 = can.interface.Bus(bustype='kvaser', channel='0')

def motor_sim():
    # Simulation parameters
    setpoint = 100
    tmax = 20
    step = 100
    # Vehicule parameters
    m = 1000       # (kg)      vehicle mass 
    b = 50         # (N.s/m)   damping coefficient
    # PI controller
    Kp = 300
    Ki = 15
    Cpi = control.tf([Kp, Ki], [1, 0])
    # Transfer function
    mot = control.tf([1], [m, b])
    gol = control.series(Cpi, mot)
    gcl = control.feedback(gol, 1)
    # Time
    t = np.linspace(0, tmax, step)
    # Input
    r = np.empty(len(t))
    r.fill(setpoint)
    # Output
    t, y, _ = control.forced_response(gcl, t, r)
    # Plot
    plt.figure()
    plt.title('Cruise Control Simulation')
    plt.axis([0, tmax+1, 0, setpoint+1])
    plt.grid()
    plt.xlabel('Time (s)')
    plt.ylabel('Speed (km/h)')
    # Animation + Sending message
    for i in range(step):
        y_int = int(round(y[i]))
        msg = can.Message(arbitration_id=100, data=[y_int, 0, 0, 0, 0, 0, 0])
        node0.send(msg)
        plt.scatter(t[i], y[i])
        plt.pause(OPTIONS['update_time'])
    plt.show()

if __name__ == "__main__":
    # Alert GUI when simulation starts
    msg_starting = can.Message(arbitration_id=200, data=[1, 0, 0, 0, 0, 0, 0])
    node0.send(msg_starting)
    # Launch simulation
    motor_sim()