import numpy as np
import scipy


def draw_signal_in_time_domain(plot, signal, sample_rate):
    """
    Draw a signal in the time domain on the given plot.

    :param plot: The matplotlib axis to draw on.
    :param signal: The signal to draw.
    :param sample_rate: The sample rate of the signal, in Hz.
    """
    time = [i / sample_rate for i in range(len(signal))]
    plot.plot(time, signal)
    plot.set_xlabel("Time (s)")
    plot.set_ylabel("Amplitude")


def draw_signal_in_frequency_domain(
    plot, signal, sample_rate, max_frequency, max_magnitude
):
    """
    Draw a signal in the frequency domain on the given plot.

    :param max_magnitude: The maximum magnitude to display in the plot.
    :param plot: The matplotlib axis to draw on.
    :param signal: The signal to draw.
    :param sample_rate: The sample rate of the signal, in Hz.
    :param max_frequency: The maximum frequency to display in the plot.
    """

    plot.set_xlabel("Frequency (Hz)")
    plot.set_ylabel("Magnitude")
    plot.set_xlim(0, max_frequency)

    if len(signal) == 0:
        return

    frequency_spectrum = scipy.fft.rfft(signal)
    frequencies = scipy.fft.rfftfreq(len(signal), d=1 / sample_rate)

    if max_frequency is not None:
        frequencies = frequencies[frequencies <= max_frequency]
        frequency_spectrum = frequency_spectrum[: len(frequencies)]

    plot.plot(frequencies, abs(frequency_spectrum))
    plot.set_ylim(0, max_magnitude)


def draw_segment_in_frequency_domain(
    plot, signal, sample_rate, max_frequency, max_magnitube, start_time, segment_length
):
    """
    Draw a segment of a signal in the frequency domain on the given plot.

    :param plot: The matplotlib axis to draw on.
    :param signal: The signal to draw.
    :param sample_rate: The sample rate of the signal, in Hz.
    :param max_frequency: The maximum frequency to display in the plot.
    :param start_time: The start time of the segment to draw.
    :param segment_length: The length of the segment to draw.
    """
    start_index = int(start_time * sample_rate)
    end_index = min(start_index + int(segment_length * sample_rate), len(signal))
    segment = signal[start_index:end_index]
    draw_signal_in_frequency_domain(
        plot, segment, sample_rate, max_frequency, max_magnitube
    )


def draw_filter_coefficients(
    filter_coefficients,
    sample_rate,
    impulse_response_plot,
    frequency_response_plot,
    phase_response_plot,
    max_frequency=None,
):
    """
    Draw the filter coefficients on the given plots.

    :param max_frequency: The maximum frequency to display in the plots.
    :param filter_coefficients: The filter coefficients to draw.
    :param sample_rate: The sample rate of the signal, in Hz.
    :param impulse_response_plot: The matplotlib axis to draw the impulse response on.
    :param frequency_response_plot: The matplotlib axis to draw the frequency response on.
    :param phase_response_plot: The matplotlib axis to draw the phase response on.
    """
    sample_indices = range(len(filter_coefficients))
    impulse_response_plot.stem(sample_indices, filter_coefficients, markerfmt="")
    impulse_response_plot.set_xlabel("Sample")
    impulse_response_plot.set_ylabel("Amplitude")

    angular_frequencies, frequency_response = scipy.signal.freqz(
        filter_coefficients, worN=2000
    )
    frequencies = 0.5 * sample_rate * angular_frequencies / np.pi
    frequency_response_plot.plot(frequencies, 20 * np.log10(abs(frequency_response)))
    frequency_response_plot.set_xlabel("Frequency (Hz)")
    frequency_response_plot.set_ylabel("Magnitude")
    if max_frequency is not None:
        frequency_response_plot.set_xlim(0, max_frequency)

    phase_response_plot.plot(frequencies, np.unwrap(np.angle(frequency_response)))
    phase_response_plot.set_xlabel("Frequency (Hz)")
    phase_response_plot.set_ylabel("Phase (radians)")
    if max_frequency is not None:
        phase_response_plot.set_xlim(0, max_frequency)
