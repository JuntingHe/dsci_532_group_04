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
    "width": "20%",
    "padding": "2% 1%",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "1%",
    "margin-right": "1%",
    "padding": "3% 2%",
    "width": "120%",
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
                    dbc.Label("Year Range"),
                    dcc.RangeSlider(
                        id="widget_g_year",
                        min=2000,
                        max=2015,
                        step=1,
                        value=[2000, 2015],
                        marks={i: str(i) for i in range(2000, 2016, 15)},
                        tooltip={'always_visible':False, 'placement':'bottom',},
                        #vertical=True,
                        #getTooltipPopupContainer={() => document.querySelector(".ant-slider-step")},
                        
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
    dbc.Row([
        dbc.Col([
            html.H5(
                "Life Expectancy Snapshot",
                style={
                    'background-color':'#E8E8E8', 
                    'font-weight':'900', 
                    'display': "flex", 
                    'justify-content': "center",
                    'align-items': "center", 
                    'width': "100%", 
                    'height': 50, 
                    'text-align':"center",
                },
            ),
            html.Iframe(
                id='map_graph',
                style={"height":"525px", "width":"100%", "display":'flex', 'scrolling':'no', 
                        'overflow':'hidden',"seamless":"seamless", 'border-width': '0',
                        "padding-right": "0px", "padding-left": "0%"
                }
            )]
        ),
        dbc.Col([
            html.H5(
                'Year-wise Trend', 
                style={
                    'background-color':'#E8E8E8', 
                    'font-weight':'900', 
                    'display': "flex", 
                    'justify-content': "center",
                    'align-items': "center", 
                    'width': "100%", 
                    'height': 50, 
                    'text-align':"center",
                },
                className="cursive",
            ),
            dbc.Row([
                dbc.Col(
                    html.P('Select Continents:', className="cursive"),
                    style={
                        'verticalAlign':"bottom",
                        'font-weight': 'bold',
                        'font-size': '14px',
                    },
                    md=2
                ),
                dbc.Col( 
                    dcc.Dropdown(
                        id='widget_l_continent',
                        options=[{'label': c, 'value': c} for c in dataset_df.continent.unique()],
                        clearable=True,
                        searchable=True,
                        style={
                            'verticalAlign':"middle",
                            'shape':'circle',
                            'border-radius':'36px',
                            'background-color':'#E8E8E8',
                            'display':'inline-block',
                            'width':"100%",
                        },
                        multi=True
                    ),
                ),], 
                no_gutters=True, 
            ),
            dbc.Row([
                dbc.Col(
                    html.P('Select Color Axis:', className="cursive",),
                    style={'verticalAlign':"bottom",
                            'font-weight': 'bold',
                            'font-size': '14px'
                    },
                    md=3
                ),
                dbc.Col(
                    dcc.RadioItems(
                        id='widget_l_color_axis',
                        options=[
                                {'label': "Continent", 'value': "continent"},
                                {'label': "Status", 'value': "status"},
                        ],
                        value='continent',
                        labelStyle={'margin-left':"2em"}
                    )
                )
                ], 
                no_gutters=True, 
            ),
            dbc.Row(
                html.Iframe(
                    id="widget_o_year_wise_trend",
                    style={
                        'border-width': '0', 
                        'width': '100%', 
                        "height":"430px"
                    }
                )
            )
            ]
        ),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H5(
                'Influence of Other Factors', 
                style={
                    'background-color':'#E8E8E8', 
                    'font-weight':'900', 
                    'width':"100%", 
                    'display': "flex", 
                    'justify-content': "center",
                    'align-items': "center", 
                    'height': 50, 
                    'text-align':"center",
                },
                className="cursive"
            ),
            dbc.Row([
                dbc.Col(
                        html.P('Select X-Axis:',
                                className="cursive",
                                ),
                        style={'verticalAlign':"bottom",
                                'font-weight': 'bold',
                                'font-size': '14px',
                                },                
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='widget_l_multi_dim_x_axis',
                        options=[
                            {'label': "Adult Mortality", 'value': "adult_mortality"},
                            {'label': "Infant Deaths", 'value': "infant_deaths"},
                            {'label': "Alcohol Consumption", 'value': "alcohol"},
                            {'label': "Expenditure (%)", 'value': "percentage_expenditure"},
                            {'label': "Hepatitis B", 'value': "hepatitis_B"},
                            {'label': "Measles", 'value': "measles"},
                            {'label': "BMI", 'value': "BMI"},
                            {'label': "Deaths (below 5 yrs)", 'value': "under_five_deaths"},
                            {'label': "Polio", 'value': "polio"},
                            {'label': "Total Expenditure", 'value': "total_expenditure"},
                            {'label': "Diphtheria", 'value': "diphtheria"},
                            {'label': "HIV/Aids", 'value': "hiv_aids"},
                            {'label': "GDP", 'value': "gdp"},
                            {'label': "Population", 'value': "population"},
                            {'label': "Schooling", 'value': "schooling"},

                        ],
                        value='adult_mortality',
                        clearable=False,
                        style={
                            'verticalAlign':"middle",
                            'shape':'circle',
                            'border-radius':'36px',
                            'background-color':'#E8E8E8',
                            'display':'inline-block',
                            'width':150,
                        },
                    ),
                    style={"margin-left":"0.5em"},
                ),
                dbc.Col(
                        html.P('Select Color Axis:',
                                className="cursive",
                                ),
                        style={'verticalAlign':"bottom",
                                'font-weight': 'bold',
                                'font-size': '14px',
                                'margin-left':'0.5em',
                                },
                ),
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
                            'background-color':'#E8E8E8',
                            'display':'inline-block',
                            'width':150,
                        },
                    ),
                    style={"margin-left":"0.5em"},
                )
            ], no_gutters=True,),
            dbc.Row([
                html.Iframe(
                            id="widget_o_multi_dim_analysis",
                            style={'border-width': '0', 'width': '100%', "height":"425px"}
                )
            ])

        ], ),
        dbc.Col([
            html.H5('Country vs Continent vs Worldwide', 
                    style={'background-color':'#E8E8E8', 'font-weight':'900', 'width':"100%", 'display': "flex", 'justify-content': "center",
                            'align-items': "center", 'height': 50, 'text-align':"center",},
                    className="cursive",),
                    dbc.Row([
                        dbc.Col(
                                html.P('Select a Country:',
                                        className="cursive",
                                ),
                                style={'verticalAlign':"bottom",
                                       'font-weight': 'bold',
                                        'font-size': '14px',
                                }, md=3,
                                ),
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
                                                'background-color':'#E8E8E8',
                                                'display':'inline-block',
                                                'width':"100%",
                                                }),
                                style={'margin-left':"1em"},                
                                ),
                            ], no_gutters=True,
                            ),
                            dbc.Row(html.Iframe(
                                id='comparison_trend',
                                style={
                                    'border-width': '0', 
                                    'width': '100%', 
                                    'height': '450px',
                                    "padding": "1% 0%",
                                }),)
        ], md=6, ),
    ])
    ], style=CONTENT_STYLE,
)

app.layout = dbc.Container([sidebar, content])

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
        x=alt.X("year:N", axis=alt.Axis(labelAngle=45), title = "Year"),
        y=alt.Y("mean(life_expectancy)", title = "Life Expectancy", scale= alt.Scale(zero = False)),
        color=alt.Color("label", title = None, legend=alt.Legend(orient="bottom"))
    ).properties(
            width=450,
            height=325
    ).configure_axis(
        labelFontSize=10,
        titleFontSize=12,
    ).configure_legend(
        labelFontSize=10
    )
    return chart_comparison.to_html()

# Year-wise trend graph
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
            color=alt.Color(color_axis, title = None, )
        ).configure_axis(
            labelFontSize=10,
            titleFontSize=12,
        ).configure_legend(
            labelFontSize=10,
            orient="bottom"
        ).project(scale=100).properties(
            width=450
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
    labels = {
        "adult_mortality": "Adult Mortality",
        "infant_deaths": "Infant Deaths",
        "alcohol": "Alcohol Consumption",
        "percentage_expenditure": "Expenditure (%)",
        "hepatitis_B": "Hepatitis B",
        "measles": "Measles",
        "BMI": "BMI",
        "under_five_deaths": "Deaths (below 5 yrs)",
        "polio": "Polio",
        "total_expenditure": "Total Expenditure",
        "diphtheria": "Diphtheria",
        "hiv_aids": "HIV/Aids",
        "gdp": "GDP",
        "population": "Population",
        "schooling": "Schooling"
    }

    chosen_ending_year = year_range[1]
    plot_multi_dim = alt.Chart(
        dataset_df[dataset_df["year"] == chosen_ending_year]
    ).mark_circle(size=100).encode(
        x=alt.X(x_axis, title=labels[x_axis]),
        y=alt.Y("life_expectancy", title="Life Expectancy", scale=alt.Scale(zero=False)),
        color=alt.Color(color_axis, title = None, legend=alt.Legend(orient="bottom")),
        #size=alt.Value("5"),
        tooltip=["country"],
    ).properties(
        width=450,
        height=310
    ).configure_axis(
        labelFontSize=10,
        titleFontSize=12,
    ).configure_legend(
        labelFontSize=10
    )
    return plot_multi_dim.to_html()

@app.callback(
    Output('map_graph', 'srcDoc'),
    Input('widget_g_year', 'value'),
)
def plot_worldmap(year_range):
    df1 = dataset_df.copy()
    world = data.world_110m()
    world_map = alt.topo_feature(data.world_110m.url, "countries")
    chosen_ending_year = year_range[1]

    country_ids = pd.read_csv(
        "https://raw.github.ubc.ca/MDS-2020-21/DSCI_532_viz-2_students/master/data/country-ids.csv?token=AAAANV4AYXPDYXASWHWFLDLACHCJK"
    )
    df1 = pd.merge(df1, country_ids, left_on="country", right_on="name").iloc[:, :-1]
    df1 = df1[df1["year"] == chosen_ending_year]

    map_click = alt.selection_multi()
    chart = (
        alt.Chart(world_map)
        .mark_geoshape(xOffset=2)
        .transform_lookup(
            lookup="id", from_=alt.LookupData(df1, "id", ["life_expectancy", "country"])
        )
        .encode(
            tooltip=[alt.Tooltip("country:N", title="Country"), alt.Tooltip("life_expectancy:Q", title="Life Exp")],
            color=alt.Color("life_expectancy:Q", legend = None),
            opacity=alt.condition(map_click, alt.value(1), alt.value(0.2)),
        )
        .add_selection(map_click)
        .project("equalEarth", scale=100).properties(
            width = 475,
            height = 475,
        ).configure_view(
            strokeWidth=0
        )
    )
    return chart.to_html()
    

if __name__ == '__main__':
    app.run_server(debug=True)
