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

card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H2("Life", className="display-6"),
                html.H2("Expectancy", className="display-6"),
                html.H2("Indicator", className="display-6"),
                html.Hr(),
                dbc.Label("Year Range"),
                dcc.RangeSlider(
                        id="widget_g_year",
                        min=2000,
                        max=2015,
                        step=1,
                        value=[2000, 2015],
                        marks={i: str(i) for i in range(2000, 2016, 15)},
                        tooltip={'always_visible':False, 'placement':'bottom',},   
                    ),
            ]
        ),
        # dbc.CardFooter("This is the footer"),
    ],
    style={"width": "18rem", 'background-color':'#f8f9fa',},
)


world_map = dbc.Card([
    dbc.CardHeader("Life Expectancy Snapshot", className="cursive", style={'font-weight':'900'}),
    dbc.CardBody([html.Iframe(id='map_graph', width = 800, height = 500, sandbox='allow-scripts', style={'border-width': '0px'})])
]) 

widget_style = {'verticalAlign':"bottom",'font-weight': 'bold','font-size': '14px',}
dropdown_style = {'verticalAlign':"middle", 'shape':'circle', 'border-radius':'36px',
'background-color':'#E8E8E8', 'display':'inline-block', 'width':"100%",}

continent_widget = html.P('Select Continents:', className="card-text", style=widget_style)
continent_dropdown = dcc.Dropdown(id='widget_l_continent',
    #value='Canada',  # REQUIRED to show the plot on the first page load
    options=[{'label': c, 'value': c} for c in dataset_df.continent.unique()],
    clearable=True,
    searchable=True,
    style= dropdown_style,
    multi=True
    ),

status_widget = html.P('Select Color Axis:', className="card-text", style=widget_style)
status_dropdown = dcc.RadioItems(id='widget_l_color_axis',
    options=[{'label': "Continent", 'value': "continent"},{'label': "Status", 'value': "status"},],
    value='continent',
    labelStyle={'margin-left':"1em",}
    )


trend_card = dbc.Card([
    dbc.CardHeader("Year-wise Trend", className="cursive",style={'font-weight':'900'}),
    dbc.CardBody([
            dbc.Row([dbc.Col(continent_widget), dbc.Col(continent_dropdown)]),
            html.Br(),
            dbc.Row([dbc.Col(status_widget), dbc.Col(status_dropdown)]),
            html.Iframe(id="widget_o_year_wise_trend", width = 500, height = 500, style={'border-width': '0',})
        ]),
    ],style={"width":550, "height":580},)

country_widget = html.P('Select a Country:', className="card-text", style=widget_style)
country_dropdown = dcc.Dropdown(id='country-l-widget',
    value='Canada',  # REQUIRED to show the plot on the first page load
    options=[{'label': country, 'value': country} for country in dataset_df.country.unique()],
    clearable=False,
    searchable=True,
    style=dropdown_style),

comparison_card = dbc.Card([
    dbc.CardHeader("Country vs Continent vs Worldwide", className="cursive",style={'font-weight':'900'}),
    dbc.CardBody([
            dbc.Row([dbc.Col(country_widget), dbc.Col(country_dropdown)]),
            html.Br(),
            html.Br(),
            html.Iframe(id="comparison_trend", width = 500, height = 500, style={'border-width': '0',})
        ]),
    ],style={"width":550, "height":580},)

axis_widget = html.P('Select X-Axis:', className="card-text", style=widget_style)
axis_dropdown = dcc.Dropdown(id='widget_l_multi_dim_x_axis',
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
        {'label': "schooling", 'value': "schooling"},],
        value='adult_mortality',
        clearable=False,
        style=dropdown_style,)

color_widget = html.P('Select Color Axis:', className="card-text", style=widget_style)
color_dropdown = dcc.Dropdown(id='widget_l_multi_dim_color_axis',
    options=[{'label': "Continent", 'value': "continent"}, {'label': "Status", 'value': "status"},],
    value='continent',
    clearable=False,
    style=dropdown_style,
    )

effect_card = dbc.Card([
    dbc.CardHeader("Influence of Other Factors", className="cursive",style={'font-weight':'900'}),
    dbc.CardBody([
            dbc.Row([dbc.Col(axis_widget), dbc.Col(axis_dropdown), dbc.Col(color_widget), dbc.Col(color_dropdown),]),
            html.Br(),
            html.Iframe(id="widget_o_multi_dim_analysis", width = 1000, height = 500, style={'border-width': '0',})
        ]),
    ],)


app.layout = dbc.Container([
    dbc.Row([card, world_map]),
    html.Br(),
    dbc.CardDeck([trend_card, comparison_card]),
    html.Br(),
    dbc.CardDeck(effect_card)])


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
        "data/processed/country-ids.csv"
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
            tooltip=["country:N", "life_expectancy:Q"],
            color=alt.Color("life_expectancy:Q", title = "Life Expectancy"),
            opacity=alt.condition(map_click, alt.value(1), alt.value(0.2)),
        )
        .add_selection(map_click)
        .project("equalEarth", scale=140)
        .properties(width = 625, height = 445,)
        .configure_view(strokeWidth=0)
    )
    return chart.to_html()

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
            alt.X("year:N", axis=alt.Axis(labelAngle=360), title="Year"),
            y=alt.Y("mean(life_expectancy)", scale=alt.Scale(zero=False), title="Mean Life Expectancy"),
            color=alt.Color(color_axis, title = None, legend=alt.Legend(orient='bottom'))
        ).configure_axis(
            labelFontSize=10,
            titleFontSize=14,
        ).configure_legend(
            labelFontSize=12,
        ).properties(
            width=400
        )
    )
    return year_wise_trend_chart.to_html()

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
        x=alt.X("year:N", axis=alt.Axis(labelAngle=360), title = "Year"),
        y=alt.Y("mean(life_expectancy)", title = "Life Expectancy", scale= alt.Scale(zero = False)),
        color=alt.Color("label", title = None, legend=alt.Legend(orient="bottom"))
    ).properties(
            width=400
        ).configure_axis(
            labelFontSize=10,
            titleFontSize=14,
        ).configure_legend(
            labelFontSize=12
        )
    return chart_comparison.to_html()

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
    ).mark_circle(size=150).encode(
        x=alt.X(x_axis, title=labels[x_axis]),
        y=alt.Y("life_expectancy", title="Life Expectancy", scale=alt.Scale(zero=False)),
        color=alt.Color(color_axis, title = None, legend=alt.Legend(orient="bottom")),
        #size=alt.Value("5"),
        tooltip=["country"],
    ).properties(
        width=900,
        height=400
    ).configure_axis(
        labelFontSize=10,
        titleFontSize=14,
    ).configure_legend(
        labelFontSize=12
    )
    return plot_multi_dim.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)
