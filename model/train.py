import os

from preprocess import load_data, basic_cleaning, create_target, select_features
from features import build_feature_pipeline


def main():

    root_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(root_dir, "data", "flights.csv")

    df = load_data(data_path)

    print("Raw dataset shape:", df.shape)

    df = basic_cleaning(df)
    df = create_target(df)
    df = select_features(df)

    print("Processed dataset shape:", df.shape)

    X = df.drop("delayed", axis=1)
    y = df["delayed"]

    pipeline = build_feature_pipeline()

    X_transformed = pipeline.fit_transform(X)

    print("Feature matrix shape:", X_transformed.shape)


if __name__ == "__main__":
    main()