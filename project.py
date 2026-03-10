# hospital_dash_dashboard_no_dbc.py
# Hospital Management System Dashboard using Dash and Plotly with Matplotlib

import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

# ----------------------
# Sample Data
# ----------------------
np.random.seed(42)

# KPIs
total_patients = 471
avg_wait_time = 34.1  # minutes
avg_satisfaction = 5.3  # out of 10

# ER Usage Heatmap
days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
hours = [f'{h}AM' if h<12 else f'{h-12 if h>12 else 12}PM' for h in range(7,19)]
er_usage = np.random.randint(0,6,(len(days), len(hours)))

# Admin Progress
admin_required = 52.4  # percent

# Referral data
referrals = pd.DataFrame({
    'Type':['None','General Practice','Orthopedics','Physiotherapy','Neurology','Cardiology','Gastroenterology','Renal'],
    'Count':[266,96,54,17,15,13,9,1]
})

# Demographics
gender_counts = pd.DataFrame({'Gender':['Male','Female'],'Count':[244,227]})
age_groups = pd.DataFrame({'Age':[5,15,25,35,45,55,65,75],'Count':np.random.randint(10,50,8)})
race_counts = pd.DataFrame({
    'Race':['White','African American','Two or More Races','Declined','Asian','Pacific Islander','Native American/Alaska'],
    'Count':[140,104,79,55,39,31,23]
})

# Department data
dept_data = pd.DataFrame({
    'Department': ['Emergency', 'ICU', 'Surgery', 'Cardiology', 'Pediatrics'],
    'Patients': [150, 45, 60, 80, 70],
    'Bed_Utilization': [92, 87, 85, 88, 75]
})

# ----------------------
# Helper Functions
# ----------------------
def create_matplotlib_figure(chart_type='heatmap'):
    """Create matplotlib charts and return as base64 encoded image"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    if chart_type == 'heatmap':
        sns.heatmap(er_usage, annot=True, cmap='Blues', xticklabels=hours, yticklabels=days, ax=ax, fmt='d')
        ax.set_title('ER Usage Heatmap (Patients per Hour)', fontsize=14, fontweight='bold')
    elif chart_type == 'dept_distribution':
        ax.bar(dept_data['Department'], dept_data['Patients'], color='steelblue')
        ax.set_title('Patients by Department', fontsize=14, fontweight='bold')
        ax.set_ylabel('Number of Patients', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
    elif chart_type == 'bed_utilization':
        colors = ['green' if x > 90 else 'orange' if x > 75 else 'red' for x in dept_data['Bed_Utilization']]
        ax.barh(dept_data['Department'], dept_data['Bed_Utilization'], color=colors)
        ax.set_title('Bed Utilization Rate (%)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Utilization (%)', fontsize=12)
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close()
    data = base64.b64encode(buf.getvalue()).decode('utf8')
    return f'data:image/png;base64,{data}'

# ----------------------
# Dash App Setup
# ----------------------
app = dash.Dash(__name__)
app.title = "Hospital ER Dashboard"

# ----------------------
# Figures (Plotly)
# ----------------------
er_fig = px.imshow(er_usage, x=hours, y=days, color_continuous_scale='Blues', 
                   text_auto=True, aspect='auto', labels={'x':'Hour','y':'Day'},
                   title='ER Usage Heatmap').update_layout(height=350)

ref_fig = px.bar(referrals.sort_values('Count', ascending=True), 
                 x='Count', y='Type', orientation='h',
                 title='Patient Referrals').update_layout(height=300)

gender_fig = px.pie(gender_counts, names='Gender', values='Count',
                    title='Gender Distribution').update_layout(height=300)

age_fig = px.bar(age_groups, x='Age', y='Count', 
                 title='Age Distribution')
age_fig.update_layout(height=300, xaxis_title='Age Group', yaxis_title='Count')

race_fig = px.bar(race_counts.sort_values('Count', ascending=False), 
                  x='Race', y='Count',
                  title='Race Distribution').update_layout(height=300)

dept_fig = px.bar(dept_data, x='Department', y='Patients',
                  color='Bed_Utilization', title='Patients by Department',
                  color_continuous_scale='RdYlGn_r').update_layout(height=300)

# ----------------------
# Styles
# ----------------------
sidebar_style = {
    'position':'fixed',
    'top':0,
    'left':0,
    'bottom':0,
    'width':'16rem',
    'padding':'2rem 1rem',
    'backgroundColor':'#1f77b4',
    'color':'white',
    'overflowY':'auto',
    'boxShadow':'2px 0 5px rgba(0,0,0,0.1)'
}

sidebar_style_link = {
    'display':'block',
    'marginBottom':'0.5rem',
    'color':'white',
    'textDecoration':'none',
    'padding':'0.5rem',
    'borderRadius':'4px',
    'transition':'background 0.3s'
}

content_style = {
    'marginLeft':'18rem',
    'padding':'2rem 1rem',
    'backgroundColor':'#f5f5f5',
    'minHeight':'100vh'
}

card_style = {
    'backgroundColor':'white',
    'padding':'1rem',
    'borderRadius':'8px',
    'boxShadow':'0 2px 8px rgba(0,0,0,0.1)',
    'marginBottom':'1rem',
    'border':'1px solid #ddd'
}

kpi_row_style = {
    'display':'flex',
    'gap':'1rem',
    'flexWrap':'wrap',
    'marginBottom':'2rem'
}

kpi_card_style = {
    'flex':'1',
    'minWidth':'12rem',
    'backgroundColor':'#ffffff',
    'padding':'1.5rem',
    'borderRadius':'8px',
    'boxShadow':'0 4px 12px rgba(0,0,0,0.1)',
    'border':'2px solid #e3f2fd'
}

progress_bar_container = {
    'backgroundColor':'#e9ecef',
    'borderRadius':'10px',
    'overflow':'hidden',
    'height':'30px',
    'width':'80%',
    'boxShadow':'inset 0 2px 4px rgba(0,0,0,0.1)'
}

progress_bar_inner = {
    'height':'100%',
    'width':f'{admin_required}%',
    'backgroundColor':'#4caf50',
    'textAlign':'center',
    'color':'white',
    'lineHeight':'30px',
    'fontWeight':'bold',
    'transition':'width 0.3s ease'
}

# ----------------------
# Layout
# ----------------------
app.layout = html.Div([
    # Sidebar
    html.Div([
        html.H2("🏥 RWFD", style={'marginBottom':'1rem', 'textAlign':'center'}),
        html.Hr(style={'borderColor':'rgba(255,255,255,0.2)'}),
        html.Div([
            html.H5("Navigation", style={'marginTop':'1rem'}),
            html.A("📊 Summary", href="#summary", style=sidebar_style_link),
            html.A("👥 Patients", href="#patients", style=sidebar_style_link),
            html.A("🏨 Departments", href="#departments", style=sidebar_style_link),
            html.Hr(style={'borderColor':'rgba(255,255,255,0.2)'}),
            html.H5("Export", style={'marginTop':'1rem'}),
            html.Button("📥 Download Data", id='download-btn', n_clicks=0, style={'margin':'0.2rem', 'width':'100%', 'padding':'0.5rem', 'backgroundColor':'#4caf50', 'color':'white', 'border':'none', 'borderRadius':'4px', 'cursor':'pointer'}),
            html.Hr(style={'borderColor':'rgba(255,255,255,0.2)'}),
            html.H5("Filters", style={'marginTop':'1rem'}),
            dcc.DatePickerRange(
                id='date_picker',
                start_date='2026-01-01',
                end_date='2026-01-14',
                style={'width':'100%'}
            ),
            dcc.Dropdown(
                id='dept_dropdown',
                options=[{'label':'All Departments', 'value':'all'}] + [{'label':d, 'value':d} for d in dept_data['Department']],
                value='all',
                placeholder='Select Department',
                style={'marginTop':'10px'}
            )
        ])
    ], style=sidebar_style),

    # Main Content
    html.Div([
        html.H1('🏥 Hospital ER Management Dashboard', style={'color':'#1f77b4', 'textAlign':'center'}),
        html.Hr(),

        # Charts Section
        html.Div([
            html.Div([
                html.H3('📈 ER Usage Pattern', style={'color':'#1f77b4'}),
                dcc.Graph(figure=er_fig, id='er-heatmap')
            ], style={**card_style, 'marginBottom':'2rem'}),

            html.Div([
                html.H3('⚠️ Admin Alert', style={'color':'#d32f2f'}),
                html.P(f'Admin Required: {admin_required}%', style={'fontSize':'18px'}),
                html.Div([
                    html.Div(style=progress_bar_inner, children=f'{admin_required}%')
                ], style=progress_bar_container),
            ], style={**card_style, 'marginBottom':'2rem'}),
        ]),

        # Three Column Layout
        html.Div([
            html.Div([
                html.H3('📋 Referrals', style={'color':'#1f77b4'}),
                dcc.Graph(figure=ref_fig, id='referral-chart')
            ], style={**card_style, 'width':'48%', 'display':'inline-block', 'marginRight':'2%'}),
            
            html.Div([
                html.H3('🏨 Departments', style={'color':'#1f77b4'}),
                dcc.Graph(figure=dept_fig, id='dept-chart')
            ], style={**card_style, 'width':'48%', 'display':'inline-block'})
        ], style={'marginBottom':'2rem'}),

        # Demographics Section
        html.Div([
            html.H2('👨‍👩‍👧‍👦 Patient Demographics', style={'color':'#1f77b4', 'marginBottom':'1rem'}),
            html.Div([
                html.Div([
                    dcc.Graph(figure=gender_fig, id='gender-chart', config={'displayModeBar':False})
                ], style={**card_style, 'width':'32%', 'display':'inline-block', 'marginRight':'1%'}),
                html.Div([
                    dcc.Graph(figure=age_fig, id='age-chart', config={'displayModeBar':False})
                ], style={**card_style, 'width':'32%', 'display':'inline-block', 'marginRight':'1%'}),
                html.Div([
                    dcc.Graph(figure=race_fig, id='race-chart', config={'displayModeBar':False})
                ], style={**card_style, 'width':'32%', 'display':'inline-block'})
            ])
        ]),

        # Matplotlib Charts
        html.Div([
            html.H2('📊 Advanced Analytics (Matplotlib)', style={'color':'#1f77b4', 'marginBottom':'1rem'}),
            html.Div([
                html.Div([
                    html.H4('Heatmap Analysis', style={'color':'#1f77b4'}),
                    html.Img(id='matplotlib-heatmap', style={'width':'100%', 'maxHeight':'400px'})
                ], style={**card_style, 'width':'48%', 'display':'inline-block', 'marginRight':'2%'}),
                html.Div([
                    html.H4('Bed Utilization', style={'color':'#1f77b4'}),
                    html.Img(id='matplotlib-bed', style={'width':'100%', 'maxHeight':'400px'})
                ], style={**card_style, 'width':'48%', 'display':'inline-block'})
            ])
        ], style={'marginBottom':'2rem'}),

    ], style=content_style),

    # Store for data persistence
    dcc.Store(id='session-data', data={})
])

# ----------------------
# Callbacks
# ----------------------
@callback(
    [Output('matplotlib-heatmap', 'src'),
     Output('matplotlib-bed', 'src')],
    [Input('dept_dropdown', 'value')]
)
def update_matplotlib_charts(selected_dept):
    """Update matplotlib charts based on department selection"""
    heatmap_img = create_matplotlib_figure('heatmap')
    bed_img = create_matplotlib_figure('bed_utilization')
    return heatmap_img, bed_img

# ----------------------
# Run App
# ----------------------
if __name__=='__main__':
    print("🚀 Starting Hospital ER Dashboard...")
    print("📱 Access the dashboard at: http://localhost:8050")
    app.run(debug=True, host='0.0.0.0', port=8050)
