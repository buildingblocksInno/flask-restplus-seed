import logging

from app_extensions import bcrypt

from database.models import User
from database import db

logger = logging.getLogger()


class UserAccess:
    """
    Class which handles the user access
    """

    @staticmethod
    def get_user(username: str, vendor_id: int, user_type: str) -> User:
        """
        Get user on the basis of the
        :param user_type:
        :param vendor_id:
        :param username:
        :return:
        """

        user = User.query.filter(
            User.username == username,
            User.vendor_id == vendor_id,
            User.user_type == user_type,
            User.is_active == True
        )
        return user.one_or_none()

    @staticmethod
    def create_user(
            username: str,
            password: str,
            vendor_id: str,
            user_type: str
    ) -> User:
        """
        Create a new user from sign up
        :param username:
        :param password:
        :param vendor_id:
        :param user_type:
        """
        password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(
            username=username,
            password=password,
            vendor_id=vendor_id,
            user_type=user_type,
            is_active=True
        )
        db.session.add(user)
        db.session.commit()

        return user
