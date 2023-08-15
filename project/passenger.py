import sqlite3


class Passenger:
    """
    Initializes a new instance of the Passenger class.
    Args:
        first_name (str): The first name of the passenger.
        last_name (str): The last name of the passenger.
        dob (str): The date of birth of the passenger.
        passport (str): The passport number of the passenger.
    """
    def __init__(self, first_name, last_name, dob, passport):
        self._first_name = first_name
        self._last_name = last_name
        self._dob = dob
        self._passport = passport
        self.add_to_psngr_db()

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def dob(self):
        return self._dob

    @dob.setter
    def dob(self, value):
        self._dob = value

    @property
    def passport(self):
        return self._passport

    @passport.setter
    def passport(self, value):
        self._passport = value

    def add_to_psngr_db(self):
        """
        Insert the passenger into the database
        """
        conn = sqlite3.connect('big_data.db')
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO passengers (first_name, last_name, date_of_birth, passport)
                VALUES (?, ?, ?, ?)
            ''', (self._first_name, self._last_name, self._dob, self._passport))
        conn.commit()
        conn.close()

    def get_pass_id(self):
        """
        Retrieves the passenger ID from the passenger database based on the passport number.
        Returns: The passenger ID.
        """
        conn = sqlite3.connect('big_data.db')
        cursor = conn.cursor()
        query = f"SELECT id FROM passengers WHERE passport =  ?"
        cursor.execute(query, (self._passport,))

        output = cursor.fetchall()
        return output[0][0]
