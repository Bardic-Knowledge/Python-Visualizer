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

def mandelbrot(c, max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return max_iter

def generate_mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter):
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    mandelbrot_set = np.zeros((width, height), dtype=int)

    for i in range(width):
        for j in range(height):
            real = x[i]
            imag = y[j]
            c = complex(real, imag)
            mandelbrot_set[i, j] = mandelbrot(c, max_iter)

    return mandelbrot_set

# Create a function to update the Mandelbrot display based on audio data
def update_mandelbrot_display():
    data = stream.read(CHUNK)
    audio_data = np.frombuffer(data, dtype=np.int16)
    
    # Process audio_data and use it to modify Mandelbrot parameters
    audio_amplitude = np.max(np.abs(audio_data))  # Measure the audio amplitude
    zoom = 1.0 * audio_amplitude / 500.0  # Modify zoom based on audio
    
    # Generate and plot the Mandelbrot set with the modified parameters
    x_min, x_max = -2 / zoom, 1 / zoom
    y_min, y_max = -1 / zoom, 1 / zoom
    mandelbrot_set = generate_mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter)
    
    plt.clf()
    plt.imshow(mandelbrot_set.T, extent=(x_min, x_max, y_min, y_max))
    #plt.xlabel("Real")
    #plt.ylabel("Imaginary")
    #plt.title("Mandelbrot Set")
    plt.pause(0.50)
    
    # Schedule the function to run again
    root.after(10, update_mandelbrot_display)

# Create a new window
root = tk.Tk()
root.title("Audio-Influenced Mandelbrot Viewer")

# Mandelbrot parameters
width = 800
height = 800
max_iter = 16

# Start updating the Mandelbrot display
update_mandelbrot_display()

# Start the main event loop
root.mainloop()

# Close the audio stream and terminate PyAudio when done
stream.stop_stream()
stream.close()
p.terminate()
