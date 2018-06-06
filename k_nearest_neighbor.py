# This script prepares the training data, then builds a knn model, and tests it
import pandas as pd
from sklearn.utils import shuffle
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# Read in financial data
data = pd.read_csv('SP500_financial_data.csv', index_col = False)

# Remove outliers
index = data.index[data['Name'] == 'Salesforce.com'].tolist()
data = data.drop(index)

# Remove classes with insufficient data
index = data.index[data['Sector'] == 'Telecommunication Services']
data = data.drop(index)
index = data.index[data['Sector'] == 'Financials']
data = data.drop(index)
index = data.index[data['Sector'] == 'Real Estate']
data = data.drop(index)

# Encode categories
le = preprocessing.LabelEncoder()
le.fit(data['Sector'])
data['Sector Encoded'] = le.transform(data['Sector'])

# Seperate the data into 70% training and 30% validation data sets
accuracy_array = []
for i in range(10):
	data = shuffle(data)
	cutoff = int(len(data)*0.8) 
	training_data = data.iloc[0: cutoff]
	test_data = data.iloc[cutoff:len(data)]

	# Use all 12 features
	#X_train = training_data[['ROE','ROA','PB_ratio','PE_ratio','Net_margin','Asset_turn',\
	#	'Div_payout_ratio','LT_debt_to_equity','Equity_to_assets','Current_ratio','Div_yield','Capex_to_revenue']]
	#X_test = test_data[['ROE','ROA','PB_ratio','PE_ratio','Net_margin','Asset_turn',\
	#	'Div_payout_ratio','LT_debt_to_equity','Equity_to_assets','Current_ratio','Div_yield','Capex_to_revenue']]
	
	# Use fewer features
	X_train = training_data[['ROE','ROA','PB_ratio','Asset_turn',\
		'LT_debt_to_equity','Equity_to_assets','Current_ratio','Div_yield','Capex_to_revenue']]
	X_test = test_data[['ROE','ROA','PB_ratio','Asset_turn',\
		'LT_debt_to_equity','Equity_to_assets','Current_ratio','Div_yield','Capex_to_revenue']]

	# Labels
	Y_train = training_data['Sector Encoded']
	Y_test = test_data['Sector Encoded']

	# Create K nearest neighbor model
	n_neighbors = 3
	neigh = KNeighborsClassifier(n_neighbors = n_neighbors)
	neigh.fit(X_train, Y_train)
	Y_predict = neigh.predict(X_test)

	# Compute accuracy of model
	n_correct = np.sum(Y_predict == Y_test)
	accuracy = n_correct / len(Y_predict)
	print('Accuracy of K = ' +str(n_neighbors) + ' nearest neighbors: ' + str(accuracy)[0:5])
	accuracy_array.append(accuracy)
print('Accuracy of K = ' + str(n_neighbors) + ' nearest neighbors, average of 10 cross validations: ' + str(np.mean(accuracy_array))[0:5])