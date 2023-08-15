import sqlite3
from flight import Flight
from exeptions import *


class FlightManagement:
    """
    Represents a flight management system with methods for searching and choosing flights.
    """

    def search_for_flights(self, num_of_travelers):
        """
        Searches for available flights based on user input.
        Args: num_of_travelers: The number of travelers.
        Returns: Flight: The chosen flight.
        """
        num_of_passengers = num_of_travelers

        is_available_flight = False
        while not is_available_flight:
            # Get origin and destination cities from user
            origin_city = input("From which city are you flying from?: ").title()
            destination_city = input("To which city are you flying to?: ").title()

            dep_date_status = False
            while not dep_date_status:
                # Get departure date from user and validate it
                departure_date = input("Please enter your departure date (yyyy/mm/dd): ")
                dep_date_status = validate_flight_date(departure_date)

            # Find available flights based on user input
            list_of_flights = self.flight_found(
                origin_city=origin_city,
                destination_city=destination_city,
                departure_date=departure_date,
                num_of_seats=num_of_passengers
            )

            if list_of_flights:
                is_available_flight = True
        # Choose a flight from the available options
        chosen_flight = self.choose_flight(list_of_flights)
        return chosen_flight

    def flight_found(self, origin_city, destination_city, departure_date, num_of_seats):
        """
        Searches for flights that match the given criteria.
        Args:
            origin_city (str): The origin city.
            destination_city (str): The destination city.
            departure_date (str): The departure date.
            num_of_seats (int): The number of seats needed.
        Returns: list: A list of flight codes and their indexes.
        """
        connection = sqlite3.connect("flights_base.db")
        cursor = connection.cursor()

        table_name = "Flights"

        # User input for search criteria
        flight_date = departure_date
        origin_city = origin_city
        dest_city = destination_city

        # Select rows that match the search criteria
        query = f"SELECT * FROM {table_name} WHERE FLIGHTDATE = ? AND ORIGINCITYNAME = ? AND DESTCITYNAME = ?"
        cursor.execute(query, (flight_date, origin_city, dest_city))
        rows = cursor.fetchall()

        for row in rows:
            seats_avail = row[16]
            if num_of_seats > seats_avail:
                print("There are not enough available seats in any of the flights")
                return False

        if rows:
            num_of_flights = len(rows)
            list_of_codes = []
            print()
            print(f"We have found {num_of_flights} flights for you")
            print()
            i = 0
            for row in rows:
                if num_of_seats < seats_avail:
                    i += 1
                    print(f"Flight number {i}")
                    print("Flight Details:")
                    print(f"Flight Date: {row[1]}")
                    print(f"Airline Name: {row[3]}")
                    print(f"Origin Airport: {row[6]}")
                    print(f"Destination Airport: {row[10]}")
                    print(f"Departure Time: {row[13][:-2] + ':' + row[13][-2:]}")
                    print(f"Arrival Time: {row[14][:-2] + ':' + row[14][-2:]}")
                    print(f"The price for this flight is: {row[17]}")
                    print()
                    print(
                        "---------------------------------------------------------------------------------------------------")
                    trans_code_id = (i, row[0])
                    list_of_codes.append(trans_code_id)

        connection.close()

        if rows:
            return list_of_codes
        else:
            print("We couldn't find a flight that matches your preferences. Let's try again")
            return False

    def choose_flight(self, list_of_flights):
        """
        Allows the user to choose a flight from the list of available flights.
        Args:  list_of_flights: A list of flight codes and their indexes.
        Returns: Flight: The chosen flight.
        """
        while True:
            print("Choose your preferred flight (type its number): ")
            chosen_i = input()
            if validate_choice(chosen_i, len(list_of_flights)):

                break
        chosen_code = list_of_flights[int(chosen_i) - 1][1]

        conn = sqlite3.connect('flights_base.db')
        cursor = conn.cursor()

        # Get the transaction ID of the chosen flight
        transaction_id = f'{chosen_code}'
        # Retrieve the flight details from the database
        cursor.execute("SELECT * FROM Flights WHERE TRANSACTIONID = ?", (transaction_id,))
        row = cursor.fetchone()

        if row:
            chosen_flight = row
            new_flight = Flight(flight_code=row[0], date=row[1], company=row[3])
            return new_flight
        else:
            print("There is a problem")
