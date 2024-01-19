import os
import pandas as pd

SELECTED_CITIES = {'Netherlands': 'Amsterdam', 'Greece': 'Athens', 'Thailand': 'Bangkok',
                       'Germany': 'Berlin', 'Belgium': 'Brussels','Belize': 'Belize', 'Argentina': 'Buenos Aires',
                       'South Africa': 'Cape Town', 'Denmark': 'Copenhagen', 'Ireland': 'Dublin',
                       'Hong Kong(SAR)': 'Hong Kong(SAR)', 'Turkey': 'Istanbul', 'Portugal': 'Lisbon',
                       'United Kingdom': 'London', 'Spain': 'Madrid', 'Malta': 'Malta', 'Mexico': 'Mexico City',
                       'United States': 'New York', 'Norway': 'Oslo', 'France': 'Paris', 'Czech Republic': 'Prague',
                       'Latvia': 'Riga', 'Brazil': 'Rio De Janeiro', 'Italy': 'Rome','Chile':'Santiago', 'Singapore': 'Singapore',
                       'Sweden': 'Stockholm', 'Australia': 'Sydney', 'Taiwan': 'Taipei', 'Japan': 'Tokyo',
                       'Canada': 'Vancouver', 'Austria': 'Vienna', 'Switzerland': 'Zurich'}

PRICE_CONVERSION = {'Netherlands': 1.09, 'Greece': 1.09, 'Thailand': 0.029,
                       'Germany': 1.09, 'Belgium': 1.09, 'Argentina': 0.0012,
                       'South Africa': 0.054, 'Denmark': 0.15, 'Ireland': 1.09,
                       'Hong Kong(SAR)': 0.13, 'Turkey': 0.033, 'Portugal': 1.09,
                       'United Kingdom': 1.27, 'Spain': 1.09, 'Malta': 1.09, 'Mexico': 0.059,
                       'United States': 1, 'Norway': 0.097, 'France': 1.09, 'Czech Republic': 0.044,
                       'Latvia': 1.09, 'Brazil': 0.21, 'Italy': 1.09, 'Singapore': 0.75,
                       'Sweden': 0.097, 'Australia': 0.67, 'Taiwan': 0.032, 'Japan': 0.0069,
                       'Canada': 0.74, 'Austria': 1.09, 'Switzerland': 1.17, 'Chile': 0.0011, 'Belize': 0.50}

file_list = os.listdir('data/airbnb/')
results = []
for file in file_list:
    df = pd.read_csv('data/airbnb/' + file)
    result = {}
    result['City'] = file.split('.')[0]
    result['Country'] =  [i for i in SELECTED_CITIES if SELECTED_CITIES[i]==result['City']][0]
    result['Average Price'] = round(df['price'].mean(), 2)
    result['Average Price in USD'] = round(PRICE_CONVERSION[result['Country']] * result['Average Price'], 2)
    results.append(result)

other_prices = pd.read_csv('data/Others.csv')
price_data = pd.DataFrame(results)
price_data = pd.concat([price_data, other_prices])
min_price = price_data['Average Price in USD'].min()
max_price = price_data['Average Price in USD'].max()
price_data['Accommodation Price Score'] = price_data['Average Price in USD'].apply(lambda x: 20 - 18 * (x-min_price)/(max_price-min_price))
price_data.to_csv('data/accomodation.csv', index=False)