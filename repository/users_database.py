from models.user import User

all_users = []


def find_user(user_id: int) -> User | None:
    for user in all_users:
        if user.id == user_id:
            return user
    return None


def remove_user(user_id: int) -> User | None:
    user = find_user(user_id)

    if user is None:
        return None

    all_users.remove(user)

    return user
