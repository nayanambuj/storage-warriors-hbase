import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import sys

def flightPredictor():
    # Getting the command line parameters
    num_split = int(sys.argv[1])
    train_percent = sys.argv[2].split(',')
    filename = sys.argv[3]
    
    # load data from csv files
    train = np.loadtxt(filename, delimiter=',')

    # use deep copy here to make cvxopt happy
    X = train[:, 1:].copy()
    Y = train[:, 0].copy()

    logisticRegression("RandomForest", "", num_split, train_percent, X, Y)

def logisticRegression(method_name, filename, num_split, train_percent, X, Y):    
    data_split_and_predict(method_name, "Weather-FlightData", X, Y, train_percent, num_split)


def calc_error(predictedY, y_test):
    k = 0
    errors = 0

    while k < len(predictedY):
        if predictedY[k] != y_test[k]:
            errors = errors + 1

        k = k + 1

    errorrate = float(errors) / len(predictedY)
    return errorrate


def data_split_and_predict (method_name, dataset_name, datasetX, datasetY, train_percent, num_split):
    i = 0
    mean_all_runs = list()
    trainpercentmean = {}

    for l in range(len(train_percent)):
        trainpercentmean[int(train_percent[l])] = 0

    print ("Printing statistics for {}".format(dataset_name))

    # Performing 80-20 train test split
    while i < num_split:
        X_train, X_test, y_train, y_test = train_test_split(datasetX, datasetY, test_size=0.2)
        j = 0

        mean_per_run_error = list()

        while (j < len(train_percent)):
            start_index = 0
            train_rate = int(train_percent[j])
            end_index = int((float(train_rate) / 100) * len(X_train))

            miniXslice = X_train[start_index:end_index, 0:]
            miniYslice = y_train[start_index:end_index]


            if method_name == "LogisticRegression":
                #Small Data Setting
                myLR = LogisticRegression(penalty='l2')
                myLR.fit(miniXslice, miniYslice)
                predictedY = myLR.predict(X_test)

                #Large Dataset setting
                # Standarize features
                '''scaler = StandardScaler()
                miniXslice = scaler.fit_transform(miniXslice)
                # Create logistic regression object using sag solver
                myLR = LogisticRegression(random_state=0, solver='sag')
                # Train model
                myLR.fit(miniXslice, miniYslice)
                #predict
                predictedY = myLR.predict(X_test)'''

            if method_name == "RandomForest":
                rf = RandomForestRegressor()
                rf.fit(miniXslice, miniYslice)
                predictedY = rf.predict(X_test)

            # calculating per run error
            errorrate = calc_error(predictedY, y_test)
            trainpercentmean[int(train_percent[j])] += errorrate
            mean_per_run_error.append(errorrate)

            print ("error rate for fold{}(LogisticRegression) with {}% train data is {}".format(i, train_rate, errorrate))

            j += 1

        mean_all_runs.append(np.mean(mean_per_run_error))

        print ("Mean error rate for fold{}(LogisticRegresson) is {}".format(i, np.mean(mean_per_run_error)))
        print ("Standard deviation for fold{}(LogisticRegression) is {}".format(i, np.std(mean_per_run_error)))

        i += 1

    print ("Mean error rate for all runs Logistic Regression is {}".format(np.mean(mean_all_runs)))
    print ("Standard deviation for all runs Logistic Regression is {}".format(np.std(mean_all_runs)))

flightPredictor()
