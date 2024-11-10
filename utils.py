import numpy as np
from matplotlib import pyplot as plt

class ExperimentResult:
    def __init__(self, t, v, i, w):
        self.t = t
        self.v = v
        self.i = i
        self.w = w
class Memristor:
    def __init__(self, R_on, R_off, D, mu, w_0=0):
        self.R_on = R_on
        self.R_off = R_off
        self.D = D
        self.mu = mu
        self.w_0 = w_0
        self.w = w_0

    def apply_voltage(self, v_t):
        """
        Apply a voltage to the memristor.
        Assume a piecewise-linear evolution of voltage vs time.

        Parameters
        ----------
        v_t: ndarray of shape (n, 2, ...)
            The voltage-time series. n is the number of timesteps to consider.
            The first dimension is timesteps, and the second dimension is the separation between time and voltage.
            That is, v_t[:,0] must be time values in seconds, and v_t[:,1] must be voltages.
        """
        # in second dimension, order is t, i, w
        # iw_t = np.zeros((v_t.shape[0],3,v_t.shape[2:]))
        i = np.zeros((v_t.shape[0],*(v_t.shape[2:])))
        w = np.zeros((v_t.shape[0],*(v_t.shape[2:])))
        # perhaps there's a better way of doing this than a for-loop lol
        # iw_t[:,0] = v_t[:,0]
        # iw_t[0, 2] = self.w
        w[0] = self.w
        for timestep in range(v_t.shape[0]):
            # iw_t[timestep, 1] = v_t[timestep, 1]/(
            #     self.R_on*iw_t[timestep, 2]/self.D
            #     + self.R_off*(1-iw_t[timestep, 2]/self.D)
            #     )
            i[timestep] = v_t[timestep, 1]/(
                self.R_on*w[timestep]/self.D
                + self.R_off*(1-w[timestep]/self.D)
                )
            # don't want to write out of range, since we put in the first w value and then step further
            if timestep == v_t.shape[0] - 1:
                break
            w[timestep+1] = w[timestep] + self.mu*self.R_on/self.D*i[timestep]*(v_t[timestep +1, 0] - v_t[timestep, 0])

        return ExperimentResult(v_t[:,0], v_t[:,1], i, w)
        

def plot_i(results, markersize=3):
    """
    Plot voltage and current.

    Parameters
    ----------
    results: dict, keys are strings, values are ExperimentResut objects
        A dictionary of the different experiments performed that we want to plot
    """
    # List of marker styles to cycle through
    markers = ['o', 's', '^', 'D', 'v', 'P', '*']

    fig, ax1 = plt.subplots()

    # Plot voltage on the left y-axis
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Voltage (V)', color='r')
    ax1.tick_params(axis='y', labelcolor='r')

    # Create a second y-axis sharing the same x-axis
    ax2 = ax1.twinx()
    ax2.set_ylabel('Current (A)', color='b')
    ax2.tick_params(axis='y', labelcolor='b')

    for n, pair in enumerate(results.items()):
        # pair[0] is the label, and pair[1] is the ExperimentResult
        ax1.plot(pair[1].t, pair[1].v, color='r', marker=markers[n % len(markers)], markersize=markersize, linestyle='-', label=pair[0])
        ax2.plot(pair[1].t, pair[1].i, color='b', marker=markers[n % len(markers)], markersize=markersize, linestyle='-', label=pair[0])

    # Add a legend for clarity
    fig.legend(loc="upper right", bbox_to_anchor=(0.85, 0.85))

    # Show the plot
    plt.title('Voltage and Current vs Time')
plt.show()