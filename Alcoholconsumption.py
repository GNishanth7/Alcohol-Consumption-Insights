from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

#Load datasets
ireland_data = pd.read_csv('Cleaned_datasets/cleaned_alcohol_consumption_data.csv')
quarterly_data = pd.read_csv('Cleaned_datasets/cleaned_quarterly_alcohol.csv')
global_data = pd.read_csv("Cleaned_datasets/cleaned_alcohol_world.csv")
coordinates_data = pd.read_csv("Cleaned_datasets/world_country_and_usa_states_latitude_and_longitude_values.csv")

#Data preparation
global_data = global_data.rename(columns={"Country Name": "Country"})
coordinates_data = coordinates_data.rename(columns={"country": "Country", "latitude": "Latitude", "longitude": "Longitude"})
merged_global = pd.merge(global_data, coordinates_data, on="Country", how="left").dropna(subset=["Latitude", "Longitude"])

#Filter Ireland-specific data
ireland_global_data = merged_global[merged_global['Country'] == "Ireland"]

#Initialize Dash App with Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

#Navbar
navbar = dbc.NavbarSimple(
    brand="Alcohol Consumption Dashboard",
    brand_href="#",
    color="dark",
    dark=True,
    sticky="top",
)

navbar = dbc.Navbar(
    children=[
        dbc.Container(
            children=[
                html.A(
                    "Alcohol Consumption Dashboard",
                    href="#",
                    className="navbar-brand",
                    style={"width": "100%", "textAlign": "center", "display": "block"}
                )
            ],
            fluid=True
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)

#Footer
footer = dbc.Container(
    [
        html.Hr(style={"borderTop": "1px solid white"}),
        html.P(
            "© 2024 Alcohol Consumption Insights | Created by Nishanth Gopinath",
            style={"textAlign": "center", "color": "#b3b3b3", "fontSize": "14px"},
        ),
    ],
    fluid=True,
    style={"padding": "10px", "backgroundColor": "#2d2d2d"},
)

app.layout = dbc.Container(
    [
        navbar,

        #Global Comparison Section
        html.Div(style={"backgroundColor": "black"}, children=[
            dbc.Row([
                dbc.Col([
                    html.H2("Global Alcohol Consumption Comparison", className="text-center", style={"color": "white"}),
                    dcc.Dropdown(
                        id="global-year-dropdown",
                        options=[{"label": year, "value": year} for year in merged_global["Year"].unique()],
                        value=2019,
                        placeholder="Select a year",
                        style={"width": "60%", "margin": "auto", "textAlign": "center"},
                    ),
                    dcc.Graph(id="globe-map", style={"height": "500px", "backgroundColor": "black"}),
                    html.P(
                        "Click on a country on the globe to compare with Ireland.",
                        style={"color": "white", "textAlign": "center", "fontSize": "14px"},
                    ),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id="ireland-map", style={"height": "400px", "backgroundColor": "black"}), width=6),
                        dbc.Col(dcc.Graph(id="country-map", style={"height": "400px", "backgroundColor": "black"}), width=6),
                    ], style={"marginTop": "20px"}),
                    html.Div(
                        id="comparison-stats",
                        style={"color": "white", "marginTop": "30px", "textAlign": "center", "fontSize": "16px"},
                    ),
                ], width=12),
            ]),
        ]),

        #Trends Section
        dbc.Row([
            dbc.Col([
                html.Div(style={"backgroundColor": "black"}, children=[
                    html.H2("Alcohol Consumption Trends in Ireland", className="text-center", style={"color": "white"}),
                    html.Label("Select Age Group:", style={"color": "#ffffff", "fontSize": "16px"}),
                    dcc.Dropdown(
                        id='age-group-dropdown',
                        options=[{'label': age, 'value': age} for age in ireland_data['Age Group'].unique()],
                        value='All ages',
                        style={"backgroundColor": "#ffffff", "color": "#000000"},
                        placeholder="Select an age group"
                    ),
                    dcc.Graph(id='trend-graph', style={"height": "400px", "backgroundColor": "black"}),
                    html.P(
                        "Explore trends in alcohol consumption across different age groups in Ireland. * No data available for 2019 and 2020.",
                        className="text-center",
                        style={"color": "#b3b3b3", "fontSize": "12px"},
                    ),
                ])
            ], width=12),
        ], className="mb-4"),

        #Demographics Section
        dbc.Row([
            dbc.Col([
                html.Div(style={"backgroundColor": "black"}, children=[
                    html.H2("Alcohol Consumption by Gender and Age", className="text-center", style={"color": "white"}),
                    html.Label("Select Year:", style={"color": "#ffffff", "fontSize": "16px"}),
                    dcc.Dropdown(
                        id='year-dropdown',
                        options=[{'label': str(year), 'value': year} for year in ireland_data['Year'].unique()],
                        value=ireland_data['Year'].max(),
                        style={"backgroundColor": "#ffffff", "color": "#000000"}
                    ),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='gender-donut-chart', style={"height": "400px", "backgroundColor": "black"}), width=6),
                        dbc.Col(dcc.Graph(id='age-gender-bar-chart', style={"height": "400px", "backgroundColor": "black"}), width=6),
                    ]),
                ])
            ], width=12),
        ], className="mb-4"),

        #Quarterly Insights Section
        dbc.Row([
            dbc.Col([
                html.Div(style={"backgroundColor": "black"}, children=[
                    html.H2("Quarterly Alcohol Consumption in Ireland", className="text-center", style={"color": "white"}),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Select Alcohol Type:", style={"color": "white"}),
                            dcc.Dropdown(
                                id='alcohol-type-dropdown',
                                options=[
                                    {'label': 'All', 'value': 'All'},
                                    {'label': 'Beer', 'value': 'Beer'},
                                    {'label': 'Wine', 'value': 'Wine'},
                                    {'label': 'Spirits', 'value': 'Spirits'},
                                    {'label': 'Cider', 'value': 'Cider'}
                                ],
                                value='All',
                                style={"color": "black"}
                            ),
                        ], width=6),
                        dbc.Col([
                            html.Label("Select Year:", style={"color": "white"}),
                            dcc.Dropdown(
                                id='quarterly-year-dropdown',
                                options=[{'label': str(year), 'value': year} for year in quarterly_data['year'].unique()],
                                value=quarterly_data['year'].max(),
                                style={"color": "black"}
                            ),
                        ], width=6),
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='quarterly-line-chart', style={"height": "400px", "backgroundColor": "black"}), width=6),
                        dbc.Col(dcc.Graph(id='stacked-bar-chart', style={"height": "400px", "backgroundColor": "black"}), width=6),
                    ]),
                ])
            ], width=12),
        ], className="mb-4"),

        footer,
    ],
    fluid=True,
    style={"backgroundColor": "black"},
)

#Callbacks
@app.callback(
    Output('trend-graph', 'figure'),
    [Input('age-group-dropdown', 'value')]
)
def update_trend_graph(selected_age_group):
    filtered_data = ireland_data[ireland_data['Age Group'] == selected_age_group]
    grouped_data = filtered_data.groupby('Year')['Alcohol Consumption (%)'].mean().reset_index()

    #Add asterisk for missing years
    grouped_data['Year'] = grouped_data['Year'].astype(str)
    for year in [2019, 2020]:
        if year in grouped_data['Year'].values:
            grouped_data.loc[grouped_data['Year'] == str(year), 'Year'] = str(year) + "*"

    fig = px.line(
        grouped_data,
        x='Year',
        y='Alcohol Consumption (%)',
        title=f"Alcohol Consumption Trends: {selected_age_group}",
        template='plotly_dark'
    )
    fig.update_layout(paper_bgcolor="black", plot_bgcolor="black")
    return fig

@app.callback(
    [Output('gender-donut-chart', 'figure'),
     Output('age-gender-bar-chart', 'figure')],
    [Input('year-dropdown', 'value')]
)
def update_charts(selected_year):
    filtered_data = ireland_data[ireland_data['Year'] == selected_year]

    #Donut Chart for Gender Distribution
    gender_data = filtered_data.groupby('Sex')['Alcohol Consumption (%)'].sum().reset_index()
    donut_chart = px.pie(
        gender_data,
        names='Sex',
        values='Alcohol Consumption (%)',
        hole=0.5,
        title=f"Alcohol Consumption by Gender in {selected_year}"
    )
    donut_chart.update_layout(
        title_x=0.5,
        paper_bgcolor="#2d2d2d",
        font_color="#ffffff",
        legend_title=dict(font=dict(color="#ffffff"))
    )

    #Bar Chart for Age and Gender
    bar_chart = px.bar(
        filtered_data,
        x='Age Group',
        y='Alcohol Consumption (%)',
        color='Sex',
        barmode='group',
        title=f"Alcohol Consumption by Age and Gender in {selected_year}"
    )
    bar_chart.update_layout(
        title_x=0.5,
        paper_bgcolor="#2d2d2d",
        plot_bgcolor="#2d2d2d",
        font_color="#ffffff",
        xaxis_title="Age Group",
        yaxis_title="Alcohol Consumption (%)",
        legend_title=dict(font=dict(color="#ffffff"))
    )

    return donut_chart, bar_chart

@app.callback(
    [Output('quarterly-line-chart', 'figure'), Output('stacked-bar-chart', 'figure')],
    [Input('alcohol-type-dropdown', 'value'), Input('quarterly-year-dropdown', 'value')]
)
def update_quarterly_charts(selected_type, selected_year):
    quarter_order = ['Q1', 'Q2', 'Q3', 'Q4']  

    #Filter data for the selected year
    filtered_data = quarterly_data[quarterly_data['year'] == selected_year]

    
    if selected_type != 'All':
        filtered_data = filtered_data[filtered_data['Alcohol Type'] == selected_type]

    
    all_types = filtered_data['Alcohol Type'].unique() if selected_type == 'All' else [selected_type]
    all_combinations = pd.MultiIndex.from_product([quarter_order, all_types], names=["quarter", "Alcohol Type"])
    all_quarters = pd.DataFrame(index=all_combinations).reset_index()
    all_quarters['net_duty_paid_€m'] = 0  

    #Merge filtered data with all_quarters to include missing quarters
    combined_data = pd.merge(
        all_quarters,
        filtered_data[['quarter', 'Alcohol Type', 'net_duty_paid_€m']],
        on=['quarter', 'Alcohol Type'],
        how='left'
    ).fillna({'net_duty_paid_€m': 0})  

    #Fix the column naming issue
    combined_data['net_duty_paid_€m'] = combined_data['net_duty_paid_€m_x'].fillna(0) + combined_data['net_duty_paid_€m_y'].fillna(0)
    combined_data = combined_data.drop(columns=['net_duty_paid_€m_x', 'net_duty_paid_€m_y'])

    #Ensure quarter order is respected
    combined_data['quarter'] = pd.Categorical(combined_data['quarter'], categories=quarter_order, ordered=True)

    #Line Chart
    line_chart = px.line(
        combined_data,
        x='quarter',
        y='net_duty_paid_€m',
        color='Alcohol Type',
        title=f"Quarterly Alcohol Consumption ({selected_type}) in {selected_year}",
        template='plotly_dark'
    )
    line_chart.update_layout(
        paper_bgcolor="black", plot_bgcolor="black",
        xaxis_title="Quarter", yaxis_title="Net Duty Paid (€m)"
    )

    #Stacked Bar Chart
    bar_chart = px.bar(
        combined_data,
        x='quarter',
        y='net_duty_paid_€m',
        color='Alcohol Type',
        barmode='stack',
        title=f"Alcohol Type Proportions in {selected_year}",
        template='plotly_dark'
    )
    bar_chart.update_layout(
        paper_bgcolor="black", plot_bgcolor="black",
        xaxis_title="Quarter", yaxis_title="Net Duty Paid (€m)"
    )

    return line_chart, bar_chart



@app.callback(
    [
        Output('globe-map', 'figure'),
        Output('ireland-map', 'figure'),
        Output('country-map', 'figure'),
        Output('comparison-stats', 'children')
    ],
    [
        Input('global-year-dropdown', 'value'),
        Input('globe-map', 'clickData')
    ]
)
def update_global_comparison(selected_year, click_data):
    filtered_data = merged_global[merged_global['Year'] == selected_year]
    globe_map = go.Figure()
    globe_map.add_trace(go.Scattergeo(
        lon=filtered_data['Longitude'],
        lat=filtered_data['Latitude'],
        text=filtered_data['Country'] + ": " + filtered_data['Alcohol Consumption'].astype(str) + " liters",
        marker=dict(
            size=(filtered_data['Alcohol Consumption'] / filtered_data['Alcohol Consumption'].max()) * 20,
            color=filtered_data['Alcohol Consumption'],
            colorscale="Viridis",
            colorbar=dict(title="Liters per Capita"),
            opacity=0.8,
        ),
        hoverinfo="text"
    ))
    globe_map.update_layout(
        geo=dict(
            projection=dict(type="orthographic"),
            showland=True,
            landcolor="rgb(30, 30, 30)",
            showocean=True,
            oceancolor="rgb(10, 10, 10)",
            showcoastlines=True,
            coastlinecolor="rgba(255, 255, 255, 0.5)",
            showcountries=True,
            countrycolor="rgba(200, 200, 200, 0.7)"
        ),
        paper_bgcolor="black",
        plot_bgcolor="black",
        margin=dict(l=0, r=0, t=30, b=0)
    )

    ireland_map_data = ireland_global_data[ireland_global_data['Year'] == selected_year]
    ireland_map = px.choropleth_mapbox(
        ireland_map_data,
        geojson=None,
        locations="Country",
        color="Alcohol Consumption",
        title=f"Ireland ({selected_year})",
        mapbox_style="carto-positron",
        center={"lat": 53.0, "lon": -8.0},
        zoom=6
    )

    selected_country = "United Kingdom"
    if click_data and "points" in click_data:
        selected_country = click_data['points'][0]['text'].split(":")[0]

    country_data = merged_global[(merged_global['Country'] == selected_country) & (merged_global['Year'] == selected_year)]
    country_map = px.choropleth_mapbox(
        country_data,
        geojson=None,
        locations="Country",
        color="Alcohol Consumption",
        title=f"{selected_country} ({selected_year})",
        mapbox_style="carto-positron",
        center={"lat": country_data["Latitude"].values[0], "lon": country_data["Longitude"].values[0]} if not country_data.empty else {"lat": 0, "lon": 0},
        zoom=3 if not country_data.empty else 1
    )

    ireland_consumption = ireland_map_data['Alcohol Consumption'].values[0] if not ireland_map_data.empty else 0
    country_consumption = country_data['Alcohol Consumption'].values[0] if not country_data.empty else 0
    comparison_text = html.Div([
        html.H4(f"Comparison for {selected_year}"),
        html.P(f"Ireland: {ireland_consumption:.2f} liters per capita"),
        html.P(f"{selected_country}: {country_consumption:.2f} liters per capita"),
        html.P(f"Difference: {abs(ireland_consumption - country_consumption):.2f} liters per capita")
    ])

    return globe_map, ireland_map, country_map, comparison_text

if __name__ == "__main__":
    app.run_server(debug=True)

