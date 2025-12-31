import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
This code is intended to take one of the experimental lists generated using the randomization script,
and generate a corresponding simulated EEG for each stimulus. 
Generated EEG will represent pre-processed data, hence with minimal noise.
I also wanted to generate a visual representation of these EEGs at the end.
AI assistance has been used in this script, mainly to figure out the steps for emulating/representing EEGs
as well as figuring out the logic/structure for this code.
"""

# defining global parameters here

np.random.seed(42) # for reproducibility of results, feel free to comment this out!

freq = 512  # units in Hz
t_min = -0.2  # or, -200 ms
t_max = 1.3  # or, 1300 ms
times = np.linspace(t_min, t_max, int(freq * (t_max - t_min)))

electrodes = ["Fz", "FCz", "Cz", "CPz", "Pz"] # considering the midline electrodes only

# background EEG noise parameters

noise_sd = 0.25  # units in microvolts
baseline_drift_sd = noise_sd/2

# defining variations in EEG ACCORDING TO STIMULI/TRIAL - assuming that EEG is recorded at a singular point for each stimulus.

# import any list by changing the parameters here - it just has to be a list that exists :)
list_type = 'A' # can be either A, B, C, or D
filename = 'List' + list_type + '.csv'
trials = pd.read_csv(filename)
n_trials = trials.shape[0]

"""
The type of error (which can be Deletion, Insertion or both for criticals)
and the number of errors (which can be 0, 1, or 2 - 0 meaning we're looking at a fully plausible/normal case)
are the main factors that will influence the ERP shape.
There will also be variations depending on the electrode and time since word onset.
"""

# ERP amplitude, polarity, and and electrode scaling by error type
# modelled after existing data

error_type_params = {
'Deletion': 
    {'amplitude': 3.0, # in microvolts
    'polarity': -1, # sustained negativity
    'electrode_scaling': {'Fz': 2.0, 'FCz': 2.0, 'Cz': 1.5, 'CPz': 1.0, 'Pz': 1.0}, # electrode dependent scaling factors
    'time_scaling': {(0.3, 0.5): 3.0}, # time period dependent scaling factors, time measured in seconds
    },
'Insertion':
    {'amplitude': 2.5, 
    'polarity': 1, # sustained positivity
    'electrode_scaling': {'Fz': 1.5, 'FCz': 1.5, 'Cz': 1.5, 'CPz': 1.0, 'Pz': 1.0}, 
    'time_scaling': {(0.5, 0.7): 3.0, (0.7, 0.9): 3.0, (0.9, 1.1): 3.0} 
    },
'Deletion+Insertion':
    {'amplitude': 3.5,
     'polarity': 1, # increased sustained positivity
     'electrode_scaling': {'Fz': 1.5, 'FCz': 1.5, 'Cz': 1.5, 'CPz': 1.0, 'Pz': 1.0},
     'time_scaling': {(0.5, 0.7): 3.0, (0.7, 0.9): 3.0, (0.9, 1.1): 3.0},
     },
'Filler':
    {'amplitude': 2.0, 
    'polarity': 1,
    'electrode_scaling': {'Fz': 1.0, 'FCz': 1.0, 'Cz': 0.5, 'CPz': 0.5, 'Pz': 0.5},
    'time_scaling': {(0.5, 0.7): 1.5, (0.7, 0.9): 1.5, (0.9, 1.1): 1.5} 
    },
}

# ERP amplitude scaling factors by number of edits

scaling_factors = {
    0: 1.0,
    1: 2.0,
    2: 3.0,
    }

# function to generate ERP for each stimulus as per the above given parameters

def generate_ERP(times, amplitude, polarity, time_scales):
    """
    About this function:
    Given the parameters of error type and number of edits,
    generate a sustained ERP effect beginning shortly after onset,
    with a spike between 100-300 ms and between 700-900 ms
    """
    onset = 0.0  # the onset of the target word being recorded as 0 ms
    
    sustain = np.zeros_like(times) # creating an array of zeroes of the same size as "times"
    sustain[times >= onset] = amplitude * polarity
    # for time_period in time_scales.keys(): # retrieving scaling factors for specific time periods as defined in error_type_params
        # multiplying values of sustain which fall within the given time period by their respective scaling factor
        # sustain[(times >= time_period[0]) & (times <= time_period[-1])] *= time_scales[time_period]
    """
    In the above code (now commented out), I'd intended to also recreate the dependency
    of ERP amplitude on the amount of time since word onset, which is distinct for the various
    experimental conditions, but it seemed ultimately to complicate the main objective,
    which was to replicate the sustained and spike components of the ERP.
    Maybe another time. :)
    
    Used AI assistance for the below code, mainly for recreating various ERP shapes,
    such as the characteristic smooth ramp upto the sustained patterns that we see,
    and the early and late positive spikes that I also wanted to simulate,
    as is typical for these stimuli.
    """
    ramp = np.clip((times - onset) / 0.1, 0, 1)
    sustain *= ramp # to ensure a smooth ramp up from 0 to the sustained ERP
    
    def gaussian(times, center, width, height):
        return height * np.exp(-0.5 * ((times - center) / width) ** 2)
    """
    The main challenge I faced here was how to confine a gaussian distribution of values
    only around a certain time point. The defined function above was the AI generated solution:
    returning values of the amplitude that would be CENTRED around the defined time point, as well
    as the defined standard deviation/spike duration.
    """
    # early positive spike (100–300 ms)
    early_pos = gaussian(
        times, 
        center=0.2,     # 200 ms 
        width=0.05,     # 50 ms
        height=0.5*amplitude
        )

    # late positive spike (700–900 ms)
    late_pos = gaussian(
        times,
        center=0.8,     # 800 ms
        width=0.07,     # 70 ms
        height=0.6*amplitude
        )
    
    # adding the sustained as well as the spike components to the final simulated signal
    erp = sustain + early_pos + late_pos
    return erp

# function to take stimulus data from each trial and generate an ERP accordingly
# thus simulating EEG data for ONE TRIAL

def simulate_trial(trial):
    """
    About this function:
    Simulate EEG data for one trial, consisting of one sentence/stimulus,
    at one word position only, for multiple electrodes.
    Structure:
    trial_data[electrode] for electrode in electrodes
    """
    trial_data = {}

    error_type = trial['Error Type']
    edit_type = trial['Edits']
    params = error_type_params[error_type]
    scale_factor = scaling_factors[edit_type]

    for electrode in electrodes:
        
        # Background noise
        noise = np.random.normal(0, noise_sd, size=len(times))

        # Baseline drift
        drift = np.cumsum(np.random.normal(0, baseline_drift_sd, size=len(times))) / freq

        # ERP signal
        amplitude = (
            params['amplitude'] * 
            params['electrode_scaling'][electrode] *
            scale_factor * 
            np.random.normal(1.0, 0.1) # random noise component
        )

        erp = generate_ERP(
            times,
            amplitude=amplitude,
            polarity=params['polarity'],
            time_scales=params['time_scaling']
        )

        # for the current electrode, adding the components of the simulated signal
        trial_data[electrode] = noise + drift + erp

    return trial_data


# assembling the full dataset; i.e., with data for each stimuli
# structure: EEG_data[trial_id][electrode] for electrode in electrodes

EEG_data = {}

for inx in range(n_trials):
    trial = trials.iloc[inx]
    trial_id = trial['Item'] # to identify stimulus by item number
    EEG_data[trial_id] = simulate_trial(trial)

# plotting the simulated data - per sentence, per electrode
"""
This serves as a visualizer for the simulated data.
It has been throwing up a memory error, though, but that may just be an issue with my own PC
as it is running low on memory right now. 
Just a heads-up in case you also encounter this error. :(
"""

for inx in range(n_trials):
    
    trial = trials.iloc[inx]
    trial_id = trial['Item']
    error_type = trial['Error Type']
    edit_type = trial['Edits'] 

    fig, axes = plt.subplots(len(electrodes), 1, figsize=(8, 10), sharex=True)
    
    fig.suptitle(
        f"Item {trial_id} | Error Type: {error_type} | Number of Edits: {edit_type}",
        fontsize=14)

    for ax, electrode in zip(axes, electrodes):
        ax.plot(times * 1000, EEG_data[trial_id][electrode]) # times were originally defined in milliseconds
        ax.axvline(0, linestyle="--")
        ax.set_yticks(np.arange(-10, 10, 2))
        ax.set_ylabel(f"{electrode} (µV)")
        # ax.invert_yaxis()

    axes[-1].set_xlabel("Time from error onset (ms)")
    axes[-1].set_xticks(np.arange(0, 1300, 100))
    plt.tight_layout()
    plt.show()
