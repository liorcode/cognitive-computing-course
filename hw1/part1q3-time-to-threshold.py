import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


# Model Parameters
T       = 10    # Simulation time          [mSec]
dt      = 0.1   # Simulation time interval [mSec]
t_init  = 0     # Stimulus init time       [V]
vRest   = -70   # Resting potential        [mV]
Rm      = 1     # Membrane Resistance      [kOhm]
Cm      = 5     # Capacitance              [uF]
tau_ref = 1     # Refractory Period       [mSec]
vTh     = -40   # Spike threshold          [mV]
I       = 0.2   # Current stimulus         [mA]
vSpike  = 50    # Spike voltage            [mV]

# Simulation Parameters
time    = np.arange(0, T*1e-3 + dt*1e-3, dt*1e-3)  # Time array
Vm      = np.ones(len(time))*vRest*1e-3            # Membrane voltage array
tau_m   = Rm*1e3 * Cm*1e-6                         # Time constant
spikes  = []                                       # Spikes timings

stim = np.full(len(time), I*1e-3) # Triangular stimulation pattern

# Simulation
for i, t in enumerate(time[:-1]):
    if t > t_init:
        uinf = vRest*1e-3 + Rm*1e3 * I*1e-3
        Vm[i+1] = uinf + (Vm[i]-uinf)*np.exp(-dt*1e-3/tau_m)
        if Vm[i] >= vTh*1e-3:
            spikes.append(t*1e3)
            Vm[i]=vSpike*1e-3
            t_init = t + tau_ref*1e-3


# calculate the time to reach the threshold voltage
i_ = ((vTh * 1e-3 - vRest * 1e-3) / (I * 1e-3 * Rm * 1e3))
time_to_spike = -tau_m * 1e3 * np.log(1 - i_)
print(time_to_spike)

# Plotting
plt.figure(figsize=(10, 5))
plt.title('Leaky Integrate-and-Fire Model', fontsize=15)
plt.ylabel('Membrane Potential (mV)', fontsize=15)
plt.xlabel('Time (msec)', fontsize=15)
plt.plot(time*1e3, Vm*1e3, linewidth=5, label = 'Vm')
plt.plot(time*1e3, np.full(len(time), 80), label = 'Stimuli (Scaled)', color='sandybrown', linewidth=2)
plt.ylim([-75, 100])
plt.axvline(x=spikes[0], c='red', label = 'Spike')
for s in spikes[1:]:
    plt.axvline(x=s, c='red')
plt.axhline(y=vTh, c='black', label = 'Threshold', linestyle='--')

# Increase the number of scale marks on the x-axis
x_ticks = np.arange(0, 10, 0.5)  # Adjust the step size to your preference
plt.xticks(x_ticks)

plt.legend()
plt.show()
