import numpy as np
import pandas as pd

from sklearn.dummy import DummyRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import GroupShuffleSplit, LeaveOneGroupOut
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def split_by_group(
    df: pd.DataFrame,
    required_cols: list[str],
    group_col: str,
    test_size: float = 0.20,
    random_state: int = 42
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create development and test sets with separate specimens."""

    model_data = df.dropna(
        subset=required_cols + [group_col]
    ).copy()

    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=test_size,
        random_state=random_state
    )

    dev_idx, test_idx = next(
        splitter.split(
            model_data,
            groups=model_data[group_col]
        )
    )

    dev_set = model_data.iloc[dev_idx].copy()
    test_set = model_data.iloc[test_idx].copy()

    assert set(dev_set[group_col]).isdisjoint(
        set(test_set[group_col])
    )

    return dev_set, test_set


def make_ridge_model(alpha: float = 1.0) -> Pipeline:
    """Create an imputed and scaled Ridge regression pipeline."""

    return Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("regressor", Ridge(alpha=alpha))
    ])


def grouped_predictions(
    model,
    X: pd.DataFrame,
    y: pd.Series,
    groups: pd.Series
) -> np.ndarray:
    """Generate leave-one-group-out validation predictions."""

    logo = LeaveOneGroupOut()
    predictions = np.empty(len(y), dtype=float)

    for train_idx, val_idx in logo.split(X, y, groups=groups):
        X_train = X.iloc[train_idx]
        X_val = X.iloc[val_idx]

        y_train = y.iloc[train_idx]

        model.fit(X_train, y_train)
        predictions[val_idx] = model.predict(X_val)

    return predictions


def calculate_metrics(
    y_true: pd.Series | np.ndarray,
    predictions: np.ndarray
) -> dict[str, float]:
    """Calculate MAE and RMSE."""

    return {
        "MAE [W/mK]": mean_absolute_error(
            y_true,
            predictions
        ),
        "RMSE [W/mK]": np.sqrt(
            mean_squared_error(y_true, predictions)
        )
    }


def compare_feature_sets(
    dev_set: pd.DataFrame,
    feature_sets: dict[str, list[str]],
    target_col: str,
    group_col: str,
    alpha: float = 1.0
) -> tuple[pd.DataFrame, dict[str, np.ndarray]]:
    """Compare a mean baseline and Ridge feature sets using LOGO."""

    y_dev = dev_set[target_col]
    groups_dev = dev_set[group_col]

    predictions = {}

    # Mean baseline
    baseline = DummyRegressor(strategy="mean")

    baseline_features = next(iter(feature_sets.values()))
    X_baseline = dev_set[baseline_features]

    predictions["Training-mean baseline"] = grouped_predictions(
        baseline,
        X_baseline,
        y_dev,
        groups_dev
    )

    # Ridge models
    for model_name, feature_cols in feature_sets.items():
        ridge = make_ridge_model(alpha=alpha)

        predictions[model_name] = grouped_predictions(
            ridge,
            dev_set[feature_cols],
            y_dev,
            groups_dev
        )

    rows = []

    for model_name, model_predictions in predictions.items():
        metrics = calculate_metrics(
            y_dev,
            model_predictions
        )

        rows.append({
            "Model": model_name,
            **metrics
        })

        comparison = pd.DataFrame(rows)
    return comparison, predictions

