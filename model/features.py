from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline


def build_feature_pipeline():
    """
    Build sklearn preprocessing pipeline.
    """

    categorical_features = [
        "AIRLINE",
        "ORIGIN_AIRPORT",
        "DESTINATION_AIRPORT",
    ]

    numerical_features = [
        "DEPARTURE_TIME",
        "DISTANCE",
        "DAY_OF_WEEK",
    ]

    categorical_transformer = OneHotEncoder(handle_unknown="ignore")

    numerical_transformer = StandardScaler()

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", categorical_transformer, categorical_features),
            ("numerical", numerical_transformer, numerical_features),
        ]
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor)
        ]
    )

    return pipeline