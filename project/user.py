from person import Person
import sqlite3


class User(Person):
    """
    Represents a user with its attributes and methods.
    Inherits from the super class Person
    """
    def __init__(self, first_name=None, last_name=None, phone_num=None, email=None, password=None, is_signed_up=False):
        super().__init__(first_name, last_name, phone_num, email, password)
        self._is_signed_up = is_signed_up
        self.add_to_db() if not self._is_signed_up else None


    def add_to_db(self):
        """
        Insert the user into the database
        """
        conn = sqlite3.connect('big_data.db')
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO users (first_name, last_name, phone_num, email, password)
                VALUES (?, ?, ?, ?, ?)
            ''', (self._first_name, self._last_name, self._phone_num, self._email, self._password))
        conn.commit()
        conn.close()


