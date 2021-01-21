import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import pandas as pd
import dash_bootstrap_components as dbc

# Read in global data
dataset_df = pd.read_csv("data/processed/life_expectancy_data_processed.csv")

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

container_1 = dbc.Container(
    [
        dbc.Row(
            [
                html.H2(
                    'Country vs Continent vs Worldwide', 
                    style={'background-color':'#E8E8E8', 'verticalAlign':"middle",'font-weight':'900'},
                    className="cursive"
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.H5('Select a country:'),
                    md=2, 
                    style={'verticalAlign':"bottom",}
                ),
                dbc.Col( 
                    dcc.Dropdown(
                        id='country-l-widget',
                        value='Canada',  # REQUIRED to show the plot on the first page load
                        options=[{'label': country, 'value': country} for country in dataset_df.country.unique()],
                        clearable=False,
                        searchable=True,
                        style={
                            'verticalAlign':"middle",
                            'shape':'circle',
                            'border-radius':'36px',
                            'background-color':'#E8E8E8'
                        }
                    ),
                md=2
                )
            ],
            no_gutters=True,
        ),
        dbc.Row(
            html.Iframe(
                id='comparison_trend',
                style={'border-width': '0', 'width': '100%', 'height': '500px'}
            ),
        )
    ],
    style=CONTENT_STYLE
)

container_2 = dbc.Container(
    [
        dbc.Row(
            [
                html.H2(
                    'Year-wise Trend', 
                    style={'background-color':'#E8E8E8', 'verticalAlign':"middle",'font-weight':'900'},
                    className="cursive"
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.H5('Select Continents:'),
                    md=3, 
                    style={'verticalAlign':"bottom",}
                ),
                dbc.Col(
                    html.H5('Select Color Axis:'),
                    md=2, 
                    style={'verticalAlign':"bottom",}
                ),
            ],
            no_gutters=True,
        ),
        dbc.Row(
            [
                dbc.Col( 
                    dcc.Dropdown(
                        id='widget_l_continent',
                        #value='Canada',  # REQUIRED to show the plot on the first page load
                        options=[{'label': c, 'value': c} for c in dataset_df.continent.unique()],
                        clearable=True,
                        searchable=True,
                        style={
                            'verticalAlign':"middle",
                            'shape':'circle',
                            'border-radius':'36px',
                            'background-color':'#E8E8E8'
                        },
                        multi=True
                    ),
                md=2
                ),
                dbc.Col(md=1),
                dbc.Col(
                    dcc.RadioItems(
                        id='widget_l_color_axis',
                        options=[
                            {'label': "Continent", 'value': "continent"},
                            {'label': "Status", 'value': "status"},
                        ],
                        value='continent',
                        labelStyle={'display': 'inline-block'}
                    ),
                md=2
                )
            ],
            no_gutters=True,
        ),
        dbc.Row(
            [
                html.Iframe(
                    id="widget_o_year_wise_trend",
                    style={'border-width': '0', 'width': '100%', "height":"425px"}
                )
            ]
        )
    ],
    style=CONTENT_STYLE
)

container_3=dbc.Container(
    [
        dbc.Row(
            [
                html.H2(
                    'Effect', 
                    style={'background-color':'#E8E8E8', 'verticalAlign':"middle",'font-weight':'900'},
                    className="cursive"
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.H5('Select X-Axis:'),
                    md=3, 
                   
                ),
                dbc.Col(
                    html.H5('Select Color Axis:'),
                    md=2, 
                   
                ),
            ],
            no_gutters=True,
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='widget_l_multi_dim_x_axis',
                        options=[
                            {'label': "Adult Mortality", 'value': "adult_mortality"},
                            {'label': "Infant Deaths", 'value': "infant_deaths"},
                            {'label': "Alcohol Consumption", 'value': "alcohol"},
                            {'label': "percentage_expenditure", 'value': "percentage_expenditure"},
                            {'label': "hepatitis_B", 'value': "hepatitis_B"},
                            {'label': "measles", 'value': "measles"},
                            {'label': "BMI", 'value': "BMI"},
                            {'label': "under_five_deaths", 'value': "under_five_deaths"},
                            {'label': "polio", 'value': "polio"},
                            {'label': "total_expenditure", 'value': "total_expenditure"},
                            {'label': "diphtheria", 'value': "diphtheria"},
                            {'label': "hiv_aids", 'value': "hiv_aids"},
                            {'label': "gdp", 'value': "gdp"},
                            {'label': "population", 'value': "population"},
                            {'label': "schooling", 'value': "schooling"},

                        ],
                        value='adult_mortality',
                        clearable=False,
                        style={
                            'verticalAlign':"middle",
                            'shape':'circle',
                            'border-radius':'36px',
                            'background-color':'#E8E8E8'
                        },
                    ),
                md=2
                ),
                dbc.Col(md=1),
                dbc.Col(
                    dcc.Dropdown(
                        id='widget_l_multi_dim_color_axis',
                        options=[
                            {'label': "Continent", 'value': "continent"},
                            {'label': "Status", 'value': "status"},
                        ],
                        value='continent',
                        clearable=False,
                        style={
                            'verticalAlign':"middle",
                            'shape':'circle',
                            'border-radius':'36px',
                            'background-color':'#E8E8E8'
                        },
                    ),
                md=2
                )
            ],
            no_gutters=True,
        ),
        dbc.Row(
            [
                html.Iframe(
                    id="widget_o_multi_dim_analysis",
                    style={'border-width': '0', 'width': '100%', "height":"425px"}
                )
            ]
        )

    ]
)

main_container = dbc.Container(
    [
        dbc.Col(container_3),
        dbc.Col(container_2),
        dbc.Col(container_1)
    ]
)

app.layout = html.Div([sidebar, main_container])

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
        x=alt.X("year:N", title = "Year", axis=alt.Axis(labelAngle=45)),
        y=alt.Y("mean(life_expectancy)", title = "Life Expectancy", scale= alt.Scale(zero = False)),
        color=alt.Color("label", title = None)
    ).configure_axis(
        labelFontSize=16,
        titleFontSize=20,
    ).configure_legend(
        labelFontSize=16
    ).properties(width=500)
    return chart_comparison.to_html()

# Set up callbacks/backend
@app.callback(
    Output('widget_o_year_wise_trend', 'srcDoc'),
    Input('widget_g_year', 'value'),
    Input('widget_l_continent', 'value'),
    Input("widget_l_color_axis", "value")
)
def plot_year_wise_trend(year_range, continent, color_axis):
    chosen_starting_year = year_range[0]
    chosen_ending_year = year_range[1]
    temp_df = dataset_df[(dataset_df["year"] <= chosen_ending_year) & (dataset_df["year"] >= chosen_starting_year)]

    if continent is None or continent=="" or len(continent)==0:
        continent = dataset_df.continent.unique().tolist()
    
    temp_df = temp_df[temp_df["continent"].isin(continent)]
    year_wise_trend_chart = (
        alt.Chart(
            temp_df.groupby([color_axis, "year"])
            .mean()["life_expectancy"]
            .reset_index()
        )
        .mark_line()
        .encode(
            alt.X("year:N", axis=alt.Axis(labelAngle=45), title="Year"),
            y=alt.Y("mean(life_expectancy)", scale=alt.Scale(zero=False), title="Mean Life Expectancy"),
            color=color_axis
        ).properties(
            width=500
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=20,
        ).configure_legend(
            labelFontSize=16
        )
    )
    return year_wise_trend_chart.to_html()

@app.callback(
    Output('widget_o_multi_dim_analysis', 'srcDoc'),
    Input('widget_g_year', 'value'),
    Input('widget_l_multi_dim_x_axis', 'value'),
    Input('widget_l_multi_dim_color_axis', 'value')
)
def plot_multi_dim_analysis(year_range, x_axis, color_axis):
    chosen_ending_year = year_range[1]
    plot_multi_dim = alt.Chart(
        dataset_df[dataset_df["year"] == chosen_ending_year]
    ).mark_circle(size=100).encode(
        x=alt.X(x_axis),
        y=alt.Y("life_expectancy", title="Life Expectancy", scale=alt.Scale(zero=False)),
        color=color_axis,
        #size=alt.Value("5"),
        tooltip=["country"],
    )
    return plot_multi_dim.to_html()
    

if __name__ == '__main__':
    app.run_server(debug=True)
