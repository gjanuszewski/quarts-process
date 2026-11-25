from sklearn.model_selection import GroupShuffleSplit

# Use specimen ID as the grouping variable
groups = eda_measurements["specimen_id"]

# 80% of specimens for training, 20% for testing
splitter = GroupShuffleSplit( n_splits=1,test_size=0.2,random_state=4)

train_idx, test_idx = next(splitter.split(eda_measurements, groups=groups))

train_df = eda_measurements.iloc[train_idx].copy()
test_df = eda_measurements.iloc[test_idx].copy()

print("Training specimens:")
print(sorted(train_df["specimen_id"].unique()))

print("\nTest specimens:")
print(sorted(test_df["specimen_id"].unique()))








# Define input features and target
feature_cols = [
    "temperature",
    "specific_heat",
    "density_kg_m3"
]

target_col = "conductivity_W_mK"

# Setting the evaluation boundary (80% dev, 20% test by specimen)
gss = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42
)

dev_idx, test_idx = next(
    gss.split(
        eda_measurements,
        groups=eda_measurements["specimen_id"]
    )
)

# Slicing into development and test sets
dev_set = eda_measurements.iloc[dev_idx].copy()
test_set = eda_measurements.iloc[test_idx].copy()

# Verifying zero specimen leakage across the boundary
assert set(dev_set["specimen_id"]).isdisjoint(
    set(test_set["specimen_id"])
), "Leakage detected!"

# Separating predictors and target
X_dev = dev_set[feature_cols].copy()
y_dev = dev_set[target_col].copy()

X_test = test_set[feature_cols].copy()
y_test = test_set[target_col].copy()

print(f"Dev shape: {X_dev.shape} | Test shape: {X_test.shape}")






from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Create mean baseline
baseline = DummyRegressor(strategy="mean")

# Fit using development data
baseline.fit(X_dev, y_dev)

# Predict on test data
y_pred_baseline = baseline.predict(X_test)

# Evaluate baseline
mae = mean_absolute_error(y_test, y_pred_baseline)
rmse = np.sqrt(mean_squared_error(y_test, y_pred_baseline))
r2 = r2_score(y_test, y_pred_baseline)

print(f"Mean prediction: {baseline.constant_[0][0]:.3f} W/mK")
print(f"Baseline MAE: {mae:.3f} W/mK")
print(f"Baseline RMSE: {rmse:.3f} W/mK")
print(f"Baseline R²: {r2:.3f}")
