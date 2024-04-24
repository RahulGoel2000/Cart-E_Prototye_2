import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from sklearn.utils import shuffle

# Load the data
data = pd.read_excel("router_data_2.xlsx")

# Shuffle the data
data_shuffled = shuffle(data, random_state=42)

# Split data into features (signal strengths) and labels (x and y coordinates)
X = data_shuffled.drop(columns=["x", "y"])
y = data_shuffled[["x", "y"]]

# Normalize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train the KNN model on the entire dataset
k = 5  # Number of neighbors
knn = KNeighborsRegressor(n_neighbors=k)
knn.fit(X_scaled, y)

# Take a contiguous subset of the data for testing
subset_size = 100  # Size of the subset
X_subset = X.iloc[:subset_size]
y_subset = y.iloc[:subset_size]



# Normalize the subset features
X_subset_scaled = scaler.transform(X_subset)

# Make predictions on the subset
y_subset_pred = knn.predict(X_subset_scaled)

# Evaluate the model
mse_subset = mean_squared_error(y_subset, y_subset_pred)
print("Mean Squared Error on Subset:", mse_subset)


new_signal_strengths = [46, 46, 46, 38, 40, 40, 84, 84, 84, 44, 46, 44, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 50, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 58, 60, 58, 0, 32, 0, 46, 48, 48, 0, 0, 0]

# Create a DataFrame with the new signal strengths
new_X = pd.DataFrame([new_signal_strengths], columns=X.columns)

# Normalize the features using the same scaler
new_X_scaled = scaler.transform(new_X)

# Make predictions using the trained KNN model
predicted_coordinates = knn.predict(new_X_scaled)

print("Predicted coordinates (x, y):", predicted_coordinates)