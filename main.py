# Created by Carlos Leon
# Data is from Carlos Leon, Femi, Andres, and Logan

## Setup
# import libraries
import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.svm import SVR
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import r2_score
from sklearn.metrics import explained_variance_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import learning_curve

# import local files
import concat as cat
import save_results as sr
import create_dataset as cd
import outlier_detection as od

# global Variables
DEBUG = 1
WINDOW_SIZE = 6
FOLD_SIZE = 5
PARAMETERS = {"kernel": ["rbf"], "C": [1,10,10,100,1000], "gamma": [1e-8, 1e-6, 1e-5, 1e-4, 1e-2, 1e-1, 'scale', 'auto']}

## Acquire Data
# get raw data
raw_data = cat.get_files(debug=DEBUG)

# transform into dataset
dataset, dataset_ids = cd.convert_to_dataframe(WINDOW_SIZE, raw_data)
hashtags = dataset["hashtag"]
dataset = dataset.drop(columns ="hashtag", axis=1)

## Build a classifier
# Declare variables
kf = KFold(n_splits=FOLD_SIZE, shuffle=True)
clf = GridSearchCV(SVR(), PARAMETERS, cv=5, verbose=0)
rs = RobustScaler()
total_accuracy = 0
r2 = 0
score_avg = 0
rows_kept = 0
len_train = 0
predictions = []
truths = []

# Perform k-folds cross validation
for train, test in kf.split(dataset	, dataset_ids):

	# Get testing data and training data
	training = dataset.values[train, :]
	training_ids = dataset_ids[train]

	# remove outliers
	count = len(train)
	training, training_ids, count = od.remove_outliers(training, training_ids)

	# Scale features
	training = rs.fit_transform(training)

	# Train the classifier
	if DEBUG == 1:
		print("Training on data length: ", len(training))
		print("ids length: ", len(training_ids))
		
	clf.fit(training, training_ids)
	
	# Get the model score
	score = clf.score(training, training_ids)
	score_avg += score
	print("Score of model: ", score)

	# Test over testing
	for i in range(len(test)):
		# Get query and label
		query = dataset.values[test[i], :].reshape(1, -1)
		label = dataset_ids[test[i]]

		# scale the query
		query = rs.transform(query)

		# predict query
		p = clf.predict(query)
		predictions.append(p[0])
		truths.append(label)

	# calculate fold accuracy
	fold_accuracy = explained_variance_score(truths, predictions)
	temp_r2 = r2_score(truths, predictions)
	total_accuracy += fold_accuracy
	r2 += temp_r2
	rows_kept += count
	len_train = len(train)

	if DEBUG == 1:
		print("Fold accuracy: ", fold_accuracy)
		print("Truths: ", len(truths))
		print("Predictions: ", len(predictions))
		print("Running total accuracy: ", total_accuracy)
		print("Fold Accuracy: ", fold_accuracy)
		print("Running count of rows kept: ", rows_kept)

## Calculate results
# Calculate total accuracy
total_accuracy = total_accuracy / FOLD_SIZE
r2 = r2 / FOLD_SIZE
score_avg = score_avg / FOLD_SIZE
rows_kept = rows_kept / FOLD_SIZE
print("Accuracy: ", total_accuracy)

sr.plot_learning_curve(clf, "Learning Curve", dataset, dataset_ids, n_jobs=4)
plt.savefig('./Results/' + str(WINDOW_SIZE) + '_learning_curve.png', bbox_inches='tight')

# save results
sr.save_results(WINDOW_SIZE, total_accuracy, r2, score_avg, rows_kept, len_train)
sr.plot_observed_vs_fitted(truths, predictions, WINDOW_SIZE)

plt.show()
