from flask import Flask, request, render_template
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import database  # Your database connector module

app = Flask(__name__)

# Feature names corresponding to the simplified questionnaire
feature_names = [
    'feature1', 'feature2', 'feature3', 'feature4', 'feature5',
    'feature6', 'feature7', 'feature8', 'feature9', 'feature10',
    'feature11', 'feature12', 'feature13', 'feature14', 'feature15'
]

# Load dataset with these features & stress label
data = pd.read_csv('student_stress.csv')

X = data[feature_names]
y = data['stress_label']

# Scale input features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train RandomForest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_scaled, y)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check all inputs present
        missing = [f for f in feature_names if f not in request.form]
        if 'user_id' not in request.form or missing:
            missing_fields = ['user_id'] + missing if 'user_id' not in request.form else missing
            return f"Missing input fields: {', '.join(missing_fields)}"

        try:
            user_id = request.form['user_id']

            # Collect and convert inputs to float
            features = [float(request.form[f]) for f in feature_names]

            # Scale features
            features_scaled = scaler.transform([features])

            # Predict stress level
            pred = int(model.predict(features_scaled)[0])

            # Insert into database
            database.insert_result(user_id, pred)

            # Return prediction result
            return f"<h3>Predicted stress level: {pred} for user {user_id}</h3>"

        except Exception as e:
            return f"An error occurred: {e}"

    return render_template('form.html')  # Your new form.html with 15 questions

if __name__ == '__main__':
    app.run(debug=True)

