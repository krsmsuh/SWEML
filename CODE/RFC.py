import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from joblib import Parallel, delayed, dump  # Add the import statement for dump
import multiprocessing


# Load the large CSV file (you might need to use a streaming/batch processing approach for very large files)
data = pd.read_csv('/home/krsmsuh/01_data/00_mahdi/00_Final/02_train/CL_13.csv')

# Split the data into input features (X) and target (y)
X = data[['Lat', 'Lon', 'Year', 'Month', 'skt', 'sd', 'ssrd', 'r', 'tp', 'api', 'ptype', 'tmp', 'vegt', 'anor', 'isor', 'slor']]
y = data['Cluster']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

In classification, Mahdi did different ratio. 


# Initialize the Random Forest classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Define the function to train a single model on a subset of data
def train_model(X_train, y_train):
    model = clf.fit(X_train, y_train)
    return model

# Get the number of CPU cores
num_cores = 50

# Train the classifiers in parallel using all available cores
trained_models = Parallel(n_jobs=num_cores)(delayed(train_model)(X_batch, y_batch)
                                           for X_batch, y_batch in zip(np.array_split(X_train, num_cores),
                                                                      np.array_split(y_train, num_cores)))

# Combine the results of trained models (optional, you can choose to use one model)
clf = trained_models[0]

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

report = classification_report(y_test, y_pred)
print("Classification Report:")
print(report)

# Save the trained model to a file
model_filename = 'random_forest_model_cluster.joblib'
joblib.dump(clf, model_filename)
print(f"Trained model saved to {model_filename}")
