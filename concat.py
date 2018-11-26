## File Will concat the the JSON files together
from glob import glob
import json as js

def get_files(path="./Data/Partition*.json", debug=0):
	""" 
	Will glob the data directory for files based
	on path parameter, concat them together and return
	"""
	
	# initialize
	raw = None
	i = 0

	# For every file
	for path in glob(path):
		if debug == 1:
			if i == 3:
				break
			else:
				i += 1

		# Open the file
		with open(path, encoding='utf8') as f:
			# Load the file
			print("Adding Path: " + path)
			if raw == None:
				raw = js.load(f)
			else:
				temp = js.load(f)
				raw = {**raw, **temp}

				# Close the stream
				f.close()

	if debug == 1:
		print("Length: ", len(raw))
		print("type: ", type(raw))

	# Return
	return raw
def get_sample(raw):
	row = raw.sample(1)