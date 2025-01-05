import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import kaiserord, firwin, freqz, lfilter

def record(sample_rate, duration):
    """
    Record audio for a given duration at a given sample rate.

    :param sample_rate: The sample rate of the recording, in Hz.
    :param duration: The duration of the recording, in seconds.
    :return: A mono-channel NumPy array with the recorded audio data.
    """
    recording = sd.rec(int(sample_rate * duration), channels=1, samplerate=sample_rate)
    sd.wait()
    recording = recording.flatten()
    return recording

def play(recording, sample_rate, start_time=0):
    """
    Play a recording at a given sample rate, optionally starting from a given time.

    :param recording: A 2-dimensional NumPy array with the recorded audio data.
    :param sample_rate: The sample rate of the recording, in Hz.
    :param start_time: The time at which to start playing the recording, in seconds.
    """
    sd.play(recording[int(start_time * sample_rate):], sample_rate)

def stop():
    """
    Stop any ongoing audio playback or recording.

    This function stops all streams being played or recorded by the sounddevice library.
    """
    sd.stop()

def save(recording, filename, sample_rate):
    """
    Save a recording to a WAV file.

    :param sample_rate: The sample rate of the recording, in Hz.
    :param recording: A 2-dimensional NumPy array with the recorded audio data.
    :param filename: The path to the file to save the recording to.
    """
    sf.write(filename, recording, sample_rate)

def get_filter_coefficients(sample_rate, cutoff_frequency=3400, transition_band=200, stopband_attenuation_db=40):
    """
    Calculate the coefficients of a low-pass FIR filter with a given sample rate and cutoff frequency.

    :param sample_rate: The sample rate of the recording, in Hz.
    :param cutoff_frequency: The frequency at which the filter should cut off, in Hz.
    :param transition_band: The width of the transition band, in Hz.
    :param stopband_attenuation_db: The desired attenuation in the stopband, in decibels.
    :return: A 1-dimensional NumPy array with the coefficients of the filter.
    """
    nyquist_rate = sample_rate / 2  # Nyquist rate
    normalized_cutoff = cutoff_frequency / nyquist_rate
    transition_width = transition_band / nyquist_rate

    # Calculate the filter order and Kaiser window beta for the desired attenuation
    filter_order, beta = kaiserord(stopband_attenuation_db, transition_width)

    # Ensure filter order is odd to avoid phase distortion
    if filter_order % 2 == 0:
        filter_order += 1

    # Calculate the filter coefficients using the Kaiser window
    filter_coefficients = firwin(filter_order, normalized_cutoff, window=("kaiser", beta))

    return filter_coefficients


def sound_filter(recording, filter_coefficients):
    """
    Apply a FIR filter to a recording.

    :param recording: A 1D or 2D NumPy array with the recorded audio data.
    :param filter_coefficients: The coefficients of the FIR filter to apply.
    :return: A 1D or 2D NumPy array with the filtered audio data.
    """
    if recording.ndim == 1:
        return lfilter(filter_coefficients, [1], recording)
    elif recording.ndim == 2:  # Stereo or multi-channel
        return np.array(
            [lfilter(filter_coefficients, [1], channel) for channel in recording.T]
        ).T
    else:
        raise ValueError("Recording must be 1D or 2D array.")