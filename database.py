import sqlite3
import hashlib


def get_connection():
    return sqlite3.connect("users.db")


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            study_hours REAL NOT NULL,
            attendance REAL NOT NULL,
            previous_score REAL NOT NULL,
            sleep_hours REAL NOT NULL,
            assignments_completed REAL NOT NULL,
            predicted_score REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                name.strip(),
                email.lower().strip(),
                hash_password(password)
            )
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, email
        FROM users
        WHERE email = ? AND password = ?
        """,
        (
            email.lower().strip(),
            hash_password(password)
        )
    )

    user = cursor.fetchone()
    conn.close()

    return user


def email_exists(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE email = ?
        """,
        (email.lower().strip(),)
    )

    user = cursor.fetchone()
    conn.close()

    return user is not None


def save_prediction(
    user_id,
    study_hours,
    attendance,
    previous_score,
    sleep_hours,
    assignments_completed,
    predicted_score
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO predictions (
            user_id,
            study_hours,
            attendance,
            previous_score,
            sleep_hours,
            assignments_completed,
            predicted_score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            study_hours,
            attendance,
            previous_score,
            sleep_hours,
            assignments_completed,
            predicted_score
        )
    )

    conn.commit()
    conn.close()


def get_prediction_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            study_hours,
            attendance,
            previous_score,
            sleep_hours,
            assignments_completed,
            predicted_score,
            created_at
        FROM predictions
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    history = cursor.fetchall()
    conn.close()

    return history


def clear_prediction_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM predictions
        WHERE user_id = ?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()


create_tables()