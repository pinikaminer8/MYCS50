-- First we will check all the data from the known date of the event on the known street of the event
SELECT * FROM crime_scene_reports WHERE street = 'Humphrey Street' AND month = 7 AND day = 28;
--Result:
--Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
--Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.


-- We will check the interviews from this day
SELECT transcript FROM interviews WHERE month = 7 AND day = 28;
--Result:
--1:
--  "...I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money."
--2:
--   "As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say
--    that they were planning to take the earliest flight out of Fiftyville tomorrow..."


--We know from the interviews where the thief spent money and that he made a call to someone during that day.
--This can give us a narrow suspect list of call recipients from the same profile
--We will make a table:
CREATE TABLE suspects_received
AS
SELECT * FROM people WHERE phone_number IN (
SELECT receiver FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60 AND caller IN(
SELECT phone_number FROM people WHERE id in(
SELECT person_id FROM bank_accounts WHERE account_number IN (
SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
))));


--We know from the interviews where the thief spent money and that he made a call to someone during that day.
--This can give us a narrow suspect list of callers matching that profile
--We will make a table :
CREATE TABLE suspects_called
AS
SELECT * FROM people WHERE phone_number IN (
SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60 AND caller IN(
SELECT phone_number FROM people WHERE id in(
SELECT person_id FROM bank_accounts WHERE account_number IN (
SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
))));


--We will find the earliest flight the next day that, according to the evidence, the thief flew on
CREATE TABLE earliest_flight
AS
SELECT * FROM flights
JOIN airports ON flights.origin_airport_id = airports.id
WHERE month = 7 AND day = 29 AND origin_airport_id IN(
SELECT id FROM airports WHERE city = 'Fiftyville')
ORDER BY flights.hour LIMIT 1;


--Find the destination of the flight
SELECT city FROM airports WHERE id = (
SELECT destination_airport_id FROM earliest_flight);


--We will find the name of the person who received the call and was on the bakery parking and he is the accomplice
CREATE TABLE accomplice
AS
SELECT name, phone_number FROM people WHERE phone_number IN (
SELECT phone_number FROM suspects_received)
AND name IN (
SELECT name FROM people WHERE license_plate IN (
SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND activity = 'exit'));


----We will find the name of the person who called and was on the plane and he is the thief
SELECT name FROM people WHERE phone_number IN (
SELECT phone_number FROM suspects_called)
AND passport_number IN(
SELECT passport_number FROM passengers WHERE flight_id IN(
SELECT id FROM earliest_flight))
AND phone_number IN (
SELECT caller FROM phone_calls WHERE receiver IN (
SELECT phone_number FROM accomplice));
