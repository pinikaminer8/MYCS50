from user import User
from exeptions import *
import sqlite3


class UserManagement:

    def create_new_user(self):
        """
        Creates a new user by prompting for user information and validating it.
        Returns: User: The created user object.
        """
        f_name_status = False
        while not f_name_status:
            first_name = input("What is your first name?: ")
            f_name_status = validate_name(first_name)

        l_name_status = False
        while not l_name_status:
            last_name = input("What is your last name?: ")
            l_name_status = validate_name(last_name)

        p_num_status = False
        while not p_num_status:
            phone_num = input("Please enter your phone num: ")
            p_num_status = validate_phone_num(phone_num)

        email_status = False
        while not email_status:
            email = input("Please enter your Email address: ")
            email_status = validate_email(email)

        pass_status = False
        while not pass_status:
            print("Password must contain: \n"
                  "Upper and Lower case letters\n"
                  "number and special char, at list 8 chars")
            new_password = input("Set a password: ")
            pass_status = validate_password(new_password)

        # Create a new User object with the provided information
        current_user = User(first_name=first_name, last_name=last_name, phone_num=phone_num, email=email,
                            password=new_password)
        return current_user

    def check_if_user(self):
        """
        Checks if a user exists in the database based on provided credentials.
        Returns: User: The user object if found in the database.
                False if the user is not found or the credentials are invalid.
        """
        user_name = input("Please enter your username (Email): ")
        password = input("Please enter your password: ")
        # Connect to the database
        conn = sqlite3.connect('big_data.db')
        cursor = conn.cursor()
        # Execute a SELECT query to retrieve the user with the given username and password
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (user_name, password))
        row = cursor.fetchone()
        # Close the connection
        conn.close()
        if row is not None:
            # User found in the database
            print(f"Welcome back, {row[1]}!")
            # Create a User object with the provided information from DB
            current_user = User(first_name=row[1], email=user_name, password=password, is_signed_up=True)
            return current_user
        else:
            # User not found in the database or invalid credentials
            print("One of the details is incorrect. Please retry.")
            return False




