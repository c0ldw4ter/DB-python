import psycopg2
import logging
from prettytable import PrettyTable
from datetime import datetime, timedelta

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename="aviation.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

def connect_to_db():
    """Подключение к базе данных."""
    try:

"""
username:password

db_admin: admin;
db_operator: operator;
db_analyst: analyst;
db_user: user



Роль:
db_admin
Права:
Полный доступ: создание, изменение, удаление объектов.


Роль:
db_operator
Права:
Чтение, добавление, редактирование и удаление данных.

Роль:
db_analyst
Права:
Только чтение данных.

Роль:
db_user
Права:
Только чтение данных из основной таблицы(aviation), нет доступа ко всем другим всмпомогательным таблицам

"""

        user = "db_admin"
        passwd = 'admin'  
        conn = psycopg2.connect(
            dbname="aviation",
            user=user,
            password=passwd,
            host="localhost",
            port="5432"
        )
        logging.info(f"Успешное подключение к базе данных пользователем: {user}")
        return conn
    except Exception as e:
        logging.error(f"Ошибка подключения к базе данных: {e}")
        print("Ошибка подключения к базе данных. Проверьте лог.")
        return None


def execute_query(conn, query, params=None):
    """Выполняет запрос и возвращает результат."""
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if query.strip().lower().startswith("select"):
                colnames = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                return colnames, rows
            else:
                conn.commit()
                return "Запрос выполнен успешно."
    except Exception as e:
        logging.error(f"Ошибка выполнения запроса: {e}")
        print("Ошибка выполнения запроса. Проверьте лог")
        return None

def insert_data(conn):
    """Вставка данных в таблицы через интерфейс."""
    print("\n--- Вставка данных в таблицы ---")
    print("Доступные таблицы для вставки:")
    print("1. aircraft_types - Типы самолётов")
    print("2. countries - Страны")
    print("3. suppliers - Поставщики")
    print("4. aircrafts - Самолёты")
    print("5. repairs - Ремонты")

    table_choice = input("Выберите таблицу для вставки (1-5): ")

    queries = {
        '1': ("INSERT INTO aircraft_types (type_name) VALUES (%s);", "Введите тип самолёта: ", "aircraft_types"),
        '2': ("INSERT INTO countries (country_name) VALUES (%s);", "Введите название страны: ", "countries"),
        '3': ("INSERT INTO suppliers (supplier_name) VALUES (%s);", "Введите имя поставщика: ", "suppliers"),
        '4': ("""
            INSERT INTO aircrafts (type_id, manufacture_year, service_life, manufacture_country_id, supplier_id, price, speed, capacity, is_repaired)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, [
            "Введите ID типа самолёта: ",
            "Введите год выпуска: ",
            "Введите срок эксплуатации (в годах): ",
            "Введите ID страны: ",
            "Введите ID поставщика: ",
            "Введите цену самолёта: ",
            "Введите скорость (км/ч): ",
            "Введите вместимость: ",
            "Отремонтирован? (yes/no): "
        ], "aircrafts"),
        '5': ("INSERT INTO repairs (aircraft_id, repair_cost, repair_date) VALUES (%s, %s, %s);", [
            "Введите ID самолёта: ",
            "Введите стоимость ремонта: ",
            "Введите дату ремонта (YYYY-MM-DD): "
        ], "repairs")
    }

    if table_choice in queries:
        query, prompts, table_name = queries[table_choice]
        if isinstance(prompts, str):
            params = (input(prompts),)
        else:
            params = []
            for prompt in prompts:
                if prompt.endswith("? (yes/no): "):
                    response = input(prompt).strip().lower()
                    params.append(response == "yes")
                else:
                    params.append(input(prompt))
            params = tuple(params)

        result = execute_query(conn, query, params)
        logging.info(f"Вставка данных в таблицу: {table_name}")  
        print("Результат вставки:", result)
    else:
        print("Некорректный выбор.")

def display_results(results):
    """Читабельный вывод результатов запроса."""
    if not results:
        print("Нет данных для отображения.")
        return
    if isinstance(results, str):
        print(results)
        return
    colnames, rows = results
    table = PrettyTable(colnames)
    for row in rows:
        formatted_row = [float(val) if isinstance(val, (int, float)) else val for val in row]
        table.add_row(formatted_row)
    print(table)

def menu():
    """Выводит меню для выбора действий."""
    print("\n--- Меню ---")
    options = [
        "Сведения о каждом самолёте",
        "Список по стоимости ремонта и сроку эксплуатации",
        "Доля отремонтированных самолётов",
        "Самый дорогой, дешевый и средняя стоимость самолётов",
        "Самолёты с ценой выше заданной",
        "Самолёты из страны с заданной вместимостью",
        "Количество самолётов с заданным сроком эксплуатации",
        "Самолёты заданного типа, выпущенные за период и с ценой в пределах",
        "Самолёты от поставщика с ценой выше средней по стране",
        "Самый дорогой, дешевый ремонт, средняя стоимость ремонта",
        "Самолёты с ремонтом в заданных пределах",
        "Статистика ремонтов за последние 6 месяцев и год",
        "Доля дешёвых самолётов по стоимости ремонта",
        "Самолёты с заданным сроком эксплуатации и ценой выше средней по вместимости",
        "Самолёты с заданной скоростью и ценой выше средней по поставщику",
        "Вставка данных в программе",
        "Выход"
    ]
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    choice = input("Выберите действие (1-17): ")
    return int(choice) if choice.isdigit() and 1 <= int(choice) <= 17 else None

def handle_query_choice(choice, conn):
    """Обрабатывает выбор пользователя и выполняет соответствующий запрос."""
    query = ""
    params = None

    if choice == 1:
        query = """
        SELECT at.type_name AS aircraft_type,
               a.manufacture_year AS year,
               a.service_life AS life_years,
               c.country_name AS country,
               s.supplier_name AS supplier,
               ROUND(a.price, 2) AS price,
               a.speed AS speed_kmh,
               a.capacity AS capacity,
               a.is_repaired AS repaired,
               COALESCE(ROUND(r.repair_cost, 2), 0) AS repair_cost
        FROM aircrafts a
        LEFT JOIN aircraft_types at ON a.type_id = at.id
        LEFT JOIN countries c ON a.manufacture_country_id = c.id
        LEFT JOIN suppliers s ON a.supplier_id = s.id
        LEFT JOIN repairs r ON a.id = r.aircraft_id;
        """
    elif choice == 2:
        query = """
        SELECT at.type_name AS aircraft_type,
               a.service_life AS life_years,
               COALESCE(ROUND(r.repair_cost, 2), 0) AS repair_cost
        FROM aircrafts a
        LEFT JOIN aircraft_types at ON a.type_id = at.id
        LEFT JOIN repairs r ON a.id = r.aircraft_id
        ORDER BY r.repair_cost DESC, a.service_life DESC;
        """

            # query = """
            # SELECT at.type_name AS aircraft_type,
            #        a.service_life AS life_years,
            #        COALESCE(ROUND(r.repair_cost, 2), 0) AS repair_cost
            # FROM aircrafts a
            # LEFT JOIN aircraft_types at ON a.type_id = at.id
            # LEFT JOIN repairs r ON a.id = r.aircraft_id
            # ORDER BY a.service_life DESC;


            # SELECT at.type_name AS aircraft_type,
            #        a.service_life AS life_years,
            #        COALESCE(ROUND(r.repair_cost, 2), 0) AS repair_cost
            # FROM aircrafts a
            # LEFT JOIN aircraft_types at ON a.type_id = at.id
            # LEFT JOIN repairs r ON a.id = r.aircraft_id
            # ORDER BY r.repair_cost DESC;
            # """
    elif choice == 3:
        query = """
        SELECT ROUND(100.0 * SUM(CASE WHEN a.is_repaired THEN 1 ELSE 0 END) / COUNT(*), 2) AS repaired_percentage
        FROM aircrafts a;
        """
    elif choice == 4:
        query = """
        SELECT ROUND(MAX(a.price), 2) AS max_price,
               ROUND(MIN(a.price), 2) AS min_price,
               ROUND(AVG(a.price), 2) AS avg_price
        FROM aircrafts a;
        """
    elif choice == 5:
        min_price = float(input("Введите минимальную стоимость самолёта (например, 100000): "))
        query = """
        SELECT at.type_name AS aircraft_type,
               a.manufacture_year AS year,
               c.country_name AS country,
               ROUND(a.price, 2) AS price
        FROM aircrafts a
        LEFT JOIN aircraft_types at ON a.type_id = at.id
        LEFT JOIN countries c ON a.manufacture_country_id = c.id
        WHERE a.price > %s;
        """
        params = (min_price,)
    elif choice == 6:
        country = input("Введите страну (например, Russia): ")
        min_capacity = int(input("Введите минимальную вместимость (например, 50): "))
        query = """
        SELECT at.type_name AS aircraft_type,
               c.country_name AS country,
               a.capacity AS capacity,
               ROUND(a.price, 2) AS price
        FROM aircrafts a
        LEFT JOIN aircraft_types at ON a.type_id = at.id
        LEFT JOIN countries c ON a.manufacture_country_id = c.id
        WHERE c.country_name = %s AND a.capacity > %s;
        """
        params = (country, min_capacity)
    elif choice == 7:
        service_life = int(input("Введите срок эксплуатации (в годах, например, 20): "))
        query = """
        SELECT COUNT(*) AS total_aircrafts
        FROM aircrafts
        WHERE service_life = %s;
        """
        params = (service_life,)
    elif choice == 8:
        aircraft_type = input("Введите тип самолёта (например, Cargo): ")
        start_year = int(input("Введите начальный год (например, 2000): "))
        end_year = int(input("Введите конечный год (например, 2020): "))
        min_price = float(input("Введите минимальную стоимость (например, 15000): "))
        max_price = float(input("Введите максимальную стоимость (например, 3000000): "))
        query = """
        SELECT at.type_name AS aircraft_type,
               a.manufacture_year AS year,
               ROUND(a.price, 2) AS price
        FROM aircrafts a
        LEFT JOIN aircraft_types at ON a.type_id = at.id
        WHERE at.type_name = %s AND a.manufacture_year BETWEEN %s AND %s
          AND a.price BETWEEN %s AND %s;
        """
        params = (aircraft_type, start_year, end_year, min_price, max_price)
    elif choice == 9:
        supplier = input("Введите поставщика (например, Boeing): ")
        country = input("Введите страну (например, Russia): ")
        query = """
        SELECT at.type_name AS aircraft_type,
               a.price AS price
        FROM aircrafts a
        LEFT JOIN aircraft_types at ON a.type_id = at.id
        LEFT JOIN suppliers s ON a.supplier_id = s.id
        WHERE s.supplier_name = %s
          AND a.price > (SELECT AVG(price) FROM aircrafts a2
                         LEFT JOIN countries c ON a2.manufacture_country_id = c.id
                         WHERE c.country_name = %s);
        """
        params = (supplier, country)
    elif choice == 10:
        query = """
        SELECT ROUND(MAX(repair_cost), 2) AS max_repair_cost,
               ROUND(MIN(repair_cost), 2) AS min_repair_cost,
               ROUND(AVG(repair_cost), 2) AS avg_repair_cost
        FROM repairs;
        """
    elif choice == 11:
        min_cost = float(input("Введите минимальную стоимость ремонта (например, 300): "))
        max_cost = float(input("Введите максимальную стоимость ремонта (например, 700): "))
        query = """
        SELECT a.id AS aircraft_id,
               ROUND(r.repair_cost, 2) AS repair_cost
        FROM repairs r
        LEFT JOIN aircrafts a ON r.aircraft_id = a.id
        WHERE r.repair_cost BETWEEN %s AND %s;
        """
        params = (min_cost, max_cost)
    elif choice == 12:
       six_months_ago = datetime.now() - timedelta(days=182)
       one_year_ago = datetime.now() - timedelta(days=365)
       query = """
       SELECT COUNT(*) FILTER (WHERE repair_date >= %s) AS repairs_last_6_months,
       COUNT(*) FILTER (WHERE repair_date >= %s) AS repairs_last_year
       FROM repairs;
       """
       params = (six_months_ago, one_year_ago)
    elif choice == 13:
        threshold = float(input("Введите пороговую стоимость ремонта (например, 50000): "))
        query = """
        SELECT ROUND(COUNT(*) FILTER (WHERE repair_cost < %s) * 100.0 / COUNT(*), 2) AS percentage
        FROM repairs;   
        """
        params = (threshold,)
    elif choice == 14:
        service_life = int(input("Введите срок эксплуатации (например, 20): "))
        capacity = int(input("Введите вместимость (например, 200): "))
        query = """
        SELECT at.type_name AS aircraft_type,
               ROUND(a.price, 2) AS price
        FROM aircrafts a
        LEFT JOIN aircraft_types at ON a.type_id = at.id
        WHERE a.service_life = %s AND a.price > (SELECT AVG(price) FROM aircrafts WHERE capacity > %s);
        """
        params = (service_life, capacity)
    elif choice == 15:
        speed = float(input("Введите скорость самолёта (например, 900): "))
        supplier = input("Введите поставщика (например, Boeing Corporation): ")
        query = """
        SELECT at.type_name AS aircraft_type,
               ROUND(a.price, 2) AS price
        FROM aircrafts a
        LEFT JOIN aircraft_types at ON a.type_id = at.id
        WHERE a.speed = %s
          AND a.price > (SELECT AVG(price) FROM aircrafts
                            WHERE supplier_id = (SELECT id FROM suppliers WHERE supplier_name = %s));
        """
        params = (speed, supplier)
    elif choice == 16:
        insert_data(conn)
        return  
    else:
        print("Некорректный выбор.")
        return

    results = execute_query(conn, query, params)
    display_results(results)

def main():
    conn = connect_to_db()
    if not conn:
        return

    try:
        while True:
            choice = menu()
            if choice == 17:
                print("Выход из программы.")
                break
            handle_query_choice(choice, conn)
    finally:
        conn.close()
        logging.info("Отключение от базы данных")

if __name__ == "__main__":
    main()