import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Load the original dataset
df_tornadoes = pd.read_csv('Tornado Incidence 1950-2023 Formatted.csv')

# Load the additional dataset with temperature values + precipitation values
df_TEXKAN_temperature = pd.read_csv('Difference on Temperatures TEXKAN.csv')
df_TEXKAN_precipitation = pd.read_csv('Difference on Precipitation TEXKAN.csv')
df_OK_temperature = pd.read_csv('Oklahoma Monthly Temperatures (1950-2023).csv')
df_OK_precipitation = pd.read_csv('Oklahoma Monthly Precipitation (1950-2023).csv')

# Ensure 'Date' columns are treated as string
df_tornadoes['Date'] = df_tornadoes['Date'].astype(str)
df_TEXKAN_temperature['Date'] = df_TEXKAN_temperature['Date'].astype(str)
df_TEXKAN_precipitation['Date'] = df_TEXKAN_precipitation['Date'].astype(str)
df_OK_temperature['Date'] = df_OK_temperature['Date'].astype(str)
df_OK_precipitation['Date'] = df_OK_precipitation['Date'].astype(str)

# Merge the two datasets on the 'Date' column
df = pd.merge(df_tornadoes, df_TEXKAN_temperature, on='Date')
df = pd.merge(df, df_TEXKAN_precipitation, on='Date', how='left')
df = pd.merge(df, df_OK_temperature, on='Date', how='left')
df = pd.merge(df, df_OK_precipitation, on='Date', how='left')

# Handle missing values in the 'PrecipDiff' column
df['PrecipDiff'] = df['PrecipDiff'].fillna(df['PrecipDiff'].mean())

# Ensure all relevant columns are treated correctly
df['Month'] = df['Date'].str.split('.').str[0].astype(int)
df['Year'] = df['Date'].str.split('.').str[1].astype(int)

# Create additional features for seasonality
df['Month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
df['Month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)

# Define features and target including the temperature difference
X = df[['Month', 'Year', 'Month_sin', 'Month_cos', 'TempDiff', 'PrecipDiff', 'OkTemp', 'OkPrecip']]
y = df['Count']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest Regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = model.score(X_test, y_test)
print(f'Mean Squared Error: {mse}')
print(f'R-squared Value: {r2}')

# Optional: Display feature importance
feature_importances = pd.Series(model.feature_importances_, index=X.columns)
print(feature_importances.sort_values(ascending=False))

# Save the trained model to a file
model_filename = 'Oklahoma_RFR_model.joblib'
joblib.dump(model, model_filename)
print(f'Model saved to {model_filename}')
