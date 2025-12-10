# AuthorizedDatabase Example

class AuthorizedDatabase:
    def __init__(self):
        # Simulating Hash Map {ID: Name}
        self.db = {
            "USER_001": "Admin Alice",
            "USER_002": "Security Bob",
            "USER_003": "Staff Charlie"
        }

    def check_access(self, user_id):
        return self.db.get(user_id, None)

if __name__ == "__main__":
    auth_db = AuthorizedDatabase()

    # List of user IDs to check
    user_ids = ["USER_001", "USER_002", "USER_004", "USER_003", "USER_005"]

    for uid in user_ids:
        user_name = auth_db.check_access(uid)
        if user_name:
            print(f"Access granted for {uid}: {user_name}")
        else:
            print(f"Access denied for {uid}")
