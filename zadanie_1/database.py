import sqlite3
import pandas as pd

def create_table(max_repeats, databasefile="flights.db"):
    # podlacz baze danych SQLite
    connection = sqlite3.connect(databasefile)
    cursor = connection.cursor()
    # proponowane podejscie: jesli parametr 0, nic nie rob
    # jesli wiekszy od 0, usun tabele i utworz nowa
    if max_repeats > 0:
        cursor.execute('''DROP TABLE IF EXISTS airport_atl''')
        cursor.execute(
    '''CREATE TABLE airport_atl (
        icao24 TEXT,
        callsign TEXT,
        origin_country TEXT,
        time_position TEXT,
        last_contact TEXT,
        long REAL,
        lat REAL,
        baro_altitude REAL,
        on_ground TEXT,
        velocity REAL,
        true_track REAL,
        vertical_rate REAL,
        sensors TEXT,
        geo_altitude REAL,
        squawk TEXT,
        spi TEXT,
        position_source INTEGER
    )'''
        )
        connection.commit()
    connection.close()
    # zamknij polaczenie z baza danych
    


def save_to_db(flight_df, databasefile="flights.db"):
    # napisz kod zapisania do bazy danych SQLite
    connection = sqlite3.connect("flights.db")
    flight_df.to_sql("airport_atl", connection, if_exists="append", index=False)
    connection.close()

def load_flight_data(databasefile="flights.db"):
    # napisz kod odczytania danych z bazy danych SQLite
    conn = sqlite3.connect(databasefile)
    flight_df = pd.read_sql_query("SELECT * FROM airport_atl", conn)
    conn.close()
    return flight_df