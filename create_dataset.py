## Will create a pandas data frame from the dictionary of dictionaries
import pandas as pd
import numpy as np
from datetime import datetime

def convert_to_dataframe(window_size, raw, sections=48):
	"""
	Converts the dict of dicts that is raw data into a pandas data frame
	"""
	# Declare variables
	columns = ["hashtag"]
	index = 0

	# Add column for days, each day has 8 sections to minimize dataset
	for i in range(window_size):
		for j in range(sections):
			columns.append("day_" + str(i) + "_" + str(j) + "_retweets")
			columns.append("day_" + str(i) + "_" + str(j) + "_followers")


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

			# Fill in each time for this row
			for index in range(count):
				# get the number of retweets
				retweets = raw[hashtag]["day" + str(day)]['retweet_count'][index]
				# get the number of followers
				followers = raw[hashtag]["day" + str(day)]['followers_count'][index]
				# get the date created
				date = raw[hashtag]["day" + str(day)]['created_at'][index]
				date = datetime.strptime(date, '%a %b %d %X %z %Y')
				section = (date.hour % sections)
				# Figure out into which column this information goes in
				row["day_" + str(day) + "_" + str(section) + "_retweets"][0] += retweets
				row["day_" + str(day) + "_" + str(section) + "_followers"][0] += followers

		# For every other day for this hashtag
		aggregate = 0
		
		# Sum the number of occurrences for each hashtag
		for day in range(window_size, 7):
			aggregate += raw[hashtag]["day" + str(day)]['occurrences']

		# Add aggregate to the ids
		ids.append(aggregate)

		# Append to the frame
		temp_list.append(row)

	# Concat the frames together
	frame = pd.concat(temp_list, ignore_index=True)

	# Make if an numpy array
	ids = np.array(ids)

	# Return the Dataframe with ids
	return frame, ids
