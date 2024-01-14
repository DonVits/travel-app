import plotly.express as px
import pandas as pd
from flask import Flask, render_template, request, redirect, session
from jinja2 import Environment, Template, PackageLoader, select_autoescape

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/result', methods=['GET'])
def result():
    SELECT_DESTINATIONS = ['Poland','France','Germany','United States','United Kingdom','Australia','Japan','Spain','Singapore']
    origin_country = request.args['country'].capitalize()
    df = pd.read_csv("data/passport-index-tidy.csv")
    selected_countries_from_origin = df[df["Passport"] == origin_country]
    selected_countries_from_origin.loc[(str(df['Requirement']).isnumeric()) & (df['Requirement'] != "-1"), 'Requirement'] = 'visa free'
    selected_countries_from_origin['Requirement'] = selected_countries_from_origin['Requirement'].apply(
        lambda x: 'visa free' if str(x).isnumeric() and x != "-1" else x)
    selected_countries_from_origin.loc[(df['Requirement'] == "-1"), 'Requirement'] = 'Your country'

    print(selected_countries_from_origin)
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
        margin={"r":0,"t":0,"l":0,"b":0},
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
    world_map = {"fig":fig.to_html(full_html=False)}

    df_airfare_prices = pd.read_csv('data/airline_prices.csv')
    selected_airfare = df_airfare_prices[(df_airfare_prices['Origin Country'] == origin_country) & (df_airfare_prices['Destination Country'].isin(SELECT_DESTINATIONS))]
    print(selected_airfare[['Origin Country','Destination Country','Price(USD)']])
    selected_airfare_grouped = selected_airfare.groupby(['Origin Country','Destination Country'], as_index=False).agg({'Price(USD)': ['mean']})
    selected_airfare_grouped.columns = list(map(''.join, selected_airfare_grouped.columns.values))

    fig_2 = px.histogram(selected_airfare_grouped, x='Destination Country', y='Price(USD)mean', height=800)
    flight_prices_plot = {"fig":fig_2.to_html(full_html=False)}
    return render_template("result.html", world_map = world_map['fig'], flight_prices = flight_prices_plot['fig'])


if __name__ == '__main__':
    app.run()
