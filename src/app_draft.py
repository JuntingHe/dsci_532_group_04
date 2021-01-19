import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import pandas as pd
import dash_bootstrap_components as dbc


# Read in global data
dataset_df = pd.read_csv("../data/processed/life_expectancy_data_processed.csv")

# Setup app and layout/frontend
app = dash.Dash(__name__,  
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div(['Country vs Continent vs Worldwide',
    dcc.Dropdown(
        id='country-l-widget',
        value='Canada',  # REQUIRED to show the plot on the first page load
        options=[{'label': country, 'value': country} for country in dataset_df.country.unique()]),
    html.Iframe(
        id='comparison_trend',
        style={'border-width': '0', 'width': '100vw', 'height': '100vh'})
    ])

# Set up callbacks/backend
@app.callback(
    Output('comparison_trend', 'srcDoc'),
    Input('country-l-widget', 'value'))
def plot_altair(country):
    chosen_country = country
    sel_continent = dataset_df[dataset_df["country"] == chosen_country].head(1).continent.tolist()[0]
    temp = (
        dataset_df.groupby("year")
        .mean()["life_expectancy"]
        .reset_index()
        .assign(label="Worldwide"))
    temp = pd.concat([
        temp,
        dataset_df[dataset_df["continent"] == sel_continent]
        .groupby("year")
        .mean()["life_expectancy"]
        .reset_index()
        .assign(label=sel_continent)],
        ignore_index=True,)
    temp = pd.concat([
        temp,
        dataset_df.loc[
            dataset_df["country"] == chosen_country, ["year", "life_expectancy"]
        ].assign(label=chosen_country),],
        ignore_index=True,)
    chart_comparison = alt.Chart(temp).mark_line().encode(
        x=alt.X("year", title = "Year"),
        y=alt.Y("life_expectancy", title = "Life Expectancy", scale= alt.Scale(zero = False)),
        color=alt.Color("label", title = None)
    ).configure_axis(
        labelFontSize=16,
        titleFontSize=20,
    ).configure_legend(
        labelFontSize=16)
    return chart_comparison.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)

