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
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "40rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Life", className="display-6"),
        html.H2("Expectancy", className="display-6"),
        html.H2("Indicator", className="display-6"),
        html.Hr(),
        # html.P(
        #     "A simple sidebar layout with navigation links", className="lead"
        # ),
        dbc.Nav(
            [
                 dbc.FormGroup(
                [
                    dbc.Label("Choose for Year"),
                    dcc.RangeSlider(
                        id="widget_g_year",
                        min=2000,
                        max=2015,
                        step=1,
                        value=[2000, 2015],
                        #marks={i: str(i) for i in range(2000, 2016, 5)},
                        tooltip={'always_visible':True, 'placement':'bottom'},
                        
                    ),
                ]
            ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = dbc.Container([
    html.H2('Country vs Continent vs Worldwide', 
            style={'background-color':'#E8E8E8', 'verticalAlign':"middle",'font-weight':'900'},
            className="cursive",
            
                                            ),
    dbc.Row(
        [
        dbc.Col(html.H5('Select a country:'),
                md=2, 
                style={'verticalAlign':"bottom",}),
        dbc.Col( 
            dcc.Dropdown(
                id='country-l-widget',
                value='Canada',  # REQUIRED to show the plot on the first page load
                options=[{'label': country, 'value': country} for country in dataset_df.country.unique()],
                clearable=False,
                searchable=True,
                style={'verticalAlign':"middle",
                       'shape':'circle',
                       'border-radius':'36px',
                       'background-color':'#E8E8E8'}),
            md=2)
        ],
        no_gutters=True,
        ),
    dbc.Row(
        html.Iframe(
        id='comparison_trend',
        style={'border-width': '0', 'width': '100vw', 'height': '100vh'}),)
    ], style=CONTENT_STYLE)

app.layout = html.Div([sidebar, content])

# Set up callbacks/backend
@app.callback(
    Output('comparison_trend', 'srcDoc'),
    Input('country-l-widget', 'value'),
    Input('widget_g_year', 'value'))
def plot_altair(country, value):
    chosen_country = country
    chosen_starting_year = value[0]
    chosen_ending_year = value[1]
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
    chart_comparison = alt.Chart(temp[(temp["year"] <= chosen_ending_year) & (temp["year"] >= chosen_starting_year)]).mark_line().encode(
        x=alt.X("year:N", title = "Year"),
        y=alt.Y("mean(life_expectancy)", title = "Life Expectancy", scale= alt.Scale(zero = False)),
        color=alt.Color("label", title = None)
    ).configure_axis(
        labelFontSize=16,
        titleFontSize=20,
    ).configure_legend(
        labelFontSize=16)
    return chart_comparison.to_html()


    

if __name__ == '__main__':
    app.run_server(debug=True)
