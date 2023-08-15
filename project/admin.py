from person import Person
import sqlite3


class Admin(Person):
    """
    The Admin class represents an administrator who has additional functionality compared to a regular Person.
    Attributes: Inherits attributes from the Person class.
    Methods: delete_user(user_id): Deletes a user from the database.

    """

    def delete_user(self, user_id):
        """
        Deletes a user from the database.
        Args: user_id (int): The ID of the user to be deleted.
        Returns: None
        """
        # Connect to the database
        conn = sqlite3.connect('big_data.db')
        cursor = conn.cursor()

        # Execute the DELETE statement
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
