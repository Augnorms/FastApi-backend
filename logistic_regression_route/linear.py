from fastapi import APIRouter, HTTPException
import pandas as pd
from sklearn.linear_model import LogisticRegression
import os
from schemas.predict_schema import PredictSchema  # Ensure correct import
from sklearn.model_selection import train_test_split

router = APIRouter()

# Define the file path for the CSV file in the project folder
csv_file_path = os.path.join(os.getcwd(), "heart.csv")

@router.post("/predict")
def predict_condition(predict: PredictSchema):
    print("working directory",os.getcwd())
    try:
        # Load CSV data
        data = pd.read_csv(csv_file_path)

        # Define X and y
        X = data.drop(["HeartDisease"], axis=1)
        y = data["HeartDisease"]

        #finding unique values from non-numeric columns
        categories = {
            'ChestPainType':[data['ChestPainType'].unique()],
            'Sex':[data['Sex'].unique()],
            'RestingECG':[data['RestingECG'].unique()],
            'ST_Slope':[data['ST_Slope'].unique()],
            'ExerciseAngina':[data['ExerciseAngina'].unique()]
        }


        #replace non-numeric columns with boolean(True/False)
        X = pd.get_dummies(X, columns=categories.keys())

        # Split the data
        X_train, X_test, y_train, _y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        lr_regression_model = LogisticRegression()
        lr_regression_model.fit(X_train, y_train)

        def user_input_data():
            age = int(predict.Age)
            sex = predict.Sex
            chest_pain_type = predict.ChestPainType
            resting_bp = int(predict.RestingBP)
            cholestrol = int(predict.Cholesterol)
            fasting_bs = int(predict.FastingBS)
            resting_ecg = predict.RestingECG
            max_hr = int(predict.MaxHR)
            exercise_angina = predict.ExerciseAngina
            oldpeak = float(predict.Oldpeak)
            st_slope = predict.ST_Slope

            return{
                "Age": age,
                "Sex": sex,
                "ChestPainType": chest_pain_type,
                "RestingBP": resting_bp,
                "Cholesterol": cholestrol,
                "FastingBS": fasting_bs,
                "RestingECG": resting_ecg,
                "MaxHR": max_hr,
                "ExerciseAngina": exercise_angina,
                "Oldpeak": oldpeak,
                "ST_Slope": st_slope
            }

        #gettting input from user
        patient_data = user_input_data()

        patient_df = pd.DataFrame([patient_data])
        patient_df = pd.get_dummies(patient_df, columns=categories.keys())

        #finding the difference between train data and dataframe
        missing_feature = set(X_train.columns) - set(patient_df.columns)

        for feature in missing_feature:
            patient_df[feature] = 0

        patient_df = patient_df[X_train.columns]

        #model prediction
        model_prediction = lr_regression_model.predict(patient_df)
        
        patient_info = []

        for column, rowval in patient_data.items():
            patient_info.append(f"{column} = {rowval}")


        result = "Heart disease detected" if model_prediction[0] == 1 else "Healthy"
        return {"prediction": result, "data": patient_info}


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
