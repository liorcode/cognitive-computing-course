import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Model Parameters
T = 50  # Simulation time [mSec]
dt = 0.1  # Simulation time interval [mSec]
vRest = -70  # Resting potential [mV]
Rm = 1  # Membrane Resistance [kOhm]
tau_ref = 1  # Refractory Period [mSec]
vTh = -40  # Spike threshold [mV]
vSpike = 50  # Spike voltage [mV]
Is = np.linspace(0.1, 3, 10)  # Different stimulus currents [mA]

# Different time constants to simulate
tau_ms = [5, 10, 20]  # Membrane time constants [ms]

# Create plot
fig, ax = plt.subplots()

for tau_m in tau_ms:
    freqs = []
    for I in Is:
        # Simulation Parameters
        time = np.arange(0, T * 1e-3 + dt * 1e-3, dt * 1e-3)  # Time array
        Vm = np.ones(len(time)) * vRest * 1e-3  # Membrane voltage array
        spikes = []  # Spikes timings
        stim = I * 1e-3 * signal.windows.triang(len(time))  # Triangular stimulation pattern

        t_init = 0  # Reset initial time for stimulus on each loop
        for i, t in enumerate(time[:-1]):
            if t > t_init:
                uinf = vRest * 1e-3 + Rm * 1e3 * stim[i]
                Vm[i + 1] = uinf + (Vm[i] - uinf) * np.exp(-dt   / tau_m)
                if Vm[i] >= vTh * 1e-3:
                    spikes.append(t * 1e3)
                    Vm[i] = vSpike * 1e-3
                    t_init = t + tau_ref * 1e-3

        # Calculate frequency
        freq = len(spikes) / (T * 1e-3)
        freqs.append(freq)

    # Plot I-f curve for the current tau_m
    ax.plot(Is, freqs, label=f'$\\tau_m = {tau_m:.0f}$ ms')

ax.set_xlabel('Stimulus Current (mA)')
ax.set_ylabel('Firing Rate (Hz)')
ax.legend()
ax.set_title('I-f curves for different $\\tau_m$')
plt.show()
