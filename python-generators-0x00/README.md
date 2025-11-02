# Python Generators – Seeding MySQL Data

## Description
This project connects to a MySQL database, creates a database `ALX_prodev`, sets up a table `user_data`, and populates it with records from a CSV file. It also prepares functionality for streaming rows using generators.

## Files
- seed.py — Handles MySQL connection setup, database creation, table creation, and data insertion.
- 0-main.py — Entry script for running seeding operations.
- user_data.csv — Source file containing sample user data.

## Usage
1. Ensure MySQL server is running.
2. Update MySQL credentials in `seed.py`.
3. Run:

chmod +x 0-main.py
./0-main.py

Expected output:

connection successful
Table user_data created successfully
Database ALX_prodev is present
[(uuid, name, email, age), ...]


## Next Step
Implement a generator function that streams rows from the `user_data` table one by one efficiently.