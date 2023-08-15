from exeptions import *
from order_management import *
from main_management import *
from user_management import *
from flights_management import *
import sys


def get_cur_user(process):
    """
    Prompts the user to create a new user or check if the user exists.
    Args: process (MainManagement): An instance of the MainManagement class.
    Returns: User: The current user.
    """
    while True:
        is_new = input("Do you have an account? (y/n): ")
        if is_new.lower() == 'n' or is_new.lower() == 'no':
            # Create new user instance
            cur_user = process.user_management.create_new_user()
            break
        elif is_new.lower() == 'y' or is_new.lower() == 'yes':
            # Loads an existing instance of user
            cur_user = process.user_management.check_if_user()
            if cur_user:
                break
    return cur_user


def get_num_of_travelers():
    """
    Prompts the user to enter the number of travelers.
    Returns: int: The number of travelers.
    """
    while True:
        num_of_travelers = input("How many travelers?: ")
        # Check if the input is a valid integer
        if is_int(num_of_travelers):
            break
    return int(num_of_travelers)


def get_cur_order(process, cur_user):
    """
    Prompts the user to create a new order or exit the script.
    Args: process (MainManagement): An instance of the MainManagement class. cur_user (User): The current user.
    Returns: Order: The current order.
    """
    while True:
        is_order = input("Do you want to open a new order? (y/n): ")
        if is_order.lower() == 'y' or is_order.lower() == 'yes':
            # Initiates a new order instance
            cur_order = process.order_management.create_new_order(cur_user.get_person_id())
            break
        # exit the program, if reservation is not opened
        elif is_order.lower() == 'n' or is_order.lower() == 'no':
            print("OK, see you next time")
            exit(1)
    return cur_order


def main():
    """
    The main function that runs the flight ticket reservation system.
    """
    # Create an instance of the MainManagement class
    process = MainManagement()  # Create an instance of the MainManagement class
    print("Hey! Welcome to the new friendly flight tickets reservation site")
    # Prompt the user to create a new user or check if the user exists and validates input
    cur_user = get_cur_user(process)

    print("Let's find the perfect flight for you")
    # Prompt the user to enter the number of travelers and validates input
    num_of_travelers = get_num_of_travelers()

    # Search for flights based on the number of travelers
    cur_flight = process.flights_management.search_for_flights(num_of_travelers)

    # Prompt the user to create a new order or exit the script
    cur_order = get_cur_order(process, cur_user)

    # Add details for each passenger
    # Add a ticket for each passenger and calculate the total price
    total_price = 0
    for passenger in range(1, num_of_travelers + 1):
        print(f"Please enter the details of passenger {passenger}")
        cur_pass = process.order_management.add_passenger()
        cur_ticket = process.order_management.add_ticket(pass_id=cur_pass.get_pass_id(),
                                                         flight_id=cur_flight.flight_code, price=cur_flight.price,
                                                         order_id=cur_order.order_id)
        total_price += int(cur_ticket.price[1:])

    # Process payment for the order
    process.order_management.payment("$" + str(total_price))
    # Update the order details
    process.order_management.update_order(order=cur_order, total_price=total_price, num_of_travelers=num_of_travelers)

    print(f"\nCongratulations {cur_user.first_name}")
    # Display the order details
    process.order_management.show_order(cur_flight.origin, cur_flight.destination, cur_order.order_id,
                                        cur_order.num_of_tickets, cur_order.total_price)

    return  # Close the main function


if __name__ == "__main__":
    main()

