import datetime

import pandas as pd
from web_scraper import WebScraper
import tkinter as tk
from tkcalendar import Calendar
import json
from datetime import date
import os

f_airport = open('data/airport.json')
AIRPORT_DATA = json.load(f_airport)
CITIES = list(AIRPORT_DATA.keys())
#SELECTED_COUNTRIES = ['Poland','Philippines','Germany','Italy','France','Spain','Japan','Singapore']
all_airport_data = pd.read_csv('data/airport_volume_airport_locations.csv')

def show_result():
    origin_ap = origin_var.get()
    destination_ap = destination_var.get()
    selected_date = date_var.get()

    if destination_ap == 'ALL':
        results = []
        for i in CITIES:
            if AIRPORT_DATA[origin_ap] != AIRPORT_DATA[i] and i != 'ALL':
                scraper = WebScraper(AIRPORT_DATA[origin_ap], AIRPORT_DATA[i], selected_date)
                result = scraper.load_data()
                print(result)
                export_to_csv(result)
    else:
        scraper = WebScraper(AIRPORT_DATA[origin_ap], AIRPORT_DATA[destination_ap], selected_date)
        results = scraper.load_data()
        export_to_csv(results)
    #Display results starting from the 4th row
    for idx, result in enumerate(results, start=5):
        price_result_label = tk.Label(window, text=result['Price(USD)'])
        price_result_label.grid(row=idx, column=0, pady=5)
        time_result_label = tk.Label(window, text=result['Time'])
        time_result_label.grid(row=idx, column=1, pady=5)
        airline_result_label = tk.Label(window, text=result['Airline'])
        airline_result_label.grid(row=idx, column=2, pady=5)

def export_to_csv(result):
    df = pd.DataFrame(result)
    df['Origin Name'] = df['Origin'].apply(lambda origin: all_airport_data.loc[all_airport_data['Orig'] == origin].iloc[0]['Name'])
    df['Origin Country'] = df['Origin'].apply(
        lambda origin: all_airport_data.loc[all_airport_data['Orig'] == origin].iloc[0]['Country Name'])
    df['Destination Name'] = df['Destination'].apply(lambda origin: all_airport_data.loc[all_airport_data['Orig'] == origin].iloc[0]['Name'])
    df['Destination Country'] = df['Destination'].apply(
        lambda origin: all_airport_data.loc[all_airport_data['Orig'] == origin].iloc[0]['Country Name'])
    saved_df = df.loc[:, ['Airline','Departure Date','Time','Price(USD)','Origin','Origin Name', 'Origin Country', 'Destination', 'Destination Name','Destination Country']]
    if not os.path.isfile('data/airline_prices.csv'):
        print('New file mode')
        saved_df.to_csv('data/airline_prices.csv', index=False)
    else:
        print('append mode')
        saved_df.to_csv('data/airline_prices.csv', mode='a', header=False, index=False)

def export_all():
    df = pd.read_csv('data/airport_volume_airport_locations.csv')
    #country_list = df[df['Country Name'].isin(SELECTED_COUNTRIES)]['Orig']
    country_list = []
    results = []
    for origin in AIRPORT_DATA.values():
        for destination in AIRPORT_DATA.values():
            if origin != destination:
                scraper = WebScraper(origin, destination, '2024-01-14')
                result = scraper.load_data()
                results.append(result)
    export_to_csv(results)


window = tk.Tk()
window.geometry('800x1000')
window.title('AIRLINE PRICES SCRAPER')
airline_price_label = tk.Label(window, text="Airline Price", font=("Helvetica", 16))
airline_price_label.grid(row=0, column=0, columnspan=2, pady=10)

date_var = tk.StringVar()
date_var.set(value=date.today() + datetime.timedelta(days=1))
date_label = tk.Label(window, textvariable=date_var)
date_label.grid(row=1, column=1, columnspan=2, pady=10, padx=10)
calendar = Calendar(window, selectmode='day', textvariable=date_var, date_pattern='yyyy-mm-dd', mindate=date.today() + datetime.timedelta(days=1))
calendar.grid(row=1, column=3, columnspan=2, pady=10)

selected_date_label = tk.Label(window, text='Selected Date: ')
selected_date_label.grid(row=1, column=0, columnspan=2, pady=10)

origin_var = tk.StringVar()
origin_label = tk.Label(window, text="ORIGIN:")
origin_label.grid(row=2, column=0, pady=5, padx=10)
origin_options = CITIES
origin_dropdown = tk.OptionMenu(window, origin_var, *origin_options)
origin_dropdown.config(width=20)
origin_dropdown.grid(row=2, column=1, pady=5, padx=10)

destination_var = tk.StringVar()
destination_label = tk.Label(window, text="DESTINATION:")
destination_label.grid(row=2, column=2, pady=5, padx=10)
destination_options = list(CITIES)
destination_options.append('ALL')
destination_dropdown = tk.OptionMenu(window, destination_var, *destination_options)
destination_dropdown.config(width=20)
destination_dropdown.grid(row=2, column=3, pady=5, padx=10)

show_results_button = tk.Button(window, text="SHOW RESULTS", command=show_result)
show_results_button.grid(row=3, column=0, columnspan=4, pady=10)

price_label = tk.Label(window, text="PRICE(USD)")
price_label.grid(row=4, column=0, pady=5)
time_label = tk.Label(window, text="TIME")
time_label.grid(row=4, column=1, pady=5)
airline_label = tk.Label(window, text="AIRLINE")
airline_label.grid(row=4, column=2, pady=5)


window.mainloop()
