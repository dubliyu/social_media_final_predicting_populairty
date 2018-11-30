## File with save the results in the chosen directory
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve

def save_results(window_size, explained, r2, score_avg, rows_kept, total_rows, path="./Results/result.txt"):
	"""
	Writes results out to the specified file
	"""

	# Open the file
	f = open(path, "a+")

	# Write out data
	f.write("-" * 25 + "\nWindow Size: " + str(window_size) + "\n")
	f.write("Explained Variance Score: " + str(explained) + "\n")
	f.write("R2 Score: " + str(r2) + "\n")
	f.write("Model Score: " + str(score_avg) + "\n")
	f.write("Avg Number of rows kept: " + str(rows_kept) + "\t Out of: " + str(total_rows) + "\n")
	f.write("Model Score: " + str(score_avg) + "\n")
	f.write("-" * 25 + "\n\n")

	# If success return true
	return True

def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
						n_jobs=None, train_sizes=np.linspace(.1, 1.0, 5)):
	# Credit to Scikit Learn: plot validation curve page

	plt.figure()
	plt.title(title)
	if ylim is not None:
		plt.ylim(*ylim)
	plt.xlabel("Training examples")
	plt.ylabel("Score")
	train_sizes, train_scores, test_scores = learning_curve(
		estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
	train_scores_mean = np.mean(train_scores, axis=1)
	train_scores_std = np.std(train_scores, axis=1)
	test_scores_mean = np.mean(test_scores, axis=1)
	test_scores_std = np.std(test_scores, axis=1)
	plt.grid()

	plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
					 train_scores_mean + train_scores_std, alpha=0.1,
					 color="r")
	plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
					 test_scores_mean + test_scores_std, alpha=0.1, color="g")
	plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
			 label="Training score")
	plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
			 label="Cross-validation score")

	plt.legend(loc="best")
	return plt

def plot_observed_vs_fitted(real_values, observed_values, window):
	temp = [real_values, observed_values]
	temp = sorted(temp, key=lambda x: x[0])

	y = temp[0]
	x = temp[1]

	plt.xlabel('Actual Occurrences')
	plt.ylabel('Predicted Occurrences')
	plt.scatter(x, y, c='red')
	plt.savefig('./Results/' + str(window) + '_results.png', bbox_inches='tight')

