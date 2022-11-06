# As per Dash tutorial, to run
# Run this app with `python app_pie .py` and
# pip install dash pandas

# Imports for Dash, HTML, DCC (Dash Core Components)
from dash import Dash, html, dcc

# Dash input/output to update from UI components
from dash import Input, Output

# For drawing pie chart
import plotly.express as px

# Import for dataframes
import pandas as pd

# Import data set from github
netflix = pd.read_csv("https://raw.githubusercontent.com/practiceprobs/datasets/main/netflix-titles/netflix-titles.csv")

# Clean up show_id to be numeric and ensure data sorted by show_id
netflix['show_id'] = pd.to_numeric(netflix['show_id'].str.removeprefix('s'),errors='coerce')
netflix = netflix.sort_values('show_id')

# This will blow up data set but we only need to do this once
# Convert listed_in into array
netflix['listed_in'] = netflix['listed_in'].str.split(',')
# Then explode it so we have a row per title per each of its listed_in
netflix = netflix.explode('listed_in')
# Strip off leading spaces
netflix['listed_in'] = netflix['listed_in'].str.strip()

# Get unique lists for filters
# under_list =  filter(lambda x: x < min, weights)
countries = list(filter( lambda x: x != '', netflix['country'].sort_values().str.split(',').explode().str.strip().dropna().unique() ))
content_types = netflix['type'].sort_values().unique()
ratings = netflix[netflix['rating'].str.contains('min')==False]['rating'].dropna().sort_values().unique()

# Create our dash app
app = Dash( __name__ )

# layout will render to screen the HTML we build
app.layout = html.Div(children=[
    html.H1(children='Interactive Netflix Pie Chart'),

    # Container to hold and show filters
    html.Div([
        html.Label('Country', style={'flex':.1,'padding-right':'5px'}),
        dcc.Dropdown( id='countries', options=countries, value=None, multi=True, style={'flex': 4}),

        html.Label('Type', style={'flex':.1, 'padding-left':'5px','padding-right':'5px'}),
        dcc.Dropdown( id='content_type', options=content_types, value=None, multi=False, style={'flex':1}),

        html.Label('Rating', style={'flex':.1, 'padding-left':'5px','padding-right':'5px'}),
        dcc.Dropdown( id='ratings', options=ratings, value=None, multi=True, style={'flex':4}),

    ], style={'width':'100%', 'display': 'flex'}),

    html.Div([ dcc.Graph( id='netflix-pie', style={'width':'100%'}
    )])
])


# This is a DASH callback that listens for changes in the HTML
# We are looking to know when a filter changes and then update what is shown on screen.
@app.callback(
    Output('netflix-pie','figure'),
    Input('countries', 'value'),
    Input('content_type', 'value'),
    Input('ratings', 'value'),
)
def update_pie( countries, content_type, ratings ):
    """
        Return the figure which is the pie chart object. Filtering on current inputs.

        Parameters
        ----------
        countries: array of countries to filter
        content_type: the type to filter on
        ratings: array of ratings to filter
    """

    # Local variable for operating on data.
    dff = netflix

    # If we have release year then filter, otherwise we need to set the
    # We filter here and keep using dff so the next filter does not start from scratch
    if content_type != None:
        dff = netflix.loc[netflix['type']==content_type]

    # If we have anything to filter for countries
    if countries != None:
        dff = dff[dff['country'].notna()]
        dff = dff.loc[dff['country'].str.contains( "|".join(countries)) ]

    # If we have anything to filter for countries
    if ratings != None:
        dff = dff[dff['rating'].notna()]
        dff = dff.loc[dff['rating'].dropna().str.contains( "|".join(ratings)) ]

    # Set up dataframe to display with categories and counts
    counts = pd.DataFrame(dff['listed_in'].value_counts())

    # Group by so we can pick out first 3 titles, already sorted by show_id earlier
    gb = dff.groupby('listed_in')
    counts['title1'] = gb['title'].nth(0)
    counts['title2'] = gb['title'].nth(1)
    counts['title3'] = gb['title'].nth(2)

    # pie object
    fig = px.pie(
            # Our data with counts
            counts,
            # by specific
            values='listed_in',
            # Names are the listed_in categories, now the index in the counts
            names=counts.index,
            # Helps with template to show first 3 titles
            custom_data=['title1','title2','title3'],
            # Title of pie
            title='Categories of Netflix Shows',
        )
    # Pie is big, looks better with % inside pie
    fig.update_traces(textposition='inside')

    # To show the movies and info on hover
    fig.for_each_trace(
        lambda t: t.update( hovertemplate="<b>%{label}</b><br>Count %{value}<br>%{customdata[0]}" ),
    )
    # The HTML object needs the pie
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
