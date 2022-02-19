from dash import Dash, html, dcc, Input, Output
import pandas as pd
import altair as alt
from vega_datasets import data


app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])


metrics={'life_expectancy':'Life Expectancy', 'child_mortality':'Child Mortality', 'pop_density':'Population Density'}
# def plot_world():
gap = pd.read_csv('gapminder.csv')
country_ids=pd.read_csv('country_ids.csv')
gap = gap.merge(country_ids, how="outer", on=["country"])
@app.callback(
    Output("map", "srcDoc"),
    Input("metric", "value")
)
def plot(metric):
    return plot_world_map(metric)


def plot_world_map(metric):

    
    
    world = data.world_110m()
    world_map = alt.topo_feature(data.world_110m.url, 'countries')
    alt.data_transformers.disable_max_rows()
    # title_metric=metric.replace("_", " ")
    # title_metric=title_metric.capitalize()
    chart = alt.Chart(world_map, title=f"{metrics[metric]} by country").mark_geoshape(stroke="black").transform_lookup(lookup="id", from_=alt.LookupData(gap, key="id", fields=["country", metric])
            ).encode(
                tooltip=["country:O", metric + ":Q"],
                color=alt.Color(metric + ":Q", title=metrics[metric]))
    return chart.to_html()

app.layout = html.Div([
    html.Div([
    dcc.RadioItems(id='metric', value='life_expectancy',
        options=[{'label': v, 'value': k} for k, v in metrics.items()]),
    
    

    'Year',
    dcc.Dropdown(id='year_dropdown', 
    options=[
            {'label': '1990', 'value': '1990'},
            {'label': '2000', 'value': '2000'},
            {'label': '2012', 'value': '2012'},
            {'label': '2015', 'value': '2015'}
            ],
        value='2012')] ) ,
        html.Iframe(id='map',
                 style={'border-width': '0', 'width': '100%', 'height': '600px'})
 
    # dcc.RangeSlider(1980, 2018, value=[5, 15], id='year_slider')
    # dcc.RangeSlider(id='year_slider', min=gap['year'].min(), max=gap['year'].max(), value=[1800, 2018])
                 
    ])











if __name__ == '__main__':
    app.run_server(debug=True)