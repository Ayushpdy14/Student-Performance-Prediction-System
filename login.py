import streamlit as st

from database import register_user, login_user, email_exists


def apply_login_style():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(
                -45deg,
                #eef2ff,
                #fdf2f8,
                #ecfeff,
                #f5f3ff
            );
            background-size: 400% 400%;
            animation: gradientAnimation 12s ease infinite;
        }

        @keyframes gradientAnimation {
            0% {
                background-position: 0% 50%;
            }

            50% {
                background-position: 100% 50%;
            }

            100% {
                background-position: 0% 50%;
            }
        }

        [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.75);
            padding: 30px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.8);
            box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.08);
            backdrop-filter: blur(12px);
        }

        .login-title {
            text-align: center;
            font-size: 38px;
            font-weight: 700;
            color: #253858;
            margin-bottom: 5px;
        }

        .login-subtitle {
            text-align: center;
            font-size: 16px;
            color: #64748b;
            margin-bottom: 30px;
        }

        .stTextInput input {
            border-radius: 10px;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            width: 100%;
            border-radius: 10px;
            height: 48px;
            font-size: 16px;
            font-weight: 600;
        }

        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.75);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def show_login():
    apply_login_style()

    st.markdown(
        """
        <div class="login-title">
            🎓 Student Performance Prediction System
        </div>

        <div class="login-subtitle">
            AI-powered student performance analysis and prediction
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("login_form"):

        st.subheader("🔐 Login")

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        login_button = st.form_submit_button(
            "Login",
            use_container_width=True,
            type="primary"
        )

        if login_button:

            if not email or not password:
                st.warning(
                    "Please enter your email and password."
                )

            else:
                user = login_user(
                    email,
                    password
                )

                if user:
                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = user[0]
                    st.session_state["user_name"] = user[1]
                    st.session_state["user_email"] = user[2]

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:
                    st.error(
                        "Invalid email or password."
                    )


def show_signup():
    apply_login_style()

    st.markdown(
        """
        <div class="login-title">
            🎓 Student Performance Prediction System
        </div>

        <div class="login-subtitle">
            Create your account to start predicting student performance
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("signup_form"):

        st.subheader("✨ Create Account")

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm your password"
        )

        signup_button = st.form_submit_button(
            "Create Account",
            use_container_width=True,
            type="primary"
        )

        if signup_button:

            if not name or not email or not password or not confirm_password:
                st.warning(
                    "Please fill in all fields."
                )

            elif password != confirm_password:
                st.error(
                    "Passwords do not match."
                )

            elif len(password) < 6:
                st.warning(
                    "Password must be at least 6 characters."
                )

            elif email_exists(email):
                st.error(
                    "An account with this email already exists."
                )

            else:
                success = register_user(
                    name,
                    email,
                    password
                )

                if success:
                    st.success(
                        "Account created successfully! "
                        "Now select Login from the sidebar."
                    )

                else:
                    st.error(
                        "Could not create account. Please try again."
                    )