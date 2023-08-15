import sqlite3


class Order:
    """
    The Order class represents an order in the flight ticket reservation system.
    Attributes:
        _user_id (int): The ID of the user associated with the order.
        _num_of_tickets (int): The number of tickets in the order.
        _total_price (float): The total price of the order.
        _order_id (int): The ID of the order in the database.
    Methods: add_order_db(): Inserts the order into the database and returns the order ID.

    """
    def __init__(self, user_id, num_of_tickets=0, total_price=0):
        self._user_id = user_id
        self._num_of_tickets = num_of_tickets
        self._total_price = total_price
        self._order_id = self.add_order_db()

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def num_of_tickets(self):
        return self._num_of_tickets

    @num_of_tickets.setter
    def num_of_tickets(self, value):
        self._num_of_tickets = value

    @property
    def total_price(self):
        return self._total_price

    @total_price.setter
    def total_price(self, value):
        self._total_price = value

    @property
    def order_id(self):
        return self._order_id

    @order_id.setter
    def order_id(self, value):
        self._order_id = value


    def add_order_db(self):
        """
         Inserts the order into the database and returns the order ID.
         Returns: The order ID.
         """
        # Insert the user into the database
        conn = sqlite3.connect('big_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (user_id, num_of_tickets, total_price)
            VALUES (?, ?, ?)
        ''', (self._user_id, self._num_of_tickets, self._total_price))
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return order_id
