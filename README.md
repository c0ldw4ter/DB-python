### This code is written in Python for easy execution of complex PostgreSQL queries.
# To launch:
- Need to create database with all tables and roles, to do it you need to use file db.sql. DB must called "aviation"
- In project folder need to create python venv (~python -m venv venv)
- Download all dependencies(~pip install -r requirements.txt)
- Now you can run python script db.py

# Info about project^
- Key actions are logged
- Available options   
  - 1. “Information about each airplane.”
  - 2. “List by repair cost and service life”,
  - 3. “Percentage of airplanes repaired.”
  - 4. “Most expensive, cheapest and average cost of airplanes”,
  - 5. “Airplanes with price higher than a given price”,
  - 6. “Airplanes from a country with a given capacity”,
  - 7. “Number of airplanes with a given service life”,
  - 8. “Aircraft of a given type produced during the period and with a price within”,
  - 9. “Airplanes from a supplier with a price above the national average”,
  - 10. “Most expensive, cheapest repairs, average cost of repairs”,
  - 11. “Airplanes with repairs within given limits”,
  - 12. “Statistics of repairs for the last 6 months and year”,
  - 13. “Proportion of low-cost airplanes by repair cost”,
  - 14. “Aircraft with a given service life and price above the average by capacity”,
  - 15. “Airplanes with a given speed and price above the supplier average”,
  - 16. “Inserting data in the program”,
  - 17. “Exit”.
- Available roles:
  
  - Role:
  - 1. db_admin
  - 2. Permissions:
  - 3. Full access: create, modify, delete objects.

  - Role:
  - 1. db_operator
  - 2. Permissions:
  - 3. Read, add, edit and delete data.

  - Role:
  - 1. db_analyst
  - 2. Permissions:
  - 3. Read data only.

  - Role:
  - 1. db_user
  - 2. Permissions:
  - 3. Only read data from the main table (aviation), no access to all other helper tables
  
