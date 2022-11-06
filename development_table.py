# As per Dash tutorial, to run
# Run this app with `python app.py`
# pip install dash pandas

# Imports for Dash, HTML, DCC (Dash Core Components)
from dash import Dash, html, dcc
from dash import dash_table, Input, Output
# Import for dataframes
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Import data set from github
netflix = pd.read_csv("https://raw.githubusercontent.com/practiceprobs/datasets/main/netflix-titles/netflix-titles.csv")

# To get list of years
netflix['release_year'] = pd.to_numeric(netflix['release_year'])
release_years = netflix['release_year'].sort_values().unique()

# To get a list of listed_in categories
listed_in = netflix['listed_in'].str.split(',').explode().str.strip().unique()

# Start dash server side app with app.py as name
app = Dash( __name__ )

app.layout = html.Div(children=[
    html.H1(children='Interactive Netflix Table'),

    # html.Div([
    #     # "release_year: ", dcc.Input(id='release_year', value=None, type='number'),
    #     # "listed_in: ", dcc.Input(id='listed_in', value=None, type='text')
    # ]),

    html.Div([
        html.Label('Release Year', style={'flex':.1,'padding-right':'5px'}),
        dcc.Dropdown( id='release_year', options=release_years, value=None, multi=False, style={'flex': 1}),
        html.Label('Category Selector', style={'flex':.1, 'padding-left':'5px','padding-right':'5px'}),
        dcc.Dropdown( id='listed_in', options=listed_in, value=None, multi=True, style={'flex':5}),
        dcc.RadioItems( id='and_or', options=['and', 'or'], value='or', style={'flex':.3}),
    ], style={'width':'100%', 'display': 'flex'}),


    html.Div([ dash_table.DataTable( id='netflix-table',

        # To get fields to wrap and fit width of screen
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px'
        },
        # Quick way to show your fields
        columns=[{'id': c, 'name': c} for c in ['title','country','release_year','listed_in']],
        # Use this one if you want to show ALL columns
        # columns=[{'id': c, 'name': c} for c in netflix.columns],
        # If you want more control over the fields you show
        # columns = [
        #     { "id": "title", "name": "Title",
        #     "hideable":False,"clearable": False,"deletable": False, "selectable": False },
        #     { "id": "country", "name": "Country",
        #     "hideable":False,"clearable": False,"deletable": False, "selectable": False },
        #     { "id": "release_year", "name": "Year", "type":"numeric",
        #     "hideable":False,"clearable": False,"deletable": False, "selectable": False },
        #     { "id": "listed_in", "name": "Category",
        #     "hideable":False,"clearable": False,"deletable": False, "selectable": False },
        # ],

        # Give it some sorting that's built in
        sort_action="native",
        sort_mode="single",

        # Paging of data
        page_current= 0,
        page_size= 100,
    )])
])


# This is a DASH callback that listens for changes in the HTML
# We are looking to know when a filter changes and then update what is shown on screen.
# for Year we only support one selected year
# but for category you can select multiple and decided AND or OR
# This is just example of what could be done.
@app.callback(
    Output('netflix-table','data'),
    Input('release_year', 'value'),
    Input('listed_in', 'value'),
    Input('and_or', 'value'),
)
def update_table( release_year, listed_in, and_or ):

    # Local variable for operating on data.
    dff = netflix

    # If we have release year then filter, otherwise we need to set the
    # We filter here and keep using dff so the next filter does not start from scratch
    if release_year != None:
        dff = netflix.loc[netflix['release_year']==release_year]

    # If we have anything to filter for listed_in
    if listed_in != None:

        # If we need to OR operations we can just use the str syntax A|B|C
        if and_or == "or":
            dff = dff.loc[dff['listed_in'].str.contains( "|".join(listed_in)) ]

        # For and there is no quick implementation, so iterate through the choices and filter down
        else:
            for str in listed_in:
                print( "Locate", str)
                dff = dff.loc[dff['listed_in'].str.contains( str ) ]

    # The HTML object needs the records from pandas
    return dff.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
