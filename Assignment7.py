#!/usr/bin/env python
# coding: utf-8

# In[3]:


#import dash
from dash import dcc, html, Output, Input, ctx
import plotly.express as px
import pandas as pd

#create dataFrames
world_cup = pd.DataFrame({
    "win": ["Uruguay", "Italy", "Italy", "Uruguay", "Germany", "Brazil", "Brazil", "England", "Brazil", "Germany", "Argentina", "Italy", "Argentina", "Germany", "Brazil", "France", "Brazil", "Italy", "Spain", "Germany", "France", "Argentina"],
    "run": ["Argentina", "Czechoslovakia", "Hungary", "Brazil", "Hungary", "Sweden", "Czechoslovakia", "Germany", "Italy", "Netherlands", "Netherlands", "Germany", "Germany", "Argentina", "Italy", "Brazil", "Germany", "France", "Netherlands", "Argentina", "Croatia", "France"],
    "year": [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022]
})
total = pd.DataFrame({
    "country": ["Argentina", "Brazil", "England", "France", "Germany", "Italy", "Uruguay", "Spain"],
    "num_win": [3, 5, 1, 2, 4, 4, 2, 1]
})

#build graph for all
def graph_up(country, data):
    fig = px.choropleth(
        total,
        locations=country,
        locationmode="country names",
        color=data,
        color_continuous_scale="Viridis",
        scope="world",
        title="Number of FIFA Wins Per Country"
    )
    return fig

#layout Dash
app = dash.Dash()
server = app.run_server(debug=True, port=8050, host='0.0.0.0')

app.layout = html.Div([
    html.H1("FIFA Soccer World Cup Winners and Runner-ups"),
    html.Br(),
        html.Label('Number of FIFA World Cup wins'),
            dcc.Dropdown(["All", "Argentina", "Brazil", "England", "France", "Germany", "Italy", "Uruguay", "Spain"],
                         placeholder="Select a Country or All", id='country_win'),#placeholder="Select a Country",
    html.Br(),
        html.Label('Winner and Runner-up'),
        dcc.Dropdown(world_cup.year, placeholder="Select a Year", id='year_win'),
    
    html.Div([
        dcc.Graph(id='graph_c')
        #dcc.Graph(figure=fig)
    ])
    
])

@app.callback(
    Output("graph_c", "figure"),
    Output ("country_win", "value"),
    Output ("year_win", "value"),
    Input ("country_win", "value"),
    Input ("year_win", "value"),
    #prevent_initial_call=True
)

#update
def update_country_win(country_win, year_win):
    #prevent both dropdowns from having values
    triggered_id = ctx.triggered_id
    #make sure only value filled in for Number of FIFA World Cup wins
    if triggered_id == 'country_win' and country_win:
        #all countries results
        if country_win == "All":
            fig = graph_up("country", "num_win")
            return fig, country_win, None  # Reset year
        #Exception for England it is not a country
        elif country_win == "England":   
            row = total[total['country'] == country_win].iloc[0]
            wins = [row['num_win']]
            fig = px.choropleth(locations=['United Kingdom'], locationmode="country names", color=wins, scope="world", labels={'color':'Wins'}, title=country_win+" Number of FIFA Wins "+str(row['num_win']))
            fig.update_geos(fitbounds="locations")
            fig.update_layout(coloraxis_showscale=False)
            return fig, country_win, None  # Reset year
        else:
            row = total[total['country'] == country_win].iloc[0]
            wins = [row['num_win']]
            #fig = px.choropleth(locations=[country_win], locationmode="country names", hover_data=[row["num_win"]], scope="world")
            fig = px.choropleth(locations=[country_win], locationmode="country names", color=wins, scope="world", labels={'color':'Wins'}, title=country_win+" Number of FIFA Wins "+str(row['num_win']))
            fig.update_geos(fitbounds="locations")
            fig.update_layout(coloraxis_showscale=False)
            return fig, country_win, None  # Reset year

    # only dropdown box 'Winner and Runner-up'is selected
    elif triggered_id == 'year_win' and year_win:
        row = world_cup[world_cup['year'] == year_win].iloc[0]
        #exception Czechoslovakia is two countries
        if row['run'] == 'Czechoslovakia':
            countries = [row['win'], "Czech Republic", "Slovakia"]
            data = ["Winner", "Runner-up (Czechoslovakia)", "Runner-up (Czechoslovakia)"]
        #exception England is not a country
        elif row['win'] == 'England':
            countries = ['United Kingdom',row['run']]
            data = ["Winner (England)", "Runner-up"]
        
        else:
            countries = [row['win'],row['run']]
            data = ["Winner", "Runner-up"]
        #fig = px.choropleth(locations=[country_win], locationmode="country names", hover_data=[row["num_win"]], scope="world")
        fig = px.choropleth(locations=countries, locationmode="country names", color=data, scope="world", title=str(year_win)+" FIFA Winner and Runner-up", labels={'color':'Result'})
        fig.update_geos(fitbounds="locations")
        fig.update_layout(coloraxis_showscale=False)
        return fig, None, year_win  # Reset country
        
    #blank world map    
    else:
        fig = px.choropleth(locationmode="country names", scope="world", title="World Map")
        return fig, None, None
        
app.run(debug=True)


# In[ ]:





# In[ ]:




