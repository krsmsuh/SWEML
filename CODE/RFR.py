import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from joblib import  dump

# Set the plot style to "seaborn"
sns.set(style="whitegrid")

# Load the CSV file into a pandas DataFrame
input_file = 'DATA_PATH' # You have to set the data path. In our study, we used the 13 csv files include the SWE variables in each cluster.
data = pd.read_csv(input_file)

# Exclude 'Cluster' and 'J_day' columns from features
X = data.drop(['Lat','Lon','Cluster', 'swe'], axis=1)
y = data['swe']

# Split the data into training and testing sets (70% training, 30% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create and train a Random Forest Regression model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Calculate the R-squared score
r2 = r2_score(y_test, y_pred)
print("R-squared score:", r2)

sns.regplot(x=y_test, y=y_pred, color='steelblue', line_kws={'color': 'red'})

# Set plot labels and title
plt.xlabel("Actual test data")
plt.ylabel("Predicted test data")
plt.title("Model: RandomForestRegressor")

# Add R-squared score and regression equation to the plot
plt.annotate(f"R-squared = {r2:.3f}", (0.05, 0.9), xycoords='axes fraction', fontsize=12)

# Display the plot
plt.show()

# Calculate RMSE
rmse = np.sqrt(((y_pred - y_test) ** 2).mean())

# Calculate the errors
errors = y_pred - y_test

# Plot RMSE with points and different colors
plt.figure(figsize=(10, 6))

# Plot RMSE with points and different colors
plt.subplot(2, 1, 1)
plt.scatter(range(len(y_test)), y_test, label='Target', color='steelblue', marker='o', s=40)
plt.scatter(range(len(y_test)), y_pred, label='Predicted', color='orange', marker='x', s=40)
plt.xlabel('Sample')
plt.ylabel('Value')
plt.title(f"RMSE: {rmse:.3f}")
plt.legend()

# Plot frequency of errors
plt.subplot(2, 1, 2)
sns.histplot(errors, kde=True, color='steelblue')
plt.xlabel('Error')
plt.ylabel('Frequency')
plt.title('Frequency of Errors')

plt.tight_layout()
plt.show()


# Save the final model using the filename as part of the model's name

filename = os.path.splitext(os.path.basename(input_file))[0]
model_filename = f"{filename}_random_forest_model.joblib"
dump(model, model_filename)

del(data)
