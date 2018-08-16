import numpy as np
import matplotlib.pyplot as plt
from helpers import timestamp

def save_xy(x_data, y_data, save_to = '', time_stamp = True, plot = True):

	# x_data: numpy array of x-axis
	# y_data: either numpy array of single y-data, or list of multiple numpy
	# arrays of y-data
	# When save_to is empty, saved data will be named by the time_stamp. 

	if save_to == '' and not time_stamp:
		message = (' save_xy(x_data, y_data, save_to = \'\', '
			+ 'time_stamp = True, plot = True)\n'
			+ '      --->  '
			+ 'Empty save_to and time_stamp = False.  Nothing to name file.')
		raise Exception(message)

	if type(y_data).__name__ == 'list':	
		if plot:
			fig, ax = plt.subplots(1, figsize = (5, 5) )
			for i in range(len(y_data)):
				ax.plot(x_data, y_data[i])
			fig.tight_layout()
			if time_stamp:
				fig.savefig(save_to + timestamp() + '.png', dpi = 100)
			else:
				fig.savefig(save_to + '.png', dpi = 100)
			plt.close(fig)
		np.save(save_to + timestamp(), [x_data, y_data] )
		return 0

	elif type(y_data).__name__ == 'ndarray':
		if plot:
			fig, ax = plt.subplots(1, figsize = (5, 5) )
			ax.plot(x_data, y_data)
			fig.tight_layout()
			if time_stamp:
				fig.savefig(save_to + timestamp() + '.png', dpi = 100)
			else:
				fig.savefig(save_to + '.png', dpi = 100)
			plt.close(fig)
		np.save(save_to + timestamp(), [x_data, y_data])
		return 0

	else:
		raise TypeError(
		'y_data of type {} not accepted.  Must be of type list or numpy.ndarray'
			.format(type(y_data).__name__))

def save_text(save_to, text):
	with open(save_to, 'w') as f:
		f.write(text)
	return 0

if __name__ == '__main__':
	x = np.linspace(0,1,1000)
	y = x**2
	save_xy(x,y,time_stamp = False)
