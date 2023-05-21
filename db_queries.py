import random

import psycopg2
#
# # Connect to the PostgreSQL database
# conn = psycopg2.connect(host='localhost', port=5432, database='demo', user='moshe', password='password')
#
# # Create tables
# with conn.cursor() as cursor:
#     # Create spaceships table
#     cursor.execute("""
#         CREATE TABLE spaceships (
#             spaceship_id SERIAL PRIMARY KEY,
#             name VARCHAR(255),
#             manufacturer VARCHAR(255),
#             year INTEGER,
#             max_speed INTEGER
#         )
#     """)
#
#     # Create crew_members table with foreign key to spaceships table
#     cursor.execute("""
#         CREATE TABLE crew_members (
#             crew_member_id SERIAL PRIMARY KEY,
#             name VARCHAR(255),
#             rank VARCHAR(255),
#             spaceship_id INTEGER REFERENCES spaceships(spaceship_id)
#         )
#     """)
#
#     # Create flights table with foreign key to spaceships table
#     cursor.execute("""
#         CREATE TABLE flights (
#             flight_id SERIAL PRIMARY KEY,
#             spaceship_id INTEGER REFERENCES spaceships(spaceship_id),
#             start_date DATE,
#             end_date DATE,
#             destination VARCHAR(255)
#         )
#     """)
#
#     # Create passengers table with foreign key to flights table
#     cursor.execute("""
#         CREATE TABLE passengers (
#             passenger_id SERIAL PRIMARY KEY,
#             name VARCHAR(255),
#             flight_id INTEGER REFERENCES flights(flight_id)
#         )
#     """)
#
# # Populate tables with random data
# with conn.cursor() as cursor:
#     # Generate random data for spaceships table
#     spaceship_data = []
#     for i in range(10):
#         name = f"Spaceship {i + 1}"
#         manufacturer = f"Manufacturer {i + 1}"
#         year = random.randint(2000, 2023)
#         max_speed = random.randint(100, 1000)
#         spaceship_data.append((name, manufacturer, year, max_speed))
#
#     # Insert random data into spaceships table
#     cursor.executemany(
#         "INSERT INTO spaceships (name, manufacturer, year, max_speed) VALUES (%s, %s, %s, %s)",
#         spaceship_data
#     )
#
#     # Generate random data for crew_members table
#     crew_member_data = []
#     for i in range(20):
#         name = f"Crew Member {i + 1}"
#         rank = random.choice(["Captain", "First Officer", "Engineer", "Navigator", "Pilot"])
#         spaceship_id = random.randint(1, 10)
#         crew_member_data.append((name, rank, spaceship_id))
#
#     # Insert random data into crew_members table
#     cursor.executemany(
#         "INSERT INTO crew_members (name, rank, spaceship_id) VALUES (%s, %s, %s)",
#         crew_member_data
#     )
#
#     # Generate random data for flights table
#     flight_data = []
#     for i in range(100):
#         spaceship_id = random.randint(1, 10)
#         start_date = f"2023-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
#         end_date = f"2023-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
#         destination = random.choice(["Mars", "Jupiter", "Saturn"])
#         flight_data.append((spaceship_id, start_date, end_date, destination))
#
#     # Insert random data into flights table
#     cursor.executemany(
#         "INSERT INTO flights (spaceship_id, start_date, end_date, destination) VALUES (%s, %s, %s, %s)",
#         flight_data
#     )
#
#     # Generate random data for passengers table
#     passenger_data = []
#     for i in range(200):
#         name = f"Passenger {i + 1}"
#         flight_id = random.randint(1, 100)
#         passenger_data.append((name, flight_id))
#
#     # Insert random data into passengers table
#     cursor.executemany(
#         "INSERT INTO passengers (name, flight_id) VALUES (%s, %s)",
#         passenger_data
#     )
#
# # Commit the changes and close the connection
# conn.commit()
# conn.close()


def exec_query(conn: psycopg2._connect, query: str) -> str:
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def extract_table_metadata(conn: psycopg2._connect) -> str:
    metadata = []
    cursor = conn.cursor()

    # Get list of table names
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        metadata.append(f"Table: {table_name} \n")

        # Get column metadata
        cursor.execute(
            f"""
            SELECT
                c.column_name,
                c.data_type,
                CASE
                    WHEN c.column_name IN (
                        SELECT kcu.column_name
                        FROM information_schema.key_column_usage AS kcu
                        JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = kcu.constraint_name
                        WHERE kcu.table_name = '{table_name}' AND kcu.constraint_name LIKE '%_pkey'
                    ) THEN 'PK'
                    WHEN c.column_name IN (
                        SELECT kcu.column_name
                        FROM information_schema.key_column_usage AS kcu
                        JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = kcu.constraint_name
                        WHERE kcu.table_name = '{table_name}' AND kcu.constraint_name LIKE '%_fkey'
                    ) THEN 'FK: ' || (
                        SELECT ccu.table_name || '.' || ccu.column_name
                        FROM information_schema.key_column_usage AS kcu
                        JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = kcu.constraint_name
                        WHERE kcu.table_name = '{table_name}' AND kcu.column_name = c.column_name
                    )
                    ELSE ''
                END AS constraint_info
            FROM
                information_schema.columns AS c
            WHERE
                c.table_name = '{table_name}'
            """)
        columns = cursor.fetchall()
        for column in columns:
            column_name = column[0]
            data_type = column[1]
            constraint_type = column[2]
            metadata.append(f"- Column: {column_name}, Data Type: {data_type}, Constraint: {constraint_type} \n")

    cursor.close()
    return ''.join(metadata)
