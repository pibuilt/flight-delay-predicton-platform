import os
import joblib
import pandas as pd

MODEL = None


def load_model():

    global MODEL

    if MODEL is None:

        # Find project root
        current_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(current_dir, "../../../"))

        model_path = os.path.join(
            project_root,
            "models",
            "flight_delay_model.joblib"
        )

        print("Loading model from:", model_path)

        MODEL = joblib.load(model_path)

    return MODEL


def predict_flight_delay(input_data: dict):

    model = load_model()

    df = pd.DataFrame([input_data])

    prediction = model.predict(df)[0]

    probability = model.predict_proba(df)[0][1]

    return {
        "prediction": int(prediction),
        "delay_probability": float(probability)
    }