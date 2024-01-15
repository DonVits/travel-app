import os

import plotly.express as px
import pandas as pd
from flask import Flask, render_template, request, redirect, session
from jinja2 import Environment, Template, PackageLoader, select_autoescape
import numpy as np

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/result', methods=['GET'])
def result():
    SELECT_DESTINATIONS = ['Netherlands', 'Greece', 'Thailand', 'Germany', 'Belgium', 'Argentina',
                           'South Africa',
                           'Denmark', 'Ireland', 'Hong Kong(SAR)', 'Turkey', 'Portugal', 'United Kingdom', 'Spain',
                           'Malta', 'Mexico', 'United States',
                           'Norway', 'France', 'Czech Republic', 'Latvia', 'Brazil', 'Italy', 'Singapore', 'Sweden',
                           'Australia', 'Taiwan', 'Japan', 'Canada', 'Austria', 'Switzerland'
                           ]
    cities = os.listdir('data/airbnb/')
    PRICE_CONVERSION = {'Netherlands': 1.09, 'Greece': 1.09, 'Thailand': 0.029,
                       'Germany': 1.09, 'Belgium': 1.09, 'Argentina': 0.0012,
                       'South Africa': 0.054, 'Denmark': 0.15, 'Ireland': 1.09,
                       'Hong Kong(SAR)': 0.13, 'Turkey': 0.033, 'Portugal': 1.09,
                       'United Kingdom': 1.27, 'Spain': 1.09, 'Malta': 1.09, 'Mexico': 0.059,
                       'United States': 1, 'Norway': 0.097, 'France': 1.09, 'Czech Republic': 0.044,
                       'Latvia': 1.09, 'Brazil': 0.21, 'Italy': 1.09, 'Singapore': 0.75,
                       'Sweden': 0.097, 'Australia': 0.67, 'Taiwan': 0.032, 'Japan': 0.0069,
                       'Canada': 0.74, 'Austria': 1.09, 'Switzerland': 1.17}

    SELECTED_CITIES = {'Netherlands': 'Amsterdam', 'Greece': 'Athens', 'Thailand': 'Bangkok',
                       'Germany': 'Berlin', 'Belgium': 'Brussels', 'Argentina': 'Buenos Aires',
                       'South Africa': 'Cape Town', 'Denmark': 'Copenhagen', 'Ireland': 'Dublin',
                       'Hong Kong(SAR)': 'Hong Kong(SAR)', 'Turkey': 'Istanbul', 'Portugal': 'Lisbon',
                       'United Kingdom': 'London', 'Spain': 'Madrid', 'Malta': 'Malta', 'Mexico': 'Mexico City',
                       'United States': 'New York', 'Norway': 'Oslo', 'France': 'Paris', 'Czech Republic': 'Prague',
                       'Latvia': 'Riga', 'Brazil': 'Rio De Janeiro', 'Italy': 'Rome', 'Singapore': 'Singapore',
                       'Sweden': 'Stockholm', 'Australia': 'Sydney', 'Taiwan': 'Taipei', 'Japan': 'Tokyo',
                       'Canada': 'Vancouver', 'Austria': 'Vienna', 'Switzerland': 'Zurich'}

    origin_country = request.args['country'].capitalize()
    df = pd.read_csv("data/passport-index-tidy.csv")
    selected_countries_from_origin = df[df["Passport"] == origin_country]
    selected_countries_from_origin.loc[
        (str(df['Requirement']).isnumeric()) & (df['Requirement'] != "-1"), 'Requirement'] = 'visa free'
    selected_countries_from_origin['Requirement'] = selected_countries_from_origin['Requirement'].apply(
        lambda x: 'visa free' if str(x).isnumeric() and x != "-1" else x)
    selected_countries_from_origin.loc[(df['Requirement'] == "-1"), 'Requirement'] = 'Your country'
    fig = px.choropleth(
        locations=selected_countries_from_origin['Destination'],
        locationmode="country names",
        color=selected_countries_from_origin['Requirement'],
        color_discrete_map=
        {'visa required': 'red',
         'e-visa': 'Yellow',
         'visa free': 'Green',
         'visa on arrival': 'Orange',
         'Your country': 'Blue',
         },
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        title_text='Passport Index Data',
        legend_title_text="Visa requirement",
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        annotations=[dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://github.com/ilyankou/passport-index-dataset">\
              Passport Index Dataset</a>',
            showarrow=False
        )])
    world_map = {"fig": fig.to_html(full_html=False)}

    df_airfare_prices = pd.read_csv('data/airline_prices.csv')
    selected_airfare = df_airfare_prices[(df_airfare_prices['Origin Country'] == origin_country) & (
        df_airfare_prices['Destination Country'].isin(SELECT_DESTINATIONS))]
    selected_airfare_grouped = selected_airfare.groupby(['Origin Country', 'Destination Country'], as_index=False).agg(
        {'Price(USD)': ['mean']})
    selected_airfare_grouped.columns = list(map(''.join, selected_airfare_grouped.columns.values))

    fig_2 = px.histogram(selected_airfare_grouped, x='Destination Country', y='Price(USD)mean', height=800)
    fig_2.update_xaxes(categoryorder='total ascending')
    fig_2.update_layout(yaxis_title='Average Airfare')

    flight_prices_plot = {"fig": fig_2.to_html(full_html=False)}

    def get_avg_accom(country):
        print(SELECTED_CITIES[country])
        city_df = pd.read_csv('data/airbnb/' + SELECTED_CITIES[country] + '.csv')
        city_sample = city_df.sample(n=40)
        city_sample.dropna()
        average_price = city_sample['price'].mean()
        return average_price * PRICE_CONVERSION[country]



    selected_airfare_grouped['Average Price'] = selected_airfare_grouped['Destination Country'].apply(get_avg_accom)
    fig_3 = px.histogram(selected_airfare_grouped, x='Destination Country', y='Average Price', height=800)
    fig_3.update_xaxes(categoryorder='total ascending')
    fig_3.update_layout(yaxis_title='Average Airbnb Price')

    accom_prices_plot = {"fig": fig_3.to_html(full_html=False)}

    return render_template("result.html", world_map=world_map['fig'], flight_prices=flight_prices_plot['fig'],
                           accom_prices=accom_prices_plot['fig'])


if __name__ == '__main__':
    app.run()
