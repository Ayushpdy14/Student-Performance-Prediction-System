# 🎓 Student Performance Prediction System

An AI-powered Machine Learning application that predicts a student's expected exam performance based on various academic and lifestyle factors.

The application provides performance analysis, personalized recommendations, prediction history, and a simple user authentication system through an interactive Streamlit interface.

## 🚀 Features

- 🔐 User Sign Up and Login System
- 🎯 Student Exam Score Prediction
- 📚 Analysis based on Study Hours
- 🏫 Attendance Percentage Analysis
- 📄 Previous Exam Score Analysis
- 😴 Sleep Hours Analysis
- ✅ Assignment Completion Analysis
- 🏆 Performance Analysis
- 💡 Smart Personalized Recommendations
- 📜 Prediction History
- 📥 Download Prediction History as CSV
- 🗑️ Clear Prediction History
- 🎨 Interactive Streamlit User Interface

## 🤖 Machine Learning

The system uses a trained Machine Learning model to predict student exam performance. The prediction is generated using the following input features:

- Study Hours per Day
- Attendance Percentage
- Previous Exam Score
- Sleep Hours per Day
- Assignments Completed Percentage

Based on these factors, the model predicts an expected exam score and provides performance feedback and recommendations.

## 🛠️ Technologies Used

- Python
- Streamlit
- Scikit-learn
- NumPy
- Pandas
- Joblib
- SQLite
- Machine Learning

## 📂 Project Structure

- app.py - Main Streamlit application
- login.py - User login and signup functionality
- database.py - Database operations
- train_model.py - Machine Learning model training
- student_performance_model.pkl - Trained ML model
- student_performance.csv - Dataset
- model_metrics.txt - Model performance metrics
- requirements.txt - Required Python dependencies

## ▶️ Run the Project Locally

Install the required dependencies:

pip install -r requirements.txt

Run the Streamlit application:

python -m streamlit run app.py

## 🌐 Deployment

The application is deployed using Streamlit Community Cloud and the source code is hosted on GitHub.

## 🎯 Project Objective

The objective of this project is to use Machine Learning to analyze factors that influence student academic performance and predict expected exam scores. The system also provides useful recommendations to help students improve their academic performance.

## 👨‍💻 Developer

Developed as a Machine Learning project using Python and Streamlit.
