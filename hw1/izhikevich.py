import numpy as np
import matplotlib.pyplot as plt

x  = 5
y  = 140

models = ['Regular Spiking', 'Chattering', 'Fast spiking', 'Intrinsically bursting', 'Low-threshold spiking', 'Thalamo-Cortical Tonic', 'Thalamo-Cortical Burst', 'Resonator']
a  = [0.02,     0.02,   0.1,    0.02,   0.02,   0.02,   0.02,   0.1]
b  = [0.2,      0.2,    0.2,    0.2,    0.25,   0.25,   0.25,   0.26]
c  = [-65,      -50,    -65,    -55,    -65,    -65,    -65,    -65]
d  = [8,        2,      2,      4,      2,      0.05,   0.05,   2]

v0 = [-70, -70, -70, -70, -70, -63, -87, -60] # Resting potential        [mV]
T       = 200                                 # Simulation time          [mSec]
dt      = 0.25                                 # Simulation time interval [mSec]

time    = np.arange(0, T + dt, dt)  # Time array

# Defining the stimulus (a step function):
stim = np.zeros(len(time))
for i,t in enumerate(stim):
    if i > 20:
        stim[i] = 15

# Simulation

trace = np.zeros((2,len(time))) # Tracing du and dv

for exp in range(len(a)):
    v  = v0[exp]
    u  = b[exp]*v
    spikes = []
    if models[exp] == 'Thalamo-Cortical Tonic':
        stim[:] = 0
        stim[60:] = 1
    if models[exp] == 'Thalamo-Cortical Burst':
        stim[:] = -1
        stim[160:] = 0.5
    if models[exp] == 'Resonator':
        stim[:] = 0.25
        stim[400:420] = 3

    for i, j in enumerate(stim):
        v += dt * (0.04*v**2 + x*v + y - u + stim[i])
        u += dt * a[exp]*(b[exp]*v-u)
        if v > 30:
            trace[0,i] = 30
            v = c[exp]
            u += d[exp]
        else:
            trace[0,i] = v
            trace[1,i] = u

    plt.figure(figsize=(10,5))
    plt.title('Izhikevich Model: {}'.format(models[exp]), fontsize=15)
    plt.ylabel('Membrane Potential (mV)', fontsize=15)
    plt.xlabel('Time (msec)', fontsize=15)
    plt.plot(time, trace[0], linewidth=2, label = 'Vm')
    plt.plot(time, trace[1], linewidth=2, label = 'Recovery', color='green')
    plt.plot(time, stim + v0[exp], label = 'Stimuli (Scaled)', color='sandybrown', linewidth=2)
    plt.legend(loc=1)
    plt.show()