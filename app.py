import streamlit as st
import joblib
import numpy as np
import pandas as pd

from login import show_login, show_signup
from database import (
    save_prediction,
    get_prediction_history,
    clear_prediction_history
)

st.set_page_config(
    page_title="Student Performance Prediction System",
    page_icon="🎓",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    auth_option = st.sidebar.radio(
        "Select Option",
        ["Login", "Sign Up"]
    )

    if auth_option == "Login":
        show_login()
    else:
        show_signup()

    st.stop()

user_name = st.session_state.get("user_name", "Student")
user_email = st.session_state.get("user_email", "")
user_id = st.session_state.get("user_id")

st.sidebar.divider()
st.sidebar.subheader(f"👤 Welcome, {user_name}")
st.sidebar.caption(user_email)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📜 Prediction History"
    ]
)

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):
    st.session_state["logged_in"] = False
    st.session_state.pop("user_id", None)
    st.session_state.pop("user_name", None)
    st.session_state.pop("user_email", None)
    st.rerun()

if page == "📜 Prediction History":
    st.title("📜 Prediction History")

    if user_id:
        history = get_prediction_history(user_id)

        if history:
            df = pd.DataFrame(
                history,
                columns=[
                    "Study Hours",
                    "Attendance (%)",
                    "Previous Score",
                    "Sleep Hours",
                    "Assignments (%)",
                    "Predicted Score",
                    "Date & Time"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download Prediction History",
                data=csv,
                file_name="prediction_history.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.divider()

            confirm_clear = st.checkbox(
                "I confirm that I want to delete my prediction history."
            )

            if st.button(
                "🗑️ Clear Prediction History",
                use_container_width=True
            ):
                if confirm_clear:
                    clear_prediction_history(user_id)
                    st.success(
                        "Prediction history cleared successfully."
                    )
                    st.rerun()
                else:
                    st.warning(
                        "Please confirm before deleting your history."
                    )
        else:
            st.info("No prediction history found.")

    else:
        st.warning(
            "User ID not found. Please logout and login again."
        )

    st.stop()

st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .sub-title {
        text-align: center;
        font-size: 18px;
        color: gray;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 25px;
        font-weight: bold;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .prediction-box {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #cccccc;
        margin-top: 20px;
    }

    .score {
        font-size: 50px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

try:
    model = joblib.load(
        "student_performance_model.pkl"
    )
except Exception as e:
    st.error("Model could not be loaded.")
    st.error(str(e))
    st.stop()

st.markdown(
    """
    <div class="main-title">
        🎓 Student Performance Prediction System
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="sub-title">
        AI-Driven Machine Learning System for Predicting
        Student Exam Performance
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

st.markdown(
    """
    <div class="section-title">
        📝 Enter Student Details
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    study_hours = st.slider(
        "📚 Study Hours per Day",
        min_value=0.5,
        max_value=10.0,
        value=5.0,
        step=0.5
    )

    attendance = st.slider(
        "🏫 Attendance Percentage",
        min_value=40,
        max_value=100,
        value=75
    )

    previous_score = st.slider(
        "📄 Previous Exam Score",
        min_value=30,
        max_value=100,
        value=70
    )

with col2:
    sleep_hours = st.slider(
        "😴 Sleep Hours per Day",
        min_value=4.0,
        max_value=10.0,
        value=7.0,
        step=0.5
    )

    assignments_completed = st.slider(
        "✅ Assignments Completed (%)",
        min_value=30,
        max_value=100,
        value=80
    )

st.divider()

if st.button(
    "🔮 Predict Student Performance",
    use_container_width=True,
    type="primary"
):
    input_data = np.array(
        [[
            study_hours,
            attendance,
            previous_score,
            sleep_hours,
            assignments_completed
        ]]
    )

    try:
        prediction = model.predict(input_data)[0]
        prediction = float(prediction)
        prediction = max(0, min(100, prediction))

    except Exception as e:
        st.error("Could not generate prediction.")
        st.error(str(e))
        st.stop()

    if user_id:
        try:
            save_prediction(
                user_id,
                study_hours,
                attendance,
                previous_score,
                sleep_hours,
                assignments_completed,
                prediction
            )

        except Exception as e:
            st.warning(
                "Prediction generated, but could not be saved to history."
            )
            st.error(str(e))

    st.markdown(
        """
        <div class="section-title">
            📊 Prediction Result
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="prediction-box">
            <h3>Predicted Exam Score</h3>
            <div class="score">
                {prediction:.2f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-title">
            🏆 Performance Analysis
        </div>
        """,
        unsafe_allow_html=True
    )

    if prediction >= 85:
        st.success(
            "🌟 Excellent Performance! "
            "The student is expected to perform exceptionally well."
        )

    elif prediction >= 70:
        st.success(
            "✅ Good Performance! "
            "The student is showing strong academic performance."
        )

    elif prediction >= 50:
        st.warning(
            "📚 Average Performance. "
            "More focused study and regular practice are recommended."
        )

    else:
        st.error(
            "⚠️ Performance Needs Improvement. "
            "The student may require additional academic support."
        )

    st.markdown(
        """
        <div class="section-title">
            💡 Smart Recommendations
        </div>
        """,
        unsafe_allow_html=True
    )

    recommendations = []

    if study_hours < 4:
        recommendations.append(
            "📚 Increase daily study time to at least 4 to 6 hours."
        )

    if attendance < 75:
        recommendations.append(
            "🏫 Improve attendance to maintain consistency in learning."
        )

    if sleep_hours < 6:
        recommendations.append(
            "😴 Try to get at least 6 to 8 hours of sleep "
            "for better concentration."
        )

    if assignments_completed < 70:
        recommendations.append(
            "📝 Complete more assignments to improve "
            "understanding and practice."
        )

    if previous_score < 60:
        recommendations.append(
            "🎯 Focus on weak subjects and revise "
            "previous concepts regularly."
        )

    if not recommendations:
        recommendations.append(
            "🌟 Great work! Maintain your current "
            "study routine and consistency."
        )

    for recommendation in recommendations:
        st.info(recommendation)

    st.markdown(
        """
        <div class="section-title">
            📋 Student Prediction Summary
        </div>
        """,
        unsafe_allow_html=True
    )

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:
        st.metric(
            "📚 Study Hours",
            f"{study_hours} hrs/day"
        )

        st.metric(
            "🏫 Attendance",
            f"{attendance}%"
        )

    with summary_col2:
        st.metric(
            "📄 Previous Score",
            f"{previous_score}%"
        )

        st.metric(
            "😴 Sleep Hours",
            f"{sleep_hours} hrs/day"
        )

    with summary_col3:
        st.metric(
            "✅ Assignments",
            f"{assignments_completed}%"
        )

        st.metric(
            "🎯 Predicted Score",
            f"{prediction:.2f}%"
        )