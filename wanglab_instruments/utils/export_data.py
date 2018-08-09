import numpy as np
import matplotlib.pyplot as plt

def save_xy(save_to, x_data, y_data, plot = True):
	# x_data: numpy array of x-axis
	# y_data: either numpy array of single y-data, or list of multiple numpy
	# arrays of y-data
	if type(y_data).__name__ == 'list':	
		if plot:
			fig, ax = plt.subplots(1, figsize = (5, 5) )
			for i in range(len(y_data)):
				ax.plot(x_data, y_data[i])
			fig.tight_layout()
			fig.savefig(save_to + '.png', dpi = 100)
			plt.close(fig)
		np.save(save_to, [x_data, y_data] )
		return 0
	elif type(y_data).__name__ == 'ndarray':
		if plot:
			fig, ax = plt.subplots(1, figsize = (5, 5) )
			ax.plot(x_data, y_data)
			fig.tight_layout()
			fig.savefig(save_to + '.png', dpi = 100)
			plt.close(fig)
		np.save(save_to, [x_data, y_data])
		return 0
	else:
		raise TypeError(
		'y_data of type {} not accepted.  Must be of type list or numpy.ndarray'
			.format(type(y_data).__name__))

def save_text(save_to, text):
	with open(save_to, 'w') as f:
		f.write(text)
	return 0

