import pandas as pd
import plotly.express as px
from flask import Flask, render_template, request

app = Flask(__name__)

#URL controller routes
@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/result', methods=['GET'])
def result():
    origin_country = request.args['country'].capitalize()

    #Data Analysis of visa requirement dataset
    df = pd.read_csv("data/passport-index-tidy.csv")
    selected_countries_from_origin = df[df["Passport"] == origin_country]
    #Converts all numeric parameter(number of days of free stay) into one(visa free)
    selected_countries_from_origin.loc[
        (str(df['Requirement']).isnumeric()) & (df['Requirement'] != "-1"), 'Requirement'] = 'visa free'
    selected_countries_from_origin['Requirement'] = selected_countries_from_origin['Requirement'].apply(
        lambda x: 'visa free' if str(x).isnumeric() and x != "-1" else x)
    #Locates Origin country from dataframe and change value of requirement
    selected_countries_from_origin.loc[(df['Requirement'] == "-1"), 'Requirement'] = 'Your country'

    #Generate World map graph with this function
    world_map = get_visa_map(selected_countries_from_origin)

    #Get count for each visa requirement type and determine score
    visa_summary = selected_countries_from_origin.groupby(['Requirement'])['Requirement'].count()

    visa_score_dict = {
        'visa free': 30,
        'e-visa': 25,
        'visa on arrival': 20,
        'visa required': 10,
        'Your country': 0
    }

    visa_scores = selected_countries_from_origin[['Destination','Requirement']]
    visa_scores['Visa Score'] = visa_scores['Requirement'].apply(lambda destination: visa_score_dict[destination])

    #Data Analysis of flight prices
    df_airfare_prices = pd.read_csv('data/airline_prices.csv')
    selected_airfare = df_airfare_prices[(df_airfare_prices['Origin Country'] == origin_country)]
    selected_airfare_grouped = selected_airfare.groupby(['Origin Country', 'Destination Country'], as_index=False).agg(
        {'Price(USD)': ['mean']})
    selected_airfare_grouped.columns = list(map(''.join, selected_airfare_grouped.columns.values))

    #Applies scoring to flight price: weight x (x-min) / (max-min)
    max_flight = selected_airfare_grouped['Price(USD)mean'].max()
    min_flight = selected_airfare_grouped['Price(USD)mean'].min()
    selected_airfare_grouped['Flight Price Score'] = selected_airfare_grouped['Price(USD)mean'].apply(
        lambda x: 40 - 36 * (x - min_flight) / (max_flight - min_flight))

    #Generate Flight Price graph with this function call
    flight_prices_plot = get_flight_price_graph(selected_airfare_grouped)

    #Data Analysis of Accommodation Prices
    accommodation_price_df = pd.read_csv('data/accomodation.csv')
    accommodation_price_df = accommodation_price_df.rename(
        columns={'Average Price in USD': 'Avg Accommodation Price(USD)'})

    # Generate Accommodation Price graph with this function call
    accom_prices_plot = get_acc_price_graph(accommodation_price_df)

    #Selection of top 5 recommendations
    result_df = pd.merge(accommodation_price_df, selected_airfare_grouped, how='inner', left_on='Country',
                         right_on='Destination Country')
    result_df = pd.merge(result_df, visa_scores, how='left', left_on='Country', right_on='Destination')
    result_df['Total Score'] = result_df['Flight Price Score'] + result_df['Accommodation Price Score'] + \
                               result_df['Visa Score']
    top_5 = result_df[
        ['Destination Country', 'Flight Price Score', 'Accommodation Price Score', 'Total Score']].sort_values(
        by='Total Score', ascending=False).head(5)

    #Sends summary data and graph to Flask HTML template
    return render_template("result.html", world_map=world_map['fig'], visa_summary=visa_summary.to_dict(),
                           flight_prices=flight_prices_plot['fig'],
                           accom_prices=accom_prices_plot['fig'], top_5=top_5.to_dict())


def get_visa_map(data):
    fig = px.choropleth(
        locations=data['Destination'],
        locationmode="country names",
        color=data['Requirement'],
        color_discrete_map=
        {'visa required': 'red',
         'e-visa': 'Yellow',
         'visa free': 'Green',
         'visa on arrival': 'Orange',
         'Your country': 'Blue',
         },
        height=600
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        showlegend=False,
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
    return {"fig": fig.to_html(full_html=False)}


def get_flight_price_graph(data):
    fig_2 = px.bar(data, x='Destination Country', y='Price(USD)mean', height=600,
                   color_continuous_scale="RdYlGn", color='Flight Price Score')
    fig_2.update_xaxes(categoryorder='total ascending')
    fig_2.update_coloraxes(showscale=False)
    fig_2.update_layout(yaxis_title='Average Airfare(USD)')
    return {"fig": fig_2.to_html(full_html=False)}


def get_acc_price_graph(data):
    fig_3 = px.bar(data, x='Country', y='Avg Accommodation Price(USD)', height=600,
                   color_continuous_scale="RdYlGn", color='Accommodation Price Score')
    fig_3.update_xaxes(categoryorder='total ascending')
    fig_3.update_coloraxes(showscale=False)
    fig_3.update_layout(yaxis_title='Average Airbnb Price(USD)')
    return {"fig": fig_3.to_html(full_html=False)}


if __name__ == '__main__':
    app.run()
