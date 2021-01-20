import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import pandas as pd
import altair as alt
dataset_df = pd.read_csv("data/processed/life_expectancy_data_processed.csv")

app = dash.Dash(
    __name__, 
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
)

@app.callback(
    Output("widget-2", "children"),
    Input("widget_g_year", "value")
)
def update_output(input_value):
    return f"Selected year: {input_value}"


def plot_trend(year=2015):
    trend_chart = (
        alt.Chart(
            dataset_df[dataset_df["year"]<=year].groupby(["continent", "year"])
            .mean()["life_expectancy"]
            .reset_index()
        )
        .mark_line()
        .encode(
            x="year:N",
            y=alt.Y("mean(life_expectancy)", scale=alt.Scale(zero=False)),
            color="continent"
        )
    )
    return trend_chart.to_html()

@app.callback(
    Output("widget_trend_plot", "srcDoc"),
    Input("widget_g_year", "value")
)
def plot_trend_year_input(input_value):
    return plot_trend(input_value)



app.layout = html.Div([
    html.H1("Trend Plot"),
    html.Div(id="widget-2"),
    dcc.Slider(
        id="widget_g_year",
        min=2001, 
        max=2015, 
        value=2015,
        marks={2001: "2001", 2015: "2015"}
    ),
    
    html.Br(),
        html.Iframe(
        id="widget_trend_plot",
        srcDoc=plot_trend(),
        style={
            "border-width":"0",
            "width": "100%",
            "height": "400px"
        }
    ),
    html.P("Select a dimension:"),
    dcc.Dropdown(
        options=[
            {"label":"Continent", "value":"continent"},
            {"label":"Status", "value":"status"}
        ],
        value="continent", placeholder="Select Color Axis"
    ),
    html.Br(),
    html.P("Select a Continent:"),
    dcc.Dropdown(
        options=[
            {"label":"Continent", "value":"continent"},
            {"label":"Status", "value":"status"}
        ],
        value="continent", placeholder="Select Color Axis"
    )
    ]
)





if __name__=="__main__":
    app.run_server(debug=True)
