from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash.dependencies import ALL
import pandas as pd
import io
import base64
import datetime
from ratios import perform_financial_analysis, unit_conversion 
import dash
from io import StringIO
import plotly.graph_objects as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Global dictionary to store dataframes for analysis
uploaded_files = {'balance_sheet': None, 'income_statement': None, 'price_history': None}

app.layout = html.Div([
    html.Div([
        html.H1("FINANCIAL RATIO CALCULATOR", style={'textAlign': 'center', 'marginTop': '20px'}),
        html.H2("Upload Financial Documents", style={'marginTop': '15px', 'textAlign': 'center'})
    ]),
    
    html.Div([
        dcc.Upload(
            id='upload-balance-sheet',
            children=html.Div(['Drag and Drop or ', html.A('Select Balance Sheet Files')]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'marginBottom': '10px'
            },
            multiple=False
        ),
        html.Div(id='output-balance-sheet'),
        
        dcc.Upload(
            id='upload-income-statement',
            children=html.Div(['Drag and Drop or ', html.A('Select Income Statement Files')]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'marginBottom': '10px'
            },
            multiple=False
        ),
        html.Div(id='output-income-statement'),
        
        dcc.Upload(
            id='upload-price-history',
            children=html.Div(['Drag and Drop or ', html.A('Select Price History Files')]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'marginBottom': '10px'
            },
            multiple=False
        ),
        html.Div(id='output-price-history')
    ]),

    html.Button('ANALYZE', id='analyze-button', n_clicks=0, style={'marginTop': '20px', 'marginLeft': '50%'}),
    
    html.Div(id='analysis-output', style={'marginTop': '20px'}),
    
    dcc.Dropdown(
        id='ratio-dropdown',
        options=[],  # This will be populated dynamically
        placeholder='Select a ratio',
        multi=True,  # Allow multiple selections
        style={'width': '100%', 'padding': '20px', 'marginTop': '20px'}
    ),
    
    dcc.Graph(id='ratio-graph'),
    
    dcc.Store(id='results-data-store'),  # Hidden div for storing intermediate data
])



@callback(
    Output('analyze-button', 'style'),
    [Input('output-balance-sheet', 'children'),
     Input('output-income-statement', 'children'),
     Input('output-price-history', 'children')]
)
def update_button_visibility(balance_sheet_output, income_statement_output, price_history_output):
    # Check if all outputs have content, which indicates files have been successfully uploaded
    if balance_sheet_output and income_statement_output and price_history_output:
        return {'display': 'block'}  # Show button
    return {'display': 'none'}  # Hide button


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'xlsx' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
            # Store DataFrame in global dictionary
            return  html.Div([
                html.H5(filename),
                html.H6(datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')),
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns],
                    style_table={'overflowX': 'auto'},
                    page_size=10
                ),
                html.Hr(),
            ])
    except Exception as e:
        return html.Div([
            f'There was an error processing this file: {str(e)}'
        ])
    



# Callbacks for uploading files
@callback(Output('output-balance-sheet', 'children'),
          Input('upload-balance-sheet', 'contents'),
          State('upload-balance-sheet', 'filename'),
          State('upload-balance-sheet', 'last_modified'))
def update_output_balance_sheet(contents, filename, date):
    if contents:
        uploaded_files['balance_sheet'] = pd.read_excel(io.BytesIO(base64.b64decode(contents.split(',')[1])))
        return parse_contents(contents, filename, date)
    return html.Div("Please upload a file.")

@callback(Output('output-income-statement', 'children'),
          Input('upload-income-statement', 'contents'),
          State('upload-income-statement', 'filename'),
          State('upload-income-statement', 'last_modified'))
def update_output_income_statement(contents, filename, date):
    if contents:
        uploaded_files['income_statement'] = pd.read_excel(io.BytesIO(base64.b64decode(contents.split(',')[1])))
        return parse_contents(contents, filename, date)
    return html.Div("Please upload a file.")

@callback(Output('output-price-history', 'children'),
          Input('upload-price-history', 'contents'),
          State('upload-price-history', 'filename'),
          State('upload-price-history', 'last_modified'))
def update_output_price_history(contents, filename, date):
    if contents:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'xlsx' in filename:
                # Skip the first 15 rows
                df = pd.read_excel(io.BytesIO(decoded), skiprows=15)
                uploaded_files['price_history'] = df  # Storing it in a global dict
                return parse_contents(contents, filename, date)
        except Exception as e:
            return html.Div([
                'There was an error processing this file: {}'.format(e)
            ])
    return html.Div("Please upload a file.")




def flatten_columns(df):
    """Flatten MultiIndex columns into single-level by joining level names with an underscore."""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(map(str, col)).strip() for col in df.columns.values]
    return df

def clean_column_names(df):
    # Strip any prefixes up to and including the underscore
    df.columns = [col.split('_', 1)[-1] if '_' in col else col for col in df.columns]
    return df



@callback(Output('analysis-output', 'children'),
          Input('analyze-button', 'n_clicks'),
          prevent_initial_call=True)
def perform_analysis(n_clicks):
    if not all(df is not None for df in uploaded_files.values()):
        return html.Div("Please upload all required files before analyzing.")

    try:
        df_balance_sheet = uploaded_files['balance_sheet']
        df_income_statement = uploaded_files['income_statement']
        df_price_history = uploaded_files['price_history']
        df_income_statement = unit_conversion(df_balance_sheet, df_income_statement)


        results_df = perform_financial_analysis(df_balance_sheet, df_income_statement, df_price_history)

        if 'Time' in results_df.columns:
            results_df['Time'] = pd.to_datetime(results_df['Time'].str.replace("'", ""), format='%b %y')
            results_df.sort_values('Time', ascending=False, inplace=True)
            results_df['Time'] = results_df['Time'].dt.strftime('%b \'%y')

        results_df = flatten_columns(results_df)  # Flatten columns if they are MultiIndex
        results_df = clean_column_names(results_df)

        return dash_table.DataTable(
        data=results_df.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in results_df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'center',
            'padding': '10px',
            'border': '1px solid grey',
            'whiteSpace': 'normal',
            'height': 'auto',
            'minWidth': '150px',
            'width': '150px',
            'maxWidth': '300px'
        },
        style_header={
            'backgroundColor': 'lightgrey',
            'fontWeight': 'bold',
            'border': '2px solid black'
        },
        style_data={
            'border': '1px solid grey'
        },
        page_size=25,
        style_as_list_view=True,
        )
    except Exception as e:
        return html.Div(f"Error in analysis: {str(e)}")
    



# Callback to store results in dcc.Store after analysis
@app.callback(
    Output('results-data-store', 'data'),
    Input('analyze-button', 'n_clicks'),
    prevent_initial_call=True
)
def store_results(n_clicks):
    if not all(df is not None for df in uploaded_files.values()):
        return dash.no_update  # Ensures that all files must be uploaded

    df_balance_sheet = uploaded_files['balance_sheet']
    df_income_statement = uploaded_files['income_statement']
    df_price_history = uploaded_files['price_history']
    
    df_income_statement = unit_conversion(df_balance_sheet, df_income_statement)
    results_df = perform_financial_analysis(df_balance_sheet, df_income_statement, df_price_history)

    return results_df.to_json(date_format='iso', orient='split')

# Callback to update the dropdown options based on stored results
@app.callback(
    Output('ratio-dropdown', 'options'),
    Input('results-data-store', 'data')
)
def update_dropdown(data):
    if not data:
        return []
    df = pd.read_json(data, orient='split')
    # Adjust here if the columns are nested or have specific formats
    ratio_names = [' - '.join(col) if isinstance(col, tuple) else col for col in df.columns][1:]
    return [{'label': ratio, 'value': ratio} for ratio in ratio_names]




@app.callback(
    Output('ratio-graph', 'figure'),
    [Input('ratio-dropdown', 'value'), Input('results-data-store', 'data')]
)
def update_graph(selected_ratios, json_data):
    if not selected_ratios or not json_data:
        return px.line(title="Please select at least one ratio.")

    data = StringIO(json_data)
    df = pd.read_json(data, orient='split')

    # Format the 'Time' column to ensure it has only month and year
    df['Time'] = pd.to_datetime(df.iloc[:, 0], format='%b \'%y', errors='coerce')
    df.sort_values('Time', ascending=True, inplace=True)
    df['Time'] = df['Time'].dt.strftime('%b %Y')  # Format as 'Mon YYYY'

    # Create a plot DataFrame
    plot_df = pd.DataFrame()
    plot_df['Time'] = df['Time']

    for ratio in selected_ratios:
        category, metric = ratio.split(' - ')
        plot_df[ratio] = df[(category, metric)]

    # Initialize the figure
    fig = go.Figure()

    # Add each trace individually for better control over appearance and legend
    for ratio in selected_ratios:
        fig.add_trace(
            go.Scatter(
                x=plot_df['Time'],
                y=plot_df[ratio],
                mode='lines+markers+text',
                name=ratio,
                text=plot_df[ratio],  # This ensures text is added to each datapoint
                textposition='top center'
            )
        )

    # Update layout for better tooltip handling and x-axis formatting
    fig.update_layout(
        hovermode='x unified',  # Unified hover mode for better tooltip display
        xaxis=dict(
            tickmode='array',
            tickvals=plot_df['Time'],
            ticktext=plot_df['Time']
        ),
        yaxis_title='Ratio Value',
        legend_title='Ratios',
        title='Financial Ratios Over Time'
    )

    return fig








if __name__ == '__main__':
    app.run_server(debug=True)



