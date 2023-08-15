from passenger import Passenger
from ticket import Ticket
from order import Order
from exeptions import *
import random
import sqlite3


class OrderManagement:
    """
    The OrderManagement class handles the creation and management of flight orders in the reservation system.
    Methods:
        create_new_order(user_id): Creates a new order for the specified user.
        add_passenger(): Adds a new passenger to the order.
        add_ticket(pass_id, order_id, flight_id, price): Adds a new ticket to the order.
        take_seat(grade): Generates a seat number based on the given grade.
        payment(total_price): Handles the payment process for the order.
        update_order(order, total_price, num_of_travelers): Updates the order details in the database.
        show_order(origin, destination, order_id, tick_num, tot_price): Displays the order information.
    """

    def create_new_order(self, user_id):
        """
        Creates a new order for the specified user.
        Args: user_id (int): The ID of the user.
        Returns: Order: The newly created order.
        """
        user_id = user_id
        new_order = Order(user_id=user_id)
        return new_order

    def add_passenger(self):
        """
        Prompts the user to enter passenger details and creates a new Passenger object.
        Returns: Passenger: The newly created passenger.
        """
        while True:
            p_f_name = input("Please enter passenger's first name: ")
            if validate_name(p_f_name):
                break

        while True:
            p_l_name = input("Please enter passenger's last name: ")
            if validate_name(p_l_name):
                break

        while True:
            p_dob = input("Please enter passenger's D.O.B (yyyy/mm/dd): ")
            if validate_dob_date(p_dob):
                break

        while True:
            p_pass_num = input("Please enter passenger's passport number: ")
            if validate_passport(p_pass_num):
                break

        new_passenger = Passenger(first_name=p_f_name, last_name=p_l_name, dob=p_dob, passport=p_pass_num)
        return new_passenger

    def add_ticket(self, pass_id, order_id, flight_id, price):
        """
        Adds a new ticket object to the order.

        Args:
            pass_id (int): The ID of the passenger.
            order_id (int): The ID of the order.
            flight_id (int): The ID of the flight.
            price (float): The price of the ticket.

        Returns:
            Ticket: The newly created ticket.
        """
        # Set the default seat class to "economy"
        seat_class = "economy"
        # Generate a random seat for the "economy" class
        seat = self.take_seat(grade="economy")
        while True:
            # Prompt the user to check for seat upgrade options
            is_upgrade = input("Do you wish to check seat upgrade options? (y/n): ")
            if is_upgrade.lower() == 'n' or is_upgrade.lower() == 'no':
                # If no upgrade is chosen, print the price and seat for economy class
                print(f"The price for economy class is {price}, passenger seat: {seat}")
                break
            # If upgrade is chosen
            elif is_upgrade.lower() == 'y' or is_upgrade.lower() == 'yes':
                new_price, new_seat = "", ""
                while True:
                    # Prompt the user to choose the preferred class
                    seat_class = input("What is your preferred class? (business/first): ")
                    if seat_class.lower() == "business":
                        # Calculate the new price based on the chosen class
                        new_price = '$' + str(int(price[1:]) * 2)
                        # Generate a random seat for the "business" class
                        new_seat = self.take_seat(grade="business")
                        break
                    elif seat_class.lower() == "first":
                        # Calculate the new price based on the chosen class
                        new_price = '$' + str(int(price[1:]) * 3)
                        # Generate a random seat for the "first" class
                        new_seat = self.take_seat(grade="first")
                        break
                # Print the price and seat for the chosen class
                print(f"The price for {seat_class} class is {new_price}, passenger seat: {new_seat}")
                # Prompt the user to confirm the upgrade
                fin_upgrade = input("Please confirm upgrade (y/n): ")
                if fin_upgrade.lower() == 'y' or fin_upgrade.lower() == 'yes':
                    # If the upgrade is confirmed, update the price and seat with the new values
                    price, seat = new_price, new_seat
                elif fin_upgrade.lower() == 'n' or fin_upgrade.lower() == 'no':
                    # If the upgrade is not confirmed, keep the original price and seat values
                    price, seat = price, seat
            break  # Exit the loop

        # Create a new ticket object with the provided details
        new_ticket = Ticket(pass_id=pass_id, flight_id=flight_id, seat_class=seat_class, price=price,
                            order_id=order_id, seat=seat)
        return new_ticket

    def take_seat(self, grade):
        """
        Generates a seat number based on the given grade.
        Args: grade: The class grade of the seat (economy/business/first).
        Returns: The generated seat number.
        """
        # Check if the grade is "economy"
        if grade == "economy":
            # Generate a random seat letter from A to J
            seat_letter = random.choice([chr(i) for i in range(65, 75)])
            # Generate a random seat number from 16 to 50
            seat_number = random.randint(16, 50)
        # Check if the grade is "business"
        elif grade == "business":
            # Generate a random seat letter from A to G
            seat_letter = random.choice([chr(i) for i in range(65, 71)])
            # Generate a random seat number from 6 to 16
            seat_number = random.randint(6, 16)
        # Check if the grade is "first"
        elif grade == "first":
            # Generate a random seat letter from A to C
            seat_letter = random.choice([chr(i) for i in range(65, 68)])
            # Generate a random seat number from 1 to 6
            seat_number = random.randint(1, 6)

        # Combine the seat number and letter
        seat = str(seat_number) + seat_letter
        # Return the generated seat
        return seat

    def payment(self, total_price):
        """
        Handles the payment process for the order.
        Args: total_price: The total price of the reservation.
        """
        # Display the total reservation price to the user
        print(f"To complete the reservation, commit payment. Total reservation price is {total_price}")
        # Loop until a valid credit card number is entered
        while True:
            # Prompt the user to enter their credit card number
            cc = input("Please type your Credit Card number (digits only): ")
            # Validate the credit card number
            if validate_cc(cc):
                break

        # Check the length of the card number and validate the card issuer
        card_issuer = ""
        if len(cc) == 15 and cc[:2] in ['34', '37']:
            card_issuer = 'American Express'
        elif len(cc) == 16 and cc[:2] in ['51', '52', '53', '54', '55']:
            card_issuer = 'MasterCard'
        elif len(cc) in [13, 16] and cc[0] == '4':
            card_issuer = 'Visa'
        # Display the card issuer to the user
        print(f"Your card issuer is {card_issuer}")

        # Loop until a valid credit card expiration date is entered
        while True:
            # Prompt the user to enter their credit card expiration date
            cc_date = input("Please type your Credit Card expiration date (mm/yy): ")
            # Validate the credit card expiration date
            if validate_cc_date(cc_date):
                break

        # Loop until a valid CVV is entered
        while True:
            # Prompt the user to enter their CVV
            cvv = input("Please type your CVV: ")

            # Validate the CVV based on the card issuer
            if validate_cvv(cvv, card_issuer):
                break

        # Display a message indicating the completion of the reservation
        print("Reservation completed! Thank you for using our services")

    def update_order(self, order, total_price, num_of_travelers):
        """
        Updates the order details in the database and instance.
        Args:
            order (Order): The order object to update.
            total_price (float): The updated total price of the order.
            num_of_travelers (int): The updated number of tickets in the order
        """
        order.total_price = "$" + str(total_price)
        order.num_of_tickets = num_of_travelers

        conn = sqlite3.connect("big_data.db")
        cur = conn.cursor()

        # Execute the INSERT statement
        cur.execute("INSERT INTO orders (num_of_tickets, total_price) VALUES (?, ?)",
                    (order.num_of_tickets, order.total_price))
        # Commit the transaction to save the changes
        conn.commit()
        # Close the cursor and the connection
        cur.close()
        conn.close()

    def show_order(self, origin, destination, order_id, tick_num, tot_price):
        """
        Displays the order information.
        Args:
            origin: The origin of the flight.
            destination: The destination of the flight.
            order_id: The ID of the order.
            tick_num: The number of tickets in the order.
            tot_price: The total price of the order.
        """
        print(
            f"You are flying from {origin} to {destination}.\n"
            f"Order id is: {order_id}\n"
            f"Order has {tick_num} ticket\s \n"
            f"Order's total price for is: {tot_price}\n"
            f"Have a nice flight!"
        )
