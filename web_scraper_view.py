from web_scraper import WebScraper
import tkinter as tk
import json

f_airport = open('data/airport.json')
AIRPORT_DATA = json.load(f_airport)
CITIES = list(AIRPORT_DATA.keys())

def show_result():
    origin_ap = origin_var.get()
    destination_ap = destination_var.get()

    scraper = WebScraper(AIRPORT_DATA[origin_ap], AIRPORT_DATA[destination_ap])
    results = scraper.load_data()
    #Display results starting from the 4th row
    for idx, result in enumerate(results, start=4):
        price_result_label = tk.Label(window, text=result['Price'])
        price_result_label.grid(row=idx, column=0, pady=5)
        time_result_label = tk.Label(window, text=result['Time'])
        time_result_label.grid(row=idx, column=1, pady=5)
        airline_result_label = tk.Label(window, text=result['Airline'])
        airline_result_label.grid(row=idx, column=2, pady=5)


window = tk.Tk()
window.geometry('600x800')
window.title('AIRLINE PRICES SCRAPER')
airline_price_label = tk.Label(window, text="Airline Price", font=("Helvetica", 16))
airline_price_label.grid(row=0, column=0, columnspan=2, pady=10)

origin_var = tk.StringVar()
origin_label = tk.Label(window, text="ORIGIN:")
origin_label.grid(row=1, column=0, pady=5)
origin_options = CITIES
origin_dropdown = tk.OptionMenu(window, origin_var, *origin_options)
origin_dropdown.grid(row=1, column=1, pady=5)

destination_var = tk.StringVar()
destination_label = tk.Label(window, text="DESTINATION:")
destination_label.grid(row=1, column=2, pady=5)
destination_options = CITIES
destination_dropdown = tk.OptionMenu(window, destination_var, *destination_options)
destination_dropdown.grid(row=1, column=3, pady=5)


show_results_button = tk.Button(window, text="SHOW RESULTS", command=show_result)
show_results_button.grid(row=2, column=0, columnspan=4, pady=10)

price_label = tk.Label(window, text="PRICE")
price_label.grid(row=3, column=0, pady=5)
time_label = tk.Label(window, text="TIME")
time_label.grid(row=3, column=1, pady=5)
airline_label = tk.Label(window, text="AIRLINE")
airline_label.grid(row=3, column=2, pady=5)


window.mainloop()
