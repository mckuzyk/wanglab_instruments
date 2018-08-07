from __future__ import print_function

def print_status(step, num_steps, width = 50):
	progress = int(step*width/num_steps)
	percent_done = int(step*100/num_steps)
	print('[{one:*<{star_len}}{two: >{space_len}}] {percent:0>2}%'.format(
		one = '*',
		two = ' ',
		star_len = progress,
		space_len = width - progress,
		percent = percent_done), end='\r')

if __name__ == '__main__':
	import time
	for i in range(150):
		print_status(i, 150, width=22)
		time.sleep(.01)
