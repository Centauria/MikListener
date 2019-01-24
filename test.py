import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import struct

SAMPLE_RATE = 44100
FFT_POINT=4096
FRAME = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
MAXINT = 2 ** 15


class Visualizer:
	def __init__(self, range_y=(-1, 1)):
		self.figure = plt.figure('Waveform')
		plt.ion()
		self.range_y = range_y

	def plot(self, data: np.array, sample_rate=SAMPLE_RATE):
		if data.shape[0] == 1 or len(data.shape) == 1:
			plt.plot(np.arange(data.shape[-1]) / sample_rate, data[0,:])
			plt.ylim(*self.range_y)
		else:
			channels = data.shape[0]
			for i in range(channels):
				plt.subplot(channels, 1, i + 1)
				plt.plot(np.arange(data.shape[-1]) / sample_rate, data[i, :])
				plt.ylim(*self.range_y)
		plt.show()

	def spectrum(self, data: np.array, sample_rate=SAMPLE_RATE):
		if data.shape[0] == 1 or len(data.shape) == 1:
			spec=np.fft.fft(data[0,:]*np.hanning(len(data)),FFT_POINT)
			log_spec=10*np.log10(np.abs(spec[0:int(len(spec)/2)]))
			plt.plot(np.linspace(0,SAMPLE_RATE/2,len(log_spec)),log_spec)
			plt.ylim(-30,30)
		else:
			channels=data.shape[0]
			for i in range(channels):
				plt.subplot(channels,1,i+1)
				spec=np.fft.fft(data[i,:]*np.hanning(len(data)),FFT_POINT)
				log_spec=10*np.log10(np.abs(spec[0:int(len(spec)/2)]))
				plt.plot(np.linspace(0,SAMPLE_RATE/2,len(log_spec)),log_spec)
				plt.ylim(-30,30)
		plt.show()


if __name__ == '__main__':
	v = Visualizer()
	x = np.arange(FRAME)
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=SAMPLE_RATE,
                 # input_device_index=0,
                 input=True,
                 frames_per_buffer=FRAME)
	stream.start_stream()
	try:
		while True:
			y = stream.read(FRAME)
			data = np.array(struct.unpack('h' * (len(y) // 2), y))
			data = data.reshape(-1, CHANNELS).T / MAXINT
			v.spectrum(data)
			plt.pause(0.01)
			plt.clf()
	except KeyboardInterrupt:
		plt.ioff()
		plt.close()
		pass
	finally:
		stream.stop_stream()
		stream.close()
		p.terminate()
