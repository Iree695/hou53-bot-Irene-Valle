import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TARGET_COLUMN = "SalePrice"
DEFAULT_DROP_COLUMNS = ["Id"]


def load_data(path: str, drop_columns: list[str] | None = None) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(path, na_values="?")

    columns_to_drop = DEFAULT_DROP_COLUMNS.copy()
    if drop_columns:
        columns_to_drop.extend(drop_columns)

    X = df.drop(columns=[TARGET_COLUMN], errors="ignore").copy()
    X = X.drop(columns=columns_to_drop, errors="ignore")

    y = df[TARGET_COLUMN].copy()

    return X, y


def infer_feature_types(X: pd.DataFrame) -> tuple[list[str], list[str]]:
    numeric_cols = X.select_dtypes(include="number").columns.tolist()
    categorical_cols = X.select_dtypes(exclude="number").columns.tolist()

    return numeric_cols, categorical_cols


def build_preprocessor(
    numeric_cols: list[str],
    categorical_cols: list[str],
    scale_numeric: bool = True,
) -> ColumnTransformer:
    numeric_steps = [
        ("imputer", SimpleImputer(strategy="median")),
    ]

    if scale_numeric:
        numeric_steps.append(("scaler", StandardScaler()))

    numeric_pipeline = Pipeline(numeric_steps)

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer([
        ("numeric", numeric_pipeline, numeric_cols),
        ("categorical", categorical_pipeline, categorical_cols),
    ])

    return preprocessor
