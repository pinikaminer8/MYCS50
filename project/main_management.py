from user_management import *
from flights_management import *
from order_management import OrderManagement


class MainManagement:
    """
    The MainManagement class handles the main operations and manages the sub-modules of the flight ticket reservation system.
    Attributes:
        user_management (UserManagement): An instance of the UserManagement class for user-related operations.
        flights_management (FlightManagement): An instance of the FlightManagement class for flight-related operations.
        order_management (OrderManagement): An instance of the OrderManagement class for order-related operations.
    """

    def __init__(self):
        """
        Initializes an instance of the MainManagement class.
        Creates instances of the sub-modules UserManagement, FlightManagement, and OrderManagement.
        """
        self.user_management = UserManagement()
        self.flights_management = FlightManagement()
        self.order_management = OrderManagement()

