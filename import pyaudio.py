import tkinter as tk
import pyaudio
import numpy as np
import matplotlib.pyplot as plt

# Constants for audio capture
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Initialize PyAudio for audio capture
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Create a function to update the audio display
def update_audio_display():
    data = stream.read(CHUNK)
    audio_data = np.frombuffer(data, dtype=np.int16)
    
    # Process audio_data (in this case, plot the waveform)
    plt.clf()
    plt.plot(audio_data)
    plt.title("Audio Waveform")
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
    plt.pause(0.1)
    
    # Schedule the function to run again
    root.after(10, update_audio_display)

# Create a new window
root = tk.Tk()
root.title("Audio Capture and Display")

# Start updating the audio display
update_audio_display()

# Start the main event loop
root.mainloop()

# Close the audio stream and terminate PyAudio when done
stream.stop_stream()
stream.close()
p.terminate()
