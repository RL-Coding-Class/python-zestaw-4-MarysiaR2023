import pandas as pd
import matplotlib.pyplot as plt
import requests
from zadanie_1.database import save_to_db, load_flight_data

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
    response = requests.get(url_data, timeout=60).json()
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
    save_to_db(flight_df, databasefile)
    print("Data saved to database successfully!")


# Odczyt danych i wygenerowanie wykresu z danych lotniczych
def plot_flight_data(databasefile="flights.db", show_plot=True):
    # Wczytaj dane lotnicze z bazy danych
    flight_df = load_flight_data(databasefile)
    # to bedzie obiekt typu DataFrame
    flight_df = flight_df.fillna('No Data')
    flight_df = flight_df[ (flight_df['velocity'] != 'No Data')
                          & (flight_df['geo_altitude'] != 'No Data') ]
    flight_df = flight_df.sort_values(by='velocity').drop_duplicates(subset='icao24', keep='first')
    x = flight_df['velocity']
    y = flight_df['geo_altitude']
    x = pd.to_numeric(x, downcast ='float', errors='coerce')
    y = pd.to_numeric(y, downcast ='float', errors='coerce')
    x = [(el*3.600) for el in x]
    y = [el/1000 for el in y]
    plt.scatter(x,y, color = 'royalblue', alpha=0.9)
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
