from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model
model = joblib.load("healthcare_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # Get values from HTML form
    data = {
        "Gender": float(request.form["Gender"]),
        "Hospital Type": float(request.form["Hospital Type"]),
        "Visit Type": float(request.form["Visit Type"]),
        "Waiting Time": float(request.form["Waiting Time"]),
        "Nurse Staff Behaviour": float(request.form["Nurse Staff Behaviour"]),
        "Doctor Communication": float(request.form["Doctor Communication"]),
        "Hospital Cleanliness": float(request.form["Hospital Cleanliness"]),
        "Overall Satisfaction": float(request.form["Overall Satisfaction"]),
        "Return Intention": float(request.form["Return Intention"]),
        "Biggest Problem": float(request.form["Biggest Problem"]),
        "Treatment Quality": float(request.form["Treatment Quality"]),
        "Waiting Area Facilities": float(request.form["Waiting Area Facilities"]),
        "Respect Privacy": float(request.form["Respect Privacy"]),
        "Medicine Explanation": float(request.form["Medicine Explanation"]),
        "Charges": float(request.form["Charges"]),
        "Occupation": float(request.form["Occupation"]),
        "Age1": float(request.form["Age1"]),
        "Nurse Staff Behaviour Score": float(
            request.form["Nurse Staff Behaviour Score"]
        ),
        "Hospital Cleanliness Score": float(
            request.form["Hospital Cleanliness Score"]
        ),
        "Waiting Time Number": float(
            request.form["Waiting Time Number"]
        )
    }

    # Convert input into DataFrame
    input_data = pd.DataFrame([data])

    # Arrange columns in training order
    feature_order = [
        "Gender",
        "Hospital Type",
        "Visit Type",
        "Waiting Time",
        "Nurse Staff Behaviour",
        "Doctor Communication",
        "Hospital Cleanliness",
        "Overall Satisfaction",
        "Return Intention",
        "Biggest Problem",
        "Treatment Quality",
        "Waiting Area Facilities",
        "Respect Privacy",
        "Medicine Explanation",
        "Charges",
        "Occupation",
        "Age1",
        "Nurse Staff Behaviour Score",
        "Hospital Cleanliness Score",
        "Waiting Time Number"
    ]

    # Arrange input columns
    input_data = input_data[feature_order]

    # DEBUG
    print("\nInput sent to model:")
    print(input_data.to_string(index=False))

    print("\nInput shape:")
    print(input_data.shape)

    # Prediction
    prediction = model.predict(input_data)

    # Convert prediction to original label
    label_mapping = {
        0: "Maybe",
        1: "No",
        2: "Yes"
    }

    result = label_mapping[int(prediction[0])]

    # Render the styled result page instead of returning raw text,
    # so result.html (with the color-coded verdict stamp) actually shows.
    return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)