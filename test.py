import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import struct

SAMPLE_RATE = 16000
FRAME = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
MAXINT = 2 ** 15


class Visualizer:
	def __init__(self, range_y=(-1, 1)):
		self.figure = plt.figure('Waveform')
		plt.ion()
		self.range_y = range_y
	
	def plot(self, data: np.array, sample_rate=SAMPLE_RATE):
		if data.shape[0] == 1 or len(data.shape) == 1:
			plt.plot(np.arange(data.shape[-1]) / sample_rate, data[0, :])
			plt.ylim(*self.range_y)
		else:
			channels = data.shape[0]
			for i in range(channels):
				plt.subplot(channels, 1, i + 1)
				plt.plot(np.arange(data.shape[-1]) / sample_rate, data[i, :])
				plt.ylim(*self.range_y)
		plt.show()


if __name__ == '__main__':
	v = Visualizer()
	x = np.arange(FRAME)
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=SAMPLE_RATE,
					input=True,
					frames_per_buffer=FRAME)
	stream.start_stream()
	try:
		while True:
			y = stream.read(FRAME)
			data = np.array(struct.unpack('h' * (len(y) // 2), y))
			data = data.reshape(-1, CHANNELS).T / MAXINT
			v.plot(data)
			plt.pause(0.01)
			plt.clf()
	except KeyboardInterrupt:
		plt.ioff()
		pass
	finally:
		stream.stop_stream()
		stream.close()
		p.terminate()
