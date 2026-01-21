# Metro Management System Web App (Final Year Project Version)
# Features: Trains CRUD, Commuters CRUD, Tickets, Dashboard, Charts

import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

# External CSS for professional styling
external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap'
]

# ---------------- Database Setup ----------------
conn = sqlite3.connect('metro.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS trains (train_id TEXT PRIMARY KEY, source TEXT, destination TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS commuters (commuter_id TEXT PRIMARY KEY, name TEXT, train_id TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS tickets (ticket_id TEXT PRIMARY KEY, commuter_id TEXT, train_id TEXT)")
conn.commit()

# ---------------- App Setup ----------------
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Metro Management System"

# Custom CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Roboto', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 0;
                margin: 0;
            }
            #react-entry-point {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px 0;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# ---------------- Layout ----------------
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1("🚇 Metro Management System", style={
                'textAlign': 'center',
                'color': 'white',
                'fontSize': '48px',
                'fontWeight': '700',
                'marginBottom': '10px',
                'textShadow': '2px 2px 4px rgba(0,0,0,0.3)'
            }),
            html.P("Efficient Urban Transit Management Platform", style={
                'textAlign': 'center',
                'color': 'rgba(255,255,255,0.9)',
                'fontSize': '16px',
                'fontWeight': '300',
                'marginTop': '5px'
            })
        ], style={
            'padding': '40px 20px',
            'background': 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
            'borderRadius': '10px',
            'marginBottom': '30px',
            'boxShadow': '0 8px 32px rgba(0,0,0,0.2)'
        })
    ], style={
        'maxWidth': '1200px',
        'margin': '30px auto',
        'padding': '0 20px'
    }),

    html.Div([
        dcc.Tabs([
            dcc.Tab(label='📊 Dashboard', children=[
                html.Div([
                    html.Div(id='stats', style={
                        'fontSize': '18px',
                        'fontWeight': 'bold',
                        'marginBottom': '20px',
                        'padding': '25px',
                        'backgroundColor': 'white',
                        'borderRadius': '10px',
                        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
                        'display': 'flex',
                        'justifyContent': 'space-around',
                        'flexWrap': 'wrap',
                        'gap': '20px'
                    }),
                    html.Div([
                        dcc.Graph(id='train-chart', style={'borderRadius': '10px'})
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '20px',
                        'marginBottom': '20px',
                        'borderRadius': '10px',
                        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)'
                    }),
                    html.Div([
                        dcc.Graph(id='commuter-chart', style={'borderRadius': '10px'})
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '20px',
                        'borderRadius': '10px',
                        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)'
                    })
                ], style={'padding': '20px'})
            ]),

            dcc.Tab(label='🚂 Trains', children=[
                html.Div([
                    html.Div([
                        html.H3("Add New Train", style={'color': '#d32f2f', 'marginBottom': '15px', 'fontSize': '20px'}),
                        html.Div([
                            dcc.Input(id='tid', placeholder='Train ID', type='text', style={
                                'margin': '8px',
                                'padding': '12px',
                                'border': '2px solid #d32f2f',
                                'borderRadius': '8px',
                                'fontSize': '14px',
                                'width': '150px'
                            }),
                            dcc.Input(id='tsrc', placeholder='Source', type='text', style={
                                'margin': '8px',
                                'padding': '12px',
                                'border': '2px solid #d32f2f',
                                'borderRadius': '8px',
                                'fontSize': '14px',
                                'width': '150px'
                            }),
                            dcc.Input(id='tdest', placeholder='Destination', type='text', style={
                                'margin': '8px',
                                'padding': '12px',
                                'border': '2px solid #d32f2f',
                                'borderRadius': '8px',
                                'fontSize': '14px',
                                'width': '150px'
                            }),
                            html.Button('Add Train', id='add-train', style={
                                'padding': '12px 25px',
                                'margin': '8px',
                                'backgroundColor': '#d32f2f',
                                'color': 'white',
                                'border': 'none',
                                'cursor': 'pointer',
                                'borderRadius': '8px',
                                'fontSize': '14px',
                                'fontWeight': '600',
                                'boxShadow': '0 4px 15px rgba(211, 47, 47, 0.3)',
                                'transition': 'all 0.3s ease'
                            })
                        ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '10px', 'marginBottom': '15px'}),
                        html.Div(id='train-msg', style={'color': 'green', 'marginTop': '10px', 'fontWeight': 'bold'})
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '20px',
                        'borderRadius': '10px',
                        'marginBottom': '20px',
                        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)'
                    }),
                    html.Hr(style={'borderColor': 'rgba(0,0,0,0.1)', 'margin': '20px 0'}),
                    html.H3("Trains List", style={'color': '#d32f2f', 'marginBottom': '15px', 'fontSize': '20px'}),
                    html.Div([
                        dash_table.DataTable(id='train-table', style_cell={
                            'textAlign': 'left',
                            'padding': '12px',
                            'fontFamily': 'Roboto, sans-serif',
                            'fontSize': '14px'
                        }, style_header={
                            'backgroundColor': '#d32f2f',
                            'color': 'white',
                            'fontWeight': 'bold',
                            'textAlign': 'left',
                            'padding': '12px'
                        }, style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
                        ])
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '20px',
                        'borderRadius': '10px',
                        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
                        'overflowX': 'auto'
                    })
                ], style={'padding': '20px'})
            ]),

            dcc.Tab(label='👥 Commuters', children=[
                html.Div([
                    html.Div([
                        html.H3("Add New Commuter", style={'color': '#388e3c', 'marginBottom': '15px', 'fontSize': '20px'}),
                        html.Div([
                            dcc.Input(id='cid', placeholder='Commuter ID', type='text', style={
                                'margin': '8px',
                                'padding': '12px',
                                'border': '2px solid #388e3c',
                                'borderRadius': '8px',
                                'fontSize': '14px',
                                'width': '150px'
                            }),
                            dcc.Input(id='cname', placeholder='Name', type='text', style={
                                'margin': '8px',
                                'padding': '12px',
                                'border': '2px solid #388e3c',
                                'borderRadius': '8px',
                                'fontSize': '14px',
                                'width': '150px'
                            }),
                            dcc.Input(id='ctrain', placeholder='Train ID', type='text', style={
                                'margin': '8px',
                                'padding': '12px',
                                'border': '2px solid #388e3c',
                                'borderRadius': '8px',
                                'fontSize': '14px',
                                'width': '150px'
                            }),
                            html.Button('Add Commuter', id='add-commuter', style={
                                'padding': '12px 25px',
                                'margin': '8px',
                                'backgroundColor': '#388e3c',
                                'color': 'white',
                                'border': 'none',
                                'cursor': 'pointer',
                                'borderRadius': '8px',
                                'fontSize': '14px',
                                'fontWeight': '600',
                                'boxShadow': '0 4px 15px rgba(56, 142, 60, 0.3)',
                                'transition': 'all 0.3s ease'
                            })
                        ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '10px', 'marginBottom': '15px'}),
                        html.Div(id='commuter-msg', style={'color': 'green', 'marginTop': '10px', 'fontWeight': 'bold'})
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '20px',
                        'borderRadius': '10px',
                        'marginBottom': '20px',
                        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)'
                    }),
                    html.Hr(style={'borderColor': 'rgba(0,0,0,0.1)', 'margin': '20px 0'}),
                    html.H3("Commuters List", style={'color': '#388e3c', 'marginBottom': '15px', 'fontSize': '20px'}),
                    html.Div([
                        dash_table.DataTable(id='commuter-table', style_cell={
                            'textAlign': 'left',
                            'padding': '12px',
                            'fontFamily': 'Roboto, sans-serif',
                            'fontSize': '14px'
                        }, style_header={
                            'backgroundColor': '#388e3c',
                            'color': 'white',
                            'fontWeight': 'bold',
                            'textAlign': 'left',
                            'padding': '12px'
                        }, style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
                        ])
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '20px',
                        'borderRadius': '10px',
                        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
                        'overflowX': 'auto'
                    })
                ], style={'padding': '20px'})
            ]),

            dcc.Tab(label='🎫 Tickets', children=[
                html.Div([
                    html.Div([
                        html.H3("Add New Ticket", style={'color': '#f57c00', 'marginBottom': '15px', 'fontSize': '20px'}),
                        html.Div([
                            dcc.Input(id='tickid', placeholder='Ticket ID', type='text', style={
                                'margin': '8px',
                                'padding': '12px',
                                'border': '2px solid #f57c00',
                                'borderRadius': '8px',
                                'fontSize': '14px',
                                'width': '150px'
                            }),
                            dcc.Input(id='tickcid', placeholder='Commuter ID', type='text', style={
                                'margin': '8px',
                                'padding': '12px',
                                'border': '2px solid #f57c00',
                                'borderRadius': '8px',
                                'fontSize': '14px',
                                'width': '150px'
                            }),
                            dcc.Input(id='ticktid', placeholder='Train ID', type='text', style={
                                'margin': '8px',
                                'padding': '12px',
                                'border': '2px solid #f57c00',
                                'borderRadius': '8px',
                                'fontSize': '14px',
                                'width': '150px'
                            }),
                            html.Button('Add Ticket', id='add-ticket', style={
                                'padding': '12px 25px',
                                'margin': '8px',
                                'backgroundColor': '#f57c00',
                                'color': 'white',
                                'border': 'none',
                                'cursor': 'pointer',
                                'borderRadius': '8px',
                                'fontSize': '14px',
                                'fontWeight': '600',
                                'boxShadow': '0 4px 15px rgba(245, 124, 0, 0.3)',
                                'transition': 'all 0.3s ease'
                            })
                        ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '10px', 'marginBottom': '15px'}),
                        html.Div(id='ticket-msg', style={'color': 'green', 'marginTop': '10px', 'fontWeight': 'bold'})
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '20px',
                        'borderRadius': '10px',
                        'marginBottom': '20px',
                        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)'
                    }),
                    html.Hr(style={'borderColor': 'rgba(0,0,0,0.1)', 'margin': '20px 0'}),
                    html.H3("Tickets List", style={'color': '#f57c00', 'marginBottom': '15px', 'fontSize': '20px'}),
                    html.Div([
                        dash_table.DataTable(id='ticket-table', style_cell={
                            'textAlign': 'left',
                            'padding': '12px',
                            'fontFamily': 'Roboto, sans-serif',
                            'fontSize': '14px'
                        }, style_header={
                            'backgroundColor': '#f57c00',
                            'color': 'white',
                            'fontWeight': 'bold',
                            'textAlign': 'left',
                            'padding': '12px'
                        }, style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
                        ])
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '20px',
                        'borderRadius': '10px',
                        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
                        'overflowX': 'auto'
                    })
                ], style={'padding': '20px'})
            ])
        ], style={
            'maxWidth': '1200px',
            'margin': '0 auto',
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'boxShadow': '0 10px 40px rgba(0,0,0,0.2)',
            'marginBottom': '50px'
        })
    ], style={
        'padding': '20px'
    })
], style={
    'fontFamily': "'Roboto', sans-serif",
    'backgroundColor': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'minHeight': '100vh',
    'paddingTop': '20px',
    'paddingBottom': '20px'
})
# ---------------- Callbacks ----------------
@app.callback(
    Output('train-table', 'data'),
    Output('train-table', 'columns'),
    Output('tid', 'value'),
    Output('tsrc', 'value'),
    Output('tdest', 'value'),
    Output('train-msg', 'children'),
    Input('add-train', 'n_clicks'),
    State('tid', 'value'),
    State('tsrc', 'value'),
    State('tdest', 'value'),
    prevent_initial_call=True
)
def update_trains(n, tid, src, dest):
    msg = ""
    if n and tid and src and dest:
        try:
            cursor.execute("INSERT INTO trains VALUES (?,?,?)", (tid, src, dest))
            conn.commit()
            msg = "✅ Train added successfully!"
        except sqlite3.IntegrityError:
            msg = "⚠️ Train ID already exists!"
    
    df = pd.read_sql('SELECT * FROM trains', conn)
    columns = [{"name": i, "id": i} for i in df.columns] if not df.empty else []
    return df.to_dict('records'), columns, "", "", "", msg

@app.callback(
    Output('commuter-table', 'data'),
    Output('commuter-table', 'columns'),
    Output('cid', 'value'),
    Output('cname', 'value'),
    Output('ctrain', 'value'),
    Output('commuter-msg', 'children'),
    Input('add-commuter', 'n_clicks'),
    State('cid', 'value'),
    State('cname', 'value'),
    State('ctrain', 'value'),
    prevent_initial_call=True
)
def update_commuters(n, cid, cname, ctrain):
    msg = ""
    if n and cid and cname and ctrain:
        try:
            cursor.execute("INSERT INTO commuters VALUES (?,?,?)", (cid, cname, ctrain))
            conn.commit()
            msg = "✅ Commuter added successfully!"
        except sqlite3.IntegrityError:
            msg = "⚠️ Commuter ID already exists!"
    
    df = pd.read_sql('SELECT * FROM commuters', conn)
    columns = [{"name": i, "id": i} for i in df.columns] if not df.empty else []
    return df.to_dict('records'), columns, "", "", "", msg

@app.callback(
    Output('ticket-table', 'data'),
    Output('ticket-table', 'columns'),
    Output('tickid', 'value'),
    Output('tickcid', 'value'),
    Output('ticktid', 'value'),
    Output('ticket-msg', 'children'),
    Input('add-ticket', 'n_clicks'),
    State('tickid', 'value'),
    State('tickcid', 'value'),
    State('ticktid', 'value'),
    prevent_initial_call=True
)
def update_tickets(n, tickid, tickcid, ticktid):
    msg = ""
    if n and tickid and tickcid and ticktid:
        try:
            cursor.execute("INSERT INTO tickets VALUES (?,?,?)", (tickid, tickcid, ticktid))
            conn.commit()
            msg = "✅ Ticket added successfully!"
        except sqlite3.IntegrityError:
            msg = "⚠️ Ticket ID already exists!"
    
    df = pd.read_sql('SELECT * FROM tickets', conn)
    columns = [{"name": i, "id": i} for i in df.columns] if not df.empty else []
    return df.to_dict('records'), columns, "", "", "", msg

@app.callback(
    Output('stats', 'children'),
    Output('train-chart', 'figure'),
    Output('commuter-chart', 'figure'),
    Input('train-table', 'data'),
    Input('commuter-table', 'data'),
    Input('ticket-table', 'data')
)
def update_dashboard(t_data, c_data, tk_data):
    t_count = len(t_data) if t_data else 0
    c_count = len(c_data) if c_data else 0
    tk_count = len(tk_data) if tk_data else 0
    
    stats = html.Div([
        html.Span(f"🚂 Trains: {t_count} | ", style={'marginRight': '20px'}),
        html.Span(f"👥 Commuters: {c_count} | ", style={'marginRight': '20px'}),
        html.Span(f"🎫 Tickets: {tk_count}", style={'marginRight': '20px'})
    ])
    
    # Train chart
    if t_data:
        df_trains = pd.DataFrame(t_data)
        train_fig = px.bar(df_trains, x='source', y='destination', title='Trains by Source', 
                           color='destination', barmode='group')
    else:
        train_fig = go.Figure().add_annotation(text="No trains yet", showarrow=False)
        train_fig.update_layout(title='Trains by Source')
    
    # Commuter chart
    if c_data and t_data:
        df_commuters = pd.DataFrame(c_data)
        df_trains = pd.DataFrame(t_data)
        commuter_counts = df_commuters['train_id'].value_counts()
        commuter_fig = px.pie(values=commuter_counts.values, names=commuter_counts.index, 
                              title='Commuters per Train')
    else:
        commuter_fig = go.Figure().add_annotation(text="No commuters yet", showarrow=False)
        commuter_fig.update_layout(title='Commuters per Train')
    
    return stats, train_fig, commuter_fig

# ---------------- Run ----------------
if __name__ == '__main__':
    app.run(debug=True)
