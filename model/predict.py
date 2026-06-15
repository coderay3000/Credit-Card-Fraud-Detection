import joblib
import pandas as pd

# import the ml model
with open('model/fraud_model.joblib','rb') as f:
    fraud_model=joblib.load(f)


def predict_output(user_input: dict):

    df = pd.DataFrame([user_input])

    # Predict the class
    predicted_class = fraud_model.predict(df)[0]

    return int(predicted_class)