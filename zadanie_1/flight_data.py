import pandas as pd
import matplotlib.pyplot as plt
import requests
from database import *

# Funkcja do pozyskania danych z OpenSky Network API
def fetch_flight_data(databasefile="flights.db"):
    # wspolrzedne ATL (Atlanta) w stopniach 
    lon_min, lat_min = -85.4277, 32.6407
    lon_max, lat_max = -83.4277, 34.6407
    # REST API QUERY
    url_data = (
   'https://'
   '@opensky-network.org/api/states/all?' +
   'lamin=' + str(lat_min) + '&lomin=' + str(lon_min) +
   '&lamax=' + str(lat_max) + '&lomax=' + str(lon_max)
)
    response = requests.get(url_data).json()
    to_data = response['states']
    col_name = [
    'icao24', 'callsign', 'origin_country', 'time_position', 'last_contact',
    'long', 'lat', 'baro_altitude', 'on_ground', 'velocity',
    'true_track', 'vertical_rate', 'sensors', 'geo_altitude',
    'squawk', 'spi', 'position_source'
    ]
    data = {}
    for i in range(len(col_name)):
        data[col_name[i]] = [el[i] for el in to_data]
    # napisz kod do pozyskania danych z OpenSky Network API, pamietaj o zalozeniu konta
    flight_df = pd.DataFrame(data)
    # Zapisz dane do bazy danych SQLite
    save_to_db(flight_df)
    print("Data saved to database successfully!")


# Odczyt danych i wygenerowanie wykresu z danych lotniczych
def plot_flight_data(databasefile="flights.db", show_plot=True):
    # Wczytaj dane lotnicze z bazy danych
    flight_df = load_flight_data()
    # to bedzie obiekt typu DataFrame
    
    # caly kod tutaj (filtracja, konwersja jednostek, sortowanie i wybieranie jednego, rysowanie wykresu)
    flight_df = flight_df.fillna('No Data')
    flight_df = flight_df[ (flight_df['velocity'] != 'No Data') & (flight_df['geo_altitude'] != 'No Data') ]
    flight_df = flight_df.sort_values(by='velocity').drop_duplicates(subset='icao24', keep='first')
    X = flight_df['velocity']
    Y = flight_df['geo_altitude']
    X = pd.to_numeric(X, downcast ='float', errors='coerce')
    Y = pd.to_numeric(Y, downcast ='float', errors='coerce')
    X = [(el*3.600) for el in X]
    Y = [el/1000 for el in Y]
    plt.scatter(X,Y, color = 'royalblue', alpha=0.9)
    plt.grid(True)
    plt.title("Aircraft Velocity vs. Geometric Altitude")
    plt.xlabel("Velocity (km/h)")
    plt.ylabel("Geometric Altitude (km)")
    plt.xlim((0,1200))
    plt.ylim((0,14))
    plt.tight_layout()
    # Wyświetlanie wykresu tylko, jeśli show_plot=True
    if show_plot:
        plt.show()
