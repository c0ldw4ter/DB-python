create database aviation;

CREATE TABLE aircraft_types (
   id SERIAL PRIMARY KEY,
   type_name VARCHAR(50) NOT NULL
);

CREATE TABLE countries (
   id SERIAL PRIMARY KEY,
   country_name VARCHAR(50) NOT NULL
);

CREATE TABLE suppliers (
   id SERIAL PRIMARY KEY,
   supplier_name VARCHAR(100) NOT NULL
);

CREATE TABLE aircrafts (
   id SERIAL PRIMARY KEY,
   type_id INTEGER REFERENCES public.aircraft_types(id),
   manufacture_year INTEGER NOT NULL,
   service_life INTEGER NOT NULL,
   manufacture_country_id INTEGER REFERENCES public.countries(id),
   supplier_id INTEGER REFERENCES public.suppliers(id),
   price NUMERIC(15,2) NOT NULL,
   speed INTEGER NOT NULL,
   capacity INTEGER NOT NULL,
   is_repaired BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE repairs (
   id SERIAL PRIMARY KEY,
   aircraft_id INTEGER REFERENCES public.aircrafts(id),
   repair_cost NUMERIC(15,2) NOT NULL,
   repair_date DATE NOT NULL
);


INSERT INTO aircraft_types (type_name) VALUES
('Passenger'),
('Cargo'),
('Military'),
('Private'),
('Helicopter'),
('Glider'),
('Amphibious'),
('Drone'),
('Electric'),
('Experimental');



INSERT INTO countries (country_name) VALUES
('USA'),
('Russia'),
('Germany'),
('France'),
('Japan'),
('China'),
('India'),
('Canada'),
('Brazil'),
('Australia');


INSERT INTO suppliers (supplier_name) VALUES
('Boeing'),
('Airbus'),
('Antonov'),
('Lockheed Martin'),
('Dassault Aviation'),
('Embraer'),
('Bombardier'),
('Mitsubishi Heavy Industries'),
('Sukhoi'),
('Textron Aviation');


INSERT INTO aircrafts (type_id, manufacture_year, service_life, manufacture_country_id, supplier_id, price, speed, capacity, is_repaired) VALUES
(1, 2010, 30, 1, 1, 8500000.00, 900, 200, TRUE),
(2, 2015, 25, 2, 2, 9500000.00, 800, 250, FALSE),
(3, 2020, 20, 3, 3, 12000000.00, 700, 100, TRUE),
(4, 2018, 15, 4, 4, 5000000.00, 650, 10, FALSE),
(5, 2012, 20, 5, 5, 3000000.00, 300, 20, TRUE),
(6, 2021, 10, 6, 6, 2000000.00, 250, 5, TRUE),
(7, 2017, 15, 7, 7, 7000000.00, 450, 50, FALSE),
(8, 2019, 10, 8, 8, 1000000.00, 200, 2, TRUE),
(9, 2022, 10, 9, 9, 4000000.00, 500, 30, FALSE),
(10, 2023, 5, 10, 10, 6000000.00, 550, 40, TRUE);


INSERT INTO repairs (aircraft_id, repair_cost, repair_date) VALUES
(1, 100000.00, '2023-01-15'),
(3, 200000.00, '2024-03-20'),
(5, 50000.00, '2023-07-10'),
(7, 150000.00, '2024-01-25'),
(10, 75000.00, '2023-06-30'),
(2, 120000.00, '2024-02-15'),
(4, 90000.00, '2023-09-10'),
(6, 30000.00, '2024-04-05'),
(8, 60000.00, '2023-11-15'),
(9, 110000.00, '2024-05-10');


INSERT INTO repairs (aircraft_id, repair_cost, repair_date) VALUES
(1, 5000.00, CURRENT_DATE - INTERVAL '3 months'),  -- Ремонт 3 месяца назад
(2, 7000.00, CURRENT_DATE - INTERVAL '5 months'),  -- Ремонт 5 месяцев назад
(3, 3000.00, CURRENT_DATE - INTERVAL '1 year'),     -- Ремонт 1 год назад
(4, 8000.00, CURRENT_DATE - INTERVAL '1 month'),    -- Ремонт 1 месяц назад
(5, 6000.00, CURRENT_DATE - INTERVAL '2 years');     -- Ремонт 2 года назад

-- Проверка данных в таблице aircraft_types
SELECT * FROM aircraft_types;

-- Проверка данных в таблице countries
SELECT * FROM countries;

-- Проверка данных в таблице suppliers
SELECT * FROM suppliers;

-- Проверка данных в таблице aircrafts
SELECT * FROM aircrafts;

-- Проверка данных в таблице repairs
SELECT * FROM repairs;



--Создание ролей
--db_admin
CREATE ROLE db_admin WITH LOGIN PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE aviation TO db_admin;
GRANT ALL ON ALL TABLES IN SCHEMA public TO db_admin;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public to db_admin;



--db_operator	
CREATE ROLE db_operator WITH LOGIN PASSWORD 'operator';
GRANT CONNECT ON DATABASE aviation TO db_operator;
GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA public TO db_operator;
GRANT USAGE,SELECT ON ALL SEQUENCES IN SCHEMA public TO db_operator;




--db_analyst
CREATE ROLE db_analyst WITH LOGIN PASSWORD 'analyst';
GRANT CONNECT ON DATABASE aviation TO db_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO db_analyst;





--db_user
CREATE ROLE db_user WITH LOGIN PASSWORD 'user';
GRANT CONNECT ON DATABASE aviation TO db_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO db_user;
