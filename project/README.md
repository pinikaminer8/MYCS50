# Flights Management System
#### Video Demo:  <URL https://youtu.be/roGYClQ-8b4>
#### Description:

This is a Python project that simulates a system that allows you to register, search for flights and book tickets. The implementation is carried out through object-oriented programming and control of several databases.


The initial file for which an instance is created in the main program only once is the file *main_management.py*. In this file we have a class called **MainManagement** This file creates only once in its initialization configuration three additional managers: "user_management.py", "flights_management.py", "order_management.py".


In the *user_management* file we have **UserManagement** class that have multiply methodes:
- create_new_user (Allows the user to register to the system, Every new user is automatically logged into the database)
- check_if_user (If the user claims to have a registered user on the website, the method checks in the database whether this is indeed the case)
Each of the methods creates an instance of another class called "User" (This class inherits from a parent class called **Person** that has the attributes of a user which also bequeaths to the **Admin** class)


In the *flights_management* file we have **FlightManagement** class that have multiply methodes:
- search_for_flights (Searches for available flights, based on user input using the choose_flight method)
- flight_found (It looks for the requested flight in the database and returns an array of flights that meet the criteria)
- choose_flight (Allows the user to choose a flight from the list of available flights). This method creates an instance of another class called **Flight**


In the *order_management* file we have **OrderManagement** class that have multiply methodes:
- create_new_order (If the user so desires, the method creates an instance of an **Order**)
- add_passenger (Prompts the user to enter passenger details and creates a new **Passenger** object)
- add_ticket (Allows the user to select a class on the plane using the take_seat method, and adds a new **Ticket** object to the order)
- take_seat (Generates a seat number based on the given grade)
- payment (Handles the payment process for the order)
- update_order (Updates the order details in the database and instance)
- show_order (Displays the order information)


In the *exeptions.py* file we have mulitply classes that handles Exceptions and validates all program variables


In the file called *flights_base.db* there is a database based on past flights that is changed to future dates, which includes thousands of flights within the US


In the file called *big_data.db* there is a new database that we created. It will keep all the data on the users of the system, the passengers, the tickets and the orders. All information is stored in a separate tables within the database


Finally, the main run file called *main.py* that have multiply functions:
- get_cur_user (Prompts the user to create a new user or check if the user exists)
- get_num_of_travelers (Prompts the user to enter the number of travelers)
- get_cur_order (Prompts the user to create a new order or exit the script)

In the *main* function we run the entire program. Initially it creates a single instance of **MainManagement**, and from there it progress through the whole process using all the other classes above until the order is finished