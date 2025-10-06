import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from database import insert_result  # Import the insert function

if __name__ == "__main__":
    try:
        print("Script started...")

        # Load dataset
        data = pd.read_csv("student_stress_factors.csv")
        X = data.drop('stress_label', axis=1)
        y = data['stress_label']

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.25, random_state=42
        )

        # Train model
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)

        # Example prediction on first test sample
        sample_user_id = "user1"
        sample_features = X_test[0].reshape(1, -1)  # Ensure correct shape
        sample_pred = clf.predict(sample_features)

        # Insert result into database
        insert_result(sample_user_id, sample_pred[0])

        print(f"Predicted stress level for {sample_user_id}: {sample_pred[0]}")
        print("Script finished successfully.")

    except Exception as e:
        print(f"Error occurred: {e}")
