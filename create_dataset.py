## Will create a pandas data frame from the dictionary of dictionaries
import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats

def convert_to_dataframe(window_size, raw, save_to_file=True, get_from_file=True, path="./Data/Concat.csv"):
	"""
	Converts the dict of dicts that is raw data into a pandas data frame
	"""

	# get from file if true
	if get_from_file:
		try:
			frame = pd.read_csv(path)
		except:
			frame = pd.DataFrame(data=[])
		print("Reading frame of length: " , len(frame))
		print("Reading frame with # columns: ", len(frame.columns))
		if len(frame) != len(raw) or len(frame.columns) == (2 + window_size * 8):
			print("Expecting frame of size: ", len(raw))
			print("Running script...")
		else:
			ids = frame["ids"].values
			frame.drop(columns="ids")
			return frame, ids


	# Declare variables
	columns = ["hashtag"]
	index = 0

	# Add column for days, each day has 8 sections to minimize dataset
	for i in range(window_size):
		columns.append("day_" + str(i) + "_retweets")
		columns.append("day_" + str(i) + "_followers")
		columns.append("day_" + str(i) + "_occurences")
		columns.append("day_" + str(i) + "_weekday")
		columns.append("day_" + str(i) + "_month")
		columns.append("day_" + str(i) + "_day")
		columns.append("day_" + str(i) + "_modehour")
		columns.append("day_" + str(i) + "_avghour")
	
	print("Number of columns of new dataset: ", len(columns))
	print("Number of hashtags: ", len(raw))


	# Make an empty dataframe and label ids
	temp_list = []
	ids = []

	# Iterate over every hashtag
	for hashtag	in raw:
		# Start empty dataframe for this hashtag
		row = pd.DataFrame(columns=columns, data=[])
		blank = [0] * len(columns)
		blank = pd.Series(blank, index=columns)
		row = row.append(blank, ignore_index=True)
		row["hashtag"][0] = hashtag

		# iterate over each day
		for day in range(window_size):
			# declare local variables
			count = raw[hashtag]["day" + str(day)]['occurrences']
			row["day_" + str(day) + "_occurences"][0] = count
			hours = [0]
			# Fill in each time for this row
			for index in range(count):
				# get the number of retweets
				row["day_" + str(day) + "_retweets"][0] += raw[hashtag]["day" + str(day)]['retweet_count'][index]
				# get the number of followers
				row["day_" + str(day) + "_followers"][0] += raw[hashtag]["day" + str(day)]['followers_count'][index]
				# get the date created
				date = raw[hashtag]["day" + str(day)]['created_at'][index]
				date = datetime.strptime(date, '%a %b %d %X %z %Y')
				hours.append(date.hour)
				if index == 0:
					row["day_" + str(day) + "_weekday"][0] = date.weekday()
					row["day_" + str(day) + "_month"][0] = date.month
					row["day_" + str(day) + "_day"][0] = date.day
			
			# Fill out avg hour and mode hour
			row["day_" + str(day) + "_modehour"][0] = stats.mode(hours, axis=0)[0][0]
			row["day_" + str(day) + "_avghour"][0] = np.mean(hours)

		# For every other day for this hashtag
		aggregate = 0
		
		# Sum the number of occurrences for each hashtag
		for day in range(window_size, 7):
			aggregate += raw[hashtag]["day" + str(day)]['occurrences']

		# Add aggregate to the ids
		ids.append(aggregate)

		# Append to the frame
		temp_list.append(row)

		print("Completed: ", hashtag)

	# Concat the frames together
	frame = pd.concat(temp_list, ignore_index=True)

	# Make if an numpy array
	ids = np.array(ids)

	# Save this to file, so that this does not need to be run later
	if save_to_file:
		copy = frame.copy()
		copy["ids"] = ids
		copy.to_csv(path, encoding='utf-8', index=False)

	# Return the Dataframe with ids
	return frame, ids
