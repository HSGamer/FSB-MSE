import threading
import time

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from audio_lib import record, stop, sound_filter, get_filter_coefficients, play, save
from graph_lib import (
    draw_signal_in_time_domain,
    draw_signal_in_frequency_domain,
    draw_segment_in_frequency_domain,
    draw_filter_coefficients,
)

SAMPLE_RATE = 44100

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audio Analyzer")
        self.geometry("800x600")

        self.recording = None
        self.filtered_recording = None
        self.filter_coefficients = None
        self.duration = tk.IntVar(value=5)
        self.current_time = tk.DoubleVar(value=0)
        self.filter_frequency = tk.IntVar(value=3000)
        self.transition_band = tk.IntVar(value=200)
        self.attenuation = tk.IntVar(value=40)
        self.max_frequency = tk.IntVar(value=10000)
        self.max_magnitude = tk.DoubleVar(value=1)
        self.playing = tk.BooleanVar(value=False)
        self.play_filtered = tk.BooleanVar(value=False)

        self.time_domain_plot = None
        self.time_domain_plot_canvas = None
        self.frequency_domain_plot = None
        self.frequency_domain_plot_canvas = None
        self.realtime_frequency_domain_plot = None
        self.realtime_frequency_domain_plot_canvas = None
        self.impulse_response_plot = None
        self.impulse_response_plot_canvas = None
        self.frequency_response_plot = None
        self.frequency_response_plot_canvas = None
        self.phase_response_plot = None
        self.phase_response_plot_canvas = None

        self.time_scale = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.current_time.trace_add("write", self.on_current_time_changed)
        self.play_filtered.trace_add("write", self.on_play_filtered_changed)
        self.filter_frequency.trace_add("write", self.on_filter_changed)
        self.transition_band.trace_add("write", self.on_filter_changed)
        self.attenuation.trace_add("write", self.on_filter_changed)
        self.max_frequency.trace_add("write", self.on_frequency_domain_setting_changed)
        self.max_magnitude.trace_add("write", self.on_frequency_domain_setting_changed)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_widgets()
        self.create_plots()
        self.update_time_domain_plot()
        self.update_frequency_domain_plot()
        self.update_realtime_frequency_domain_plot()

        self.on_filter_changed()

    def create_widgets(self):
        playback_frame = ttk.Frame(self)
        playback_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        playback_frame.grid_rowconfigure(1, weight=1)

        duration_frame = ttk.Frame(playback_frame)
        duration_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        duration_frame.grid_columnconfigure(0, weight=1)
        duration_label = ttk.Label(duration_frame, text="Duration (s):")
        duration_label.grid(row=0, column=0, padx=5, pady=5)
        duration_entry = ttk.Entry(duration_frame, textvariable=self.duration)
        duration_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        action_frame = ttk.Frame(playback_frame)
        action_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        record_button = ttk.Button(action_frame, text="Record", command=self.on_record)
        record_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        save_button = ttk.Button(action_frame, text="Save", command=self.on_save)
        save_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        play_button = ttk.Button(action_frame, text="Play", command=self.on_play)
        play_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        stop_button = ttk.Button(action_frame, text="Stop", command=self.on_stop)
        stop_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        filter_frame = ttk.Frame(self)
        filter_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        filter_frame.grid_rowconfigure(0, weight=1)
        filter_frame.grid_columnconfigure(0, weight=1)
        filter_scale = tk.Scale(filter_frame, orient="horizontal", from_=0, to=10000, label="Filter Frequency (Hz):", variable=self.filter_frequency)
        filter_scale.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        transition_scale = tk.Scale(filter_frame, orient="horizontal", from_=0, to=10000, label="Transition Band (Hz):", variable=self.transition_band)
        transition_scale.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        attenuation_scale = tk.Scale(filter_frame, orient="horizontal", from_=0, to=100, label="Attenuation (dB):", variable=self.attenuation)
        attenuation_scale.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        filter_checkbox = ttk.Checkbutton(filter_frame, text="Play Filtered", variable=self.play_filtered)
        filter_checkbox.grid(row=3, column=0, padx=5, pady=5)

    def create_plots(self):
        plot_frame = ttk.Frame(self)
        plot_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        plot_frame.grid_columnconfigure(1, weight=1)
        plot_frame.grid_columnconfigure(2, weight=1)
        plot_frame.grid_rowconfigure(0, weight=1)
        plot_frame.grid_rowconfigure(1, weight=1)
        plot_frame.grid_rowconfigure(2, weight=1)

        time_domain_fig, self.time_domain_plot = plt.subplots(1, 1, figsize=(3, 2))
        self.time_domain_plot_canvas = FigureCanvasTkAgg(time_domain_fig, master=plot_frame)
        self.time_domain_plot_canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        self.time_scale = tk.Scale(plot_frame, orient="vertical", from_=0, to=self.duration.get(), showvalue=False, variable=self.current_time, resolution=0.01)
        self.time_scale.grid(row=0, column=0, sticky="nsew")

        frequency_domain_fig, self.frequency_domain_plot = plt.subplots(1, 1, figsize=(3, 2))
        self.frequency_domain_plot_canvas = FigureCanvasTkAgg(frequency_domain_fig, master=plot_frame)
        self.frequency_domain_plot_canvas.get_tk_widget().grid(row=1, column=1, sticky="nsew")
        max_frequency_scale = tk.Scale(plot_frame, orient="vertical", from_=0, to=30000, showvalue=False, variable=self.max_frequency)
        max_frequency_scale.grid(row=1, column=0, sticky="nsew")
        max_magnitude_scale = tk.Scale(plot_frame, orient="vertical", from_=0, to=20, showvalue=False, variable=self.max_magnitude, resolution=0.01)
        max_magnitude_scale.grid(row=2, column=0, sticky="nsew")

        realtime_frequency_domain_fig, self.realtime_frequency_domain_plot = plt.subplots(1, 1, figsize=(3, 2))
        self.realtime_frequency_domain_plot_canvas = FigureCanvasTkAgg(realtime_frequency_domain_fig, master=plot_frame)
        self.realtime_frequency_domain_plot_canvas.get_tk_widget().grid(row=2, column=1, sticky="nsew")

        impulse_response_fig, self.impulse_response_plot = plt.subplots(1, 1, figsize=(3, 2))
        self.impulse_response_plot_canvas = FigureCanvasTkAgg(impulse_response_fig, master=plot_frame)
        self.impulse_response_plot_canvas.get_tk_widget().grid(row=0, column=2, sticky="nsew")

        frequency_response_fig, self.frequency_response_plot = plt.subplots(1, 1, figsize=(3, 2))
        self.frequency_response_plot_canvas = FigureCanvasTkAgg(frequency_response_fig, master=plot_frame)
        self.frequency_response_plot_canvas.get_tk_widget().grid(row=1, column=2, sticky="nsew")

        phase_response_fig, self.phase_response_plot = plt.subplots(1, 1, figsize=(3, 2))
        self.phase_response_plot_canvas = FigureCanvasTkAgg(phase_response_fig, master=plot_frame)
        self.phase_response_plot_canvas.get_tk_widget().grid(row=2, column=2, sticky="nsew")

    def get_recording(self, show_warning=False, get_filtered=False):
        recording = self.recording
        if get_filtered and self.filtered_recording is not None:
            recording = self.filtered_recording
        if recording is None and show_warning:
            messagebox.showwarning("No Recording", "No recording has been recorded yet.")
        return recording

    def update_time_domain_plot(self):
        self.time_domain_plot.clear()
        self.time_domain_plot.set_title("Time Domain")

        recording = self.get_recording(get_filtered=self.play_filtered.get())
        if recording is not None:
            draw_signal_in_time_domain(self.time_domain_plot, recording, SAMPLE_RATE)
            self.time_domain_plot.axvline(x=self.current_time.get(), color='red', linestyle='--', label='Current Time')

        self.time_domain_plot_canvas.draw()

    def update_frequency_domain_plot(self):
        self.frequency_domain_plot.clear()
        self.frequency_domain_plot.set_title("Frequency Domain")

        recording = self.get_recording(get_filtered=self.play_filtered.get())
        if recording is not None:
            draw_signal_in_frequency_domain(self.frequency_domain_plot, recording, SAMPLE_RATE, self.max_frequency.get(), self.max_magnitude.get())

        self.frequency_domain_plot_canvas.draw()

    def update_realtime_frequency_domain_plot(self):
        self.realtime_frequency_domain_plot.clear()
        self.realtime_frequency_domain_plot.set_title("Realtime Frequency Domain")

        recording = self.get_recording(get_filtered=self.play_filtered.get())
        if recording is not None:
            draw_segment_in_frequency_domain(self.realtime_frequency_domain_plot, recording, SAMPLE_RATE, self.max_frequency.get(), self.max_magnitude.get(), self.current_time.get(), 0.1)

        self.realtime_frequency_domain_plot_canvas.draw()

    def update_filter_frequency_plot(self):
        self.impulse_response_plot.clear()
        self.frequency_response_plot.clear()
        self.phase_response_plot.clear()

        self.impulse_response_plot.set_title("Impulse Response")
        self.frequency_response_plot.set_title("Frequency Response")
        self.phase_response_plot.set_title("Phase Response")

        if self.filter_coefficients is not None:
            draw_filter_coefficients(self.filter_coefficients, SAMPLE_RATE, self.impulse_response_plot, self.frequency_response_plot, self.phase_response_plot, self.max_frequency.get())

        self.impulse_response_plot_canvas.draw()
        self.frequency_response_plot_canvas.draw()
        self.phase_response_plot_canvas.draw()

    def update_filter_frequency(self):
        try:
            self.filter_coefficients = get_filter_coefficients(SAMPLE_RATE, max(1, self.filter_frequency.get()), max(1, self.transition_band.get()), max(1, self.attenuation.get()))
        except Exception as e:
            print(e)
            return

        self.update_filter_frequency_plot()

        recording = self.get_recording()
        if recording is not None:
            self.filtered_recording = sound_filter(recording, self.filter_coefficients)

        self.update_time_domain_plot()
        self.update_frequency_domain_plot()
        self.update_realtime_frequency_domain_plot()

    def on_record(self):
        self.recording = record(SAMPLE_RATE, self.duration.get())
        self.filtered_recording = sound_filter(self.recording, self.filter_coefficients)
        self.time_scale.configure(to=self.duration.get())
        self.current_time.set(0)
        self.update_time_domain_plot()
        self.update_frequency_domain_plot()

    def on_save(self):
        recording = self.get_recording(show_warning=True, get_filtered=self.play_filtered.get())
        if recording is not None:
            save(recording, "recording.wav", SAMPLE_RATE)
            messagebox.showinfo("Saved", "Recording saved successfully!")

    def on_play(self):
        if not self.playing.get():
            if self.current_time.get() >= self.duration.get():
                self.current_time.set(0)

            recording = self.get_recording(show_warning=True, get_filtered=self.play_filtered.get())
            if recording is None:
                return

            self.playing.set(True)

            play(recording, SAMPLE_RATE, self.current_time.get())

            def update_current_time():
                start_value = self.current_time.get()
                start_time = time.time()
                while self.playing.get():
                    current_time = time.time()
                    range_in_seconds = current_time - start_time
                    if start_value + range_in_seconds >= self.duration.get():
                        self.current_time.set(self.duration.get())
                        self.playing.set(False)
                    else:
                        self.current_time.set(start_value + range_in_seconds)
                    time.sleep(0.01)
            threading.Thread(target=update_current_time).start()

    def on_stop(self):
        stop()
        self.playing.set(False)

    def on_current_time_changed(self, *args):
        self.update_time_domain_plot()
        self.update_realtime_frequency_domain_plot()

    def on_filter_changed(self, *args):
        self.update_filter_frequency()

    def on_frequency_domain_setting_changed(self, *args):
        self.update_frequency_domain_plot()
        self.update_realtime_frequency_domain_plot()
        self.update_filter_frequency_plot()

    def on_play_filtered_changed(self, *args):
        self.on_stop()
        self.update_time_domain_plot()
        self.update_frequency_domain_plot()
        self.update_realtime_frequency_domain_plot()

    def on_closing(self):
        self.on_stop()
        self.quit()
        self.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()