import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# --------------------------------------------------
# AI-Driven Student Performance Prediction System
# Model Training Script
# --------------------------------------------------

# Fix random seed so results remain reproducible
np.random.seed(42)

# Number of student records
num_students = 1500

# Generate sample student dataset
study_hours = np.random.uniform(0.5, 10, num_students)
attendance = np.random.uniform(40, 100, num_students)
previous_score = np.random.uniform(30, 100, num_students)
sleep_hours = np.random.uniform(4, 10, num_students)
assignments_completed = np.random.uniform(30, 100, num_students)

# Generate exam score based on student performance factors
exam_score = (
    study_hours * 3.0
    + attendance * 0.25
    + previous_score * 0.35
    + sleep_hours * 1.0
    + assignments_completed * 0.12
    + np.random.normal(0, 3, num_students)
)

# Keep exam scores between 0 and 100
exam_score = np.clip(exam_score, 0, 100)

# Create DataFrame
data = pd.DataFrame({
    "Study_Hours": study_hours,
    "Attendance": attendance,
    "Previous_Score": previous_score,
    "Sleep_Hours": sleep_hours,
    "Assignments_Completed": assignments_completed,
    "Exam_Score": exam_score
})

# Save dataset
data.to_csv("student_performance.csv", index=False)

# Features and target
X = data[
    [
        "Study_Hours",
        "Attendance",
        "Previous_Score",
        "Sleep_Hours",
        "Assignments_Completed"
    ]
]

y = data["Exam_Score"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Random Forest Machine Learning model
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

# Train model
model.fit(X_train, y_train)

# Test model
predictions = model.predict(X_test)

# Calculate evaluation metrics
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

# Save trained model
joblib.dump(model, "student_performance_model.pkl")

# Save model metrics
with open("model_metrics.txt", "w") as file:
    file.write(f"Mean Absolute Error: {mae:.2f}\n")
    file.write(f"R2 Score: {r2:.4f}\n")

print("=" * 50)
print("STUDENT PERFORMANCE ML MODEL")
print("=" * 50)
print("Dataset created successfully!")
print(f"Total Student Records: {len(data)}")
print(f"Mean Absolute Error: {mae:.2f}")
print(f"R2 Score: {r2:.4f}")
print("Model saved as: student_performance_model.pkl")
print("Dataset saved as: student_performance.csv")
print("=" * 50)
print("MODEL TRAINING COMPLETED SUCCESSFULLY!")