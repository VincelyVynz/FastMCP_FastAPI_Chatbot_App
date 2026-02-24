import pyodbc

# SQL Server connection string
CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=MyDatabase;"
    "Trusted_Connection=yes;"
)

# Custom exceptions
class UserNotFoundError(Exception):
    pass


def get_connection():
    return pyodbc.connect(CONNECTION_STRING)


def get_user_by_id(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Users WHERE id = ?",
        (user_id,)
    )
    user = cursor.fetchone()
    conn.close()

    if user is None:
        raise UserNotFoundError(f"User with id {user_id} not found")

    return user


def add_new_user(username: str, email: str, country: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Users (username, email, country) VALUES (?, ?, ?)",
        (username, email, country)
    )
    conn.commit()
    conn.close()


def delete_user(user_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Users WHERE id = ?",
            (user_id,)
        )
        conn.commit()
        conn.close()
        return {"status": "success", "deleted_user_id": user_id}
    except Exception as e:
        return f"Error deleting user with id {user_id}. Error: {e}"


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()

    if len(users) == 0:
        return "Database accessed successfully. The users table is currently empty."

    return {"status": "success", "users": users}


def delete_duplicate_users():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM Users
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM Users
                GROUP BY email
            )
            """
        )
        deleted_counts = cursor.rowcount
        conn.commit()
        conn.close()
        return {"status": "success", "deleted_duplicates": deleted_counts}
    except Exception as e:
        return f"Error deleting duplicate users. Error: {e}"