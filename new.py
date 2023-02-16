import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Load GPS data and ground truth speed data into a Pandas dataframe
data = pd.read_csv("data/address.csv")

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data[["gps_latitude", "gps_longitude"]], data["vehicle_speed"], test_size=0.5)

# Train a linear regression model on the training data
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model on the testing data
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print("Mean absolute error: ", mae)
