from database import execute_query, hash_password

class User:
    @staticmethod
    def add_user(username, password):
        """Add a new user to the database."""
        password_hash = hash_password(password)
        try:
            execute_query(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists

    @staticmethod
    def authenticate_user(username, password):
        """Authenticate a user."""
        password_hash = hash_password(password)
        result = execute_query(
            "SELECT id, username, has_voted FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash),
            fetch=True
        )
        if result:
            return {"id": result[0][0], "username": result[0][1], "has_voted": result[0][2]}
        return None

    @staticmethod
    def mark_user_voted(user_id):
        """Mark a user as having voted."""
        execute_query(
            "UPDATE users SET has_voted = TRUE WHERE id = ?",
            (user_id,)
        )