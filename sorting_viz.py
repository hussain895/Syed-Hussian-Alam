# Premium Sorting Algorithm Visualizer
# Advanced web-based interactive visualizer with enhanced UI/UX

import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import numpy as np

# ----------------------
# Sorting Algorithms
# ----------------------

class SortingVisualizer:
    def __init__(self, array):
        self.original = array.copy()
        self.array = array.copy()
        self.steps = []
        self.comparisons = 0
        self.swaps = 0
        
    def reset(self):
        self.array = self.original.copy()
        self.steps = []
        self.comparisons = 0
        self.swaps = 0
        
    def record_step(self, array, active_indices=None, sorted_indices=None, title=""):
        self.steps.append({
            'array': array.copy(),
            'active': active_indices or [],
            'sorted': sorted_indices or [],
            'title': title
        })
    
    def bubble_sort(self):
        self.reset()
        n = len(self.array)
        
        for i in range(n):
            swapped = False
            for j in range(0, n-i-1):
                self.comparisons += 1
                self.record_step(self.array, active_indices=[j, j+1], 
                               sorted_indices=list(range(n-i, n)),
                               title=f"Comparing: {self.array[j]} and {self.array[j+1]}")
                
                if self.array[j] > self.array[j+1]:
                    self.array[j], self.array[j+1] = self.array[j+1], self.array[j]
                    self.swaps += 1
                    self.record_step(self.array, active_indices=[j, j+1],
                                   sorted_indices=list(range(n-i, n)),
                                   title=f"Swapped positions")
                    swapped = True
            
            if not swapped:
                break
        
        self.record_step(self.array, sorted_indices=list(range(n)), 
                       title="✅ Sorting Complete!")
        return self.steps
    
    def selection_sort(self):
        self.reset()
        n = len(self.array)
        
        for i in range(n):
            min_idx = i
            self.record_step(self.array, active_indices=[i], 
                           sorted_indices=list(range(i)),
                           title=f"Finding minimum from index {i}")
            
            for j in range(i+1, n):
                self.comparisons += 1
                self.record_step(self.array, active_indices=[min_idx, j],
                               sorted_indices=list(range(i)),
                               title=f"Comparing: {self.array[min_idx]} vs {self.array[j]}")
                
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
            
            if min_idx != i:
                self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
                self.swaps += 1
                self.record_step(self.array, active_indices=[i, min_idx],
                               sorted_indices=list(range(i+1)),
                               title=f"Placed minimum at position {i}")
        
        self.record_step(self.array, sorted_indices=list(range(n)), 
                       title="✅ Sorting Complete!")
        return self.steps
    
    def insertion_sort(self):
        self.reset()
        n = len(self.array)
        
        for i in range(1, n):
            key = self.array[i]
            j = i - 1
            
            self.record_step(self.array, active_indices=[i], 
                           sorted_indices=list(range(i)),
                           title=f"Inserting {key} into sorted portion")
            
            while j >= 0 and self.array[j] > key:
                self.comparisons += 1
                self.record_step(self.array, active_indices=[j, j+1],
                               sorted_indices=list(range(i)),
                               title=f"Comparing: {self.array[j]} > {key}")
                
                self.array[j+1] = self.array[j]
                self.swaps += 1
                j -= 1
                
                self.record_step(self.array, active_indices=[j+1],
                               sorted_indices=list(range(i+1)),
                               title=f"Shifting elements")
            
            self.array[j+1] = key
            self.record_step(self.array, sorted_indices=list(range(i+1)),
                           title=f"Placed {key} in correct position")
        
        self.record_step(self.array, sorted_indices=list(range(n)), 
                       title="✅ Sorting Complete!")
        return self.steps
    
    def merge_sort_helper(self, arr, left, right, sorted_indices):
        if left >= right:
            return arr
        
        mid = (left + right) // 2
        self.merge_sort_helper(arr, left, mid, sorted_indices)
        self.merge_sort_helper(arr, mid+1, right, sorted_indices)
        self.merge(arr, left, mid, right, sorted_indices)
        
        return arr
    
    def merge(self, arr, left, mid, right, sorted_indices):
        left_arr = arr[left:mid+1]
        right_arr = arr[mid+1:right+1]
        
        i = j = 0
        k = left
        
        while i < len(left_arr) and j < len(right_arr):
            self.comparisons += 1
            self.record_step(self.array, active_indices=[left+i, mid+1+j],
                           sorted_indices=sorted_indices,
                           title=f"Merging: comparing {left_arr[i]} and {right_arr[j]}")
            
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1
            self.swaps += 1
        
        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1
            self.swaps += 1
            
        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1
            self.swaps += 1
    
    def merge_sort(self):
        self.reset()
        n = len(self.array)
        self.merge_sort_helper(self.array, 0, n-1, [])
        self.record_step(self.array, sorted_indices=list(range(n)), 
                       title="✅ Sorting Complete!")
        return self.steps
    
    def heapify(self, n, i, sorted_indices):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n:
            self.comparisons += 1
            self.record_step(self.array, active_indices=[largest, left],
                           sorted_indices=sorted_indices,
                           title=f"Comparing: {self.array[largest]} vs {self.array[left]}")
            if self.array[left] > self.array[largest]:
                largest = left
        
        if right < n:
            self.comparisons += 1
            self.record_step(self.array, active_indices=[largest, right],
                           sorted_indices=sorted_indices,
                           title=f"Comparing: {self.array[largest]} vs {self.array[right]}")
            if self.array[right] > self.array[largest]:
                largest = right
        
        if largest != i:
            self.array[i], self.array[largest] = self.array[largest], self.array[i]
            self.swaps += 1
            self.record_step(self.array, active_indices=[i, largest],
                           sorted_indices=sorted_indices,
                           title=f"Swapped heap elements")
            self.heapify(n, largest, sorted_indices)
    
    def heap_sort(self):
        self.reset()
        n = len(self.array)
        
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(n, i, [])
        
        for i in range(n - 1, 0, -1):
            self.array[0], self.array[i] = self.array[i], self.array[0]
            self.swaps += 1
            self.record_step(self.array, active_indices=[0, i],
                           sorted_indices=list(range(i+1, n)),
                           title=f"Moving {self.array[i]} to sorted position")
            self.heapify(i, 0, list(range(i+1, n)))
        
        self.record_step(self.array, sorted_indices=list(range(n)), 
                       title="✅ Sorting Complete!")
        return self.steps
    
    def partition(self, low, high, sorted_indices):
        pivot = self.array[high]
        i = low - 1
        
        for j in range(low, high):
            self.comparisons += 1
            self.record_step(self.array, active_indices=[j, high],
                           sorted_indices=sorted_indices,
                           title=f"Comparing {self.array[j]} with pivot {pivot}")
            
            if self.array[j] < pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
                self.swaps += 1
                self.record_step(self.array, active_indices=[i, j],
                               sorted_indices=sorted_indices,
                               title=f"Swapped elements")
        
        self.array[i+1], self.array[high] = self.array[high], self.array[i+1]
        self.swaps += 1
        self.record_step(self.array, active_indices=[i+1, high],
                       sorted_indices=sorted_indices,
                       title=f"Pivot placed at position {i+1}")
        
        return i + 1
    
    def quick_sort_helper(self, low, high, sorted_indices):
        if low < high:
            pi = self.partition(low, high, sorted_indices)
            self.quick_sort_helper(low, pi - 1, sorted_indices)
            self.quick_sort_helper(pi + 1, high, sorted_indices)
    
    def quick_sort(self):
        self.reset()
        n = len(self.array)
        self.quick_sort_helper(0, n - 1, [])
        self.record_step(self.array, sorted_indices=list(range(n)), 
                       title="✅ Sorting Complete!")
        return self.steps


# ----------------------
# Dash App Setup
# ----------------------

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Sorting Visualizer"

# ----------------------
# Inline Styles
# ----------------------

COLORS = {
    'primary': '#2c3e50',
    'secondary': '#3498db',
    'success': '#27ae60',
    'danger': '#e74c3c',
    'warning': '#f39c12',
    'light': '#ecf0f1',
    'dark': '#2c3e50'
}

# ----------------------
# App Layout
# ----------------------

app.layout = html.Div([
    dcc.Store(id='visualizer-store', data={}),
    dcc.Store(id='autoplay-store', data={'playing': False}),
    
    html.Div([
        # Header
        html.Div([
            html.H1("🎨 Sorting Algorithm Visualizer", style={
                'color': 'white',
                'marginBottom': '0.5rem',
                'fontSize': '2.5rem'
            }),
            html.P("Watch different sorting algorithms in action", style={
                'color': '#ecf0f1',
                'fontSize': '1.1rem',
                'margin': '0'
            })
        ], style={
            'background': f'linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["secondary"]} 100%)',
            'padding': '2rem',
            'textAlign': 'center',
            'marginBottom': '2rem',
            'borderRadius': '0 0 10px 10px',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'
        }),
        
        # Main Container
        html.Div([
            # Left Panel - Controls
            html.Div([
                html.Div([
                    html.H3("⚙️ Controls", style={'marginBottom': '1rem', 'color': COLORS['primary']}),
                    
                    # Input Array
                    html.Div([
                        html.Label("Enter Array (comma-separated):", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '0.5rem'}),
                        dcc.Input(
                            id='array-input',
                            type='text',
                            placeholder='e.g., 64, 34, 25, 12, 22, 11, 90',
                            value='64, 34, 25, 12, 22, 11, 90, 88, 45, 50',
                            style={
                                'width': '100%',
                                'padding': '12px',
                                'fontSize': '13px',
                                'border': f'2px solid {COLORS["light"]}',
                                'borderRadius': '6px',
                                'boxSizing': 'border-box',
                                'fontFamily': 'monospace'
                            }
                        ),
                        html.Small("Or generate random data below", style={'color': '#7f8c8d', 'display': 'block', 'marginTop': '0.3rem'})
                    ], style={'marginBottom': '1.5rem'}),
                    
                    # Array Size
                    html.Div([
                        html.Label("Array Size:", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '0.5rem'}),
                        dcc.Slider(
                            id='array-size-slider',
                            min=5,
                            max=50,
                            step=1,
                            value=20,
                            marks={5: '5', 15: '15', 25: '25', 35: '35', 50: '50'},
                            tooltip={"placement": "bottom", "always_visible": True},
                            updatemode='drag'
                        )
                    ], style={'marginBottom': '1.5rem'}),
                    
                    # Algorithm Selection
                    html.Div([
                        html.Label("Select Algorithm:", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '0.5rem'}),
                        dcc.Dropdown(
                            id='algorithm-dropdown',
                            options=[
                                {'label': '🫧 Bubble Sort - O(n²)', 'value': 'bubble'},
                                {'label': '📍 Selection Sort - O(n²)', 'value': 'selection'},
                                {'label': '📥 Insertion Sort - O(n²)', 'value': 'insertion'},
                                {'label': '🔀 Merge Sort - O(n log n)', 'value': 'merge'},
                                {'label': '📚 Heap Sort - O(n log n)', 'value': 'heap'},
                                {'label': '⚡ Quick Sort - O(n log n)', 'value': 'quick'}
                            ],
                            value='bubble',
                            style={'width': '100%'}
                        )
                    ], style={'marginBottom': '1.5rem'}),
                    
                    # Speed Control
                    html.Div([
                        html.Label("Animation Speed:", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '0.5rem'}),
                        dcc.Slider(
                            id='speed-slider',
                            min=10,
                            max=1000,
                            step=50,
                            value=200,
                            marks={10: '🐇 Fast', 500: 'Medium', 1000: '🐢 Slow'},
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ], style={'marginBottom': '1.5rem'}),
                    
                    # Control Buttons
                    html.Div([
                        html.Button(
                            '▶️ Start',
                            id='start-button',
                            n_clicks=0,
                            style={
                                'width': '32%',
                                'padding': '12px',
                                'margin': '5px 1%',
                                'border': 'none',
                                'borderRadius': '6px',
                                'backgroundColor': COLORS['success'],
                                'color': 'white',
                                'fontWeight': 'bold',
                                'cursor': 'pointer',
                                'fontSize': '14px',
                                'transition': 'all 0.3s'
                            }
                        ),
                        html.Button(
                            '⏸️ Pause',
                            id='pause-button',
                            n_clicks=0,
                            style={
                                'width': '32%',
                                'padding': '12px',
                                'margin': '5px 1%',
                                'border': 'none',
                                'borderRadius': '6px',
                                'backgroundColor': COLORS['warning'],
                                'color': 'white',
                                'fontWeight': 'bold',
                                'cursor': 'pointer',
                                'fontSize': '14px',
                                'transition': 'all 0.3s'
                            }
                        ),
                        html.Button(
                            '🔄 Reset',
                            id='reset-button',
                            n_clicks=0,
                            style={
                                'width': '32%',
                                'padding': '12px',
                                'margin': '5px 1%',
                                'border': 'none',
                                'borderRadius': '6px',
                                'backgroundColor': COLORS['danger'],
                                'color': 'white',
                                'fontWeight': 'bold',
                                'cursor': 'pointer',
                                'fontSize': '14px',
                                'transition': 'all 0.3s'
                            }
                        )
                    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '1.5rem'}),
                    
                    # Statistics
                    html.Div([
                        html.Div([
                            html.Div('📊 Comparisons', style={'fontSize': '12px', 'color': '#7f8c8d', 'marginBottom': '0.3rem'}),
                            html.Div(id='comparisons-stat', style={'fontSize': '24px', 'fontWeight': 'bold', 'color': COLORS['secondary']}, children='0')
                        ], style={'flex': '1', 'padding': '0.8rem', 'backgroundColor': COLORS['light'], 'borderRadius': '6px', 'margin': '0 0.3rem'}),
                        html.Div([
                            html.Div('🔄 Swaps', style={'fontSize': '12px', 'color': '#7f8c8d', 'marginBottom': '0.3rem'}),
                            html.Div(id='swaps-stat', style={'fontSize': '24px', 'fontWeight': 'bold', 'color': COLORS['danger']}, children='0')
                        ], style={'flex': '1', 'padding': '0.8rem', 'backgroundColor': COLORS['light'], 'borderRadius': '6px', 'margin': '0 0.3rem'}),
                        html.Div([
                            html.Div('📈 Steps', style={'fontSize': '12px', 'color': '#7f8c8d', 'marginBottom': '0.3rem'}),
                            html.Div(id='steps-stat', style={'fontSize': '24px', 'fontWeight': 'bold', 'color': COLORS['success']}, children='0')
                        ], style={'flex': '1', 'padding': '0.8rem', 'backgroundColor': COLORS['light'], 'borderRadius': '6px', 'margin': '0 0.3rem'})
                    ], style={'display': 'flex', 'justifyContent': 'space-between'})
                    
                ], style={
                    'backgroundColor': 'white',
                    'padding': '1.5rem',
                    'borderRadius': '8px',
                    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'
                })
            ], style={'width': '28%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '2%'}),
            
            # Right Panel - Visualization
            html.Div([
                html.Div([
                    html.H3(id='chart-title', style={'textAlign': 'center', 'marginBottom': '1rem', 'color': COLORS['primary']}),
                    
                    dcc.Graph(
                        id='sorting-chart',
                        style={'height': '500px'},
                        config={'responsive': True, 'displayModeBar': True}
                    ),
                    
                    # Playback Controls
                    html.Div([
                        html.Div([
                            html.Label("Playback:", style={'fontWeight': 'bold', 'marginRight': '1rem'}),
                            dcc.Slider(
                                id='playback-slider',
                                min=0,
                                max=100,
                                step=1,
                                value=0,
                                marks={0: '0%', 25: '25%', 50: '50%', 75: '75%', 100: '100%'},
                                tooltip={"placement": "bottom", "always_visible": False}
                            )
                        ], style={'marginBottom': '1rem'}),
                        html.Div(id='step-info', style={'textAlign': 'center', 'fontSize': '14px', 'color': '#7f8c8d', 'fontWeight': 'bold'})
                    ], style={'marginTop': '1.5rem'})
                    
                ], style={
                    'backgroundColor': 'white',
                    'padding': '1.5rem',
                    'borderRadius': '8px',
                    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'
                })
            ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        
    ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 2rem 2rem 2rem'}),
    
    dcc.Interval(id='animation-interval', interval=50, disabled=False)
], style={
    'backgroundColor': '#f8f9fa',
    'minHeight': '100vh',
    'fontFamily': 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
    'margin': '0',
    'padding': '0'
})


# ----------------------
# Callbacks
# ----------------------

@callback(
    Output('visualizer-store', 'data'),
    Output('comparisons-stat', 'children'),
    Output('swaps-stat', 'children'),
    Output('steps-stat', 'children'),
    Input('start-button', 'n_clicks'),
    Input('reset-button', 'n_clicks'),
    Input('array-size-slider', 'value'),
    Input('algorithm-dropdown', 'value'),
    State('array-input', 'value'),
    State('visualizer-store', 'data'),
    prevent_initial_call=False
)
def update_sorting(start_clicks, reset_clicks, size, algorithm, array_input, store_data):
    # Priority: User input first, then random generation
    try:
        if array_input and array_input.strip() and array_input != '64, 34, 25, 12, 22, 11, 90, 88, 45, 50':
            # User has entered custom data
            array = [int(x.strip()) for x in array_input.split(',')]
            array = array[:100]
        else:
            # Use random array based on slider size
            array = np.random.randint(10, 100, size=size).tolist()
    except (ValueError, AttributeError):
        # If parsing fails, generate random array
        array = np.random.randint(10, 100, size=size).tolist()
    
    viz = SortingVisualizer(array)
    
    algorithms = {
        'bubble': viz.bubble_sort,
        'selection': viz.selection_sort,
        'insertion': viz.insertion_sort,
        'merge': viz.merge_sort,
        'heap': viz.heap_sort,
        'quick': viz.quick_sort
    }
    
    steps = algorithms.get(algorithm, viz.bubble_sort)()
    
    store_data = {
        'steps': steps,
        'comparisons': viz.comparisons,
        'swaps': viz.swaps,
        'current_step': 0
    }
    
    return store_data, str(viz.comparisons), str(viz.swaps), str(len(steps))


@callback(
    Output('autoplay-store', 'data'),
    Input('start-button', 'n_clicks'),
    Input('pause-button', 'n_clicks'),
    Input('reset-button', 'n_clicks'),
    State('autoplay-store', 'data'),
    prevent_initial_call=False
)
def control_autoplay(start_clicks, pause_clicks, reset_clicks, autoplay_data):
    if not autoplay_data:
        autoplay_data = {'playing': False}
    
    if start_clicks and start_clicks > (autoplay_data.get('last_start', 0) or 0):
        autoplay_data['playing'] = True
        autoplay_data['last_start'] = start_clicks
    
    if pause_clicks and pause_clicks > (autoplay_data.get('last_pause', 0) or 0):
        autoplay_data['playing'] = False
        autoplay_data['last_pause'] = pause_clicks
    
    if reset_clicks and reset_clicks > (autoplay_data.get('last_reset', 0) or 0):
        autoplay_data['playing'] = False
        autoplay_data['last_reset'] = reset_clicks
    
    return autoplay_data


@callback(
    Output('playback-slider', 'value'),
    Input('animation-interval', 'n_intervals'),
    Input('reset-button', 'n_clicks'),
    State('playback-slider', 'value'),
    State('playback-slider', 'max'),
    State('autoplay-store', 'data'),
    State('speed-slider', 'value'),
    prevent_initial_call=False,
    allow_duplicate=True
)
def auto_advance_slider(n_intervals, reset_clicks, current_value, max_value, autoplay_data, speed):
    if reset_clicks:
        return 0
    
    if not autoplay_data or not autoplay_data.get('playing', False):
        return current_value
    
    if current_value >= max_value:
        return current_value
    
    speed_factor = (1100 - speed) / 100
    step = max(1, int(speed_factor))
    
    return min(current_value + step, max_value)


@callback(
    Output('sorting-chart', 'figure'),
    Output('chart-title', 'children'),
    Output('step-info', 'children'),
    Output('playback-slider', 'max'),
    Input('playback-slider', 'value'),
    State('visualizer-store', 'data'),
    allow_duplicate=True,
    prevent_initial_call=False
)
def update_chart(step, store_data):
    if not store_data or 'steps' not in store_data or not store_data['steps']:
        fig = go.Figure()
        fig.add_trace(go.Bar(y=[]))
        fig.update_layout(
            title="Click 'Start' to begin sorting",
            height=500,
            xaxis_title='Index',
            yaxis_title='Value',
            margin=dict(l=40, r=40, t=60, b=40)
        )
        return fig, "", "", 100
    
    steps = store_data['steps']
    max_steps = len(steps) - 1
    current_step = min(int(step), max_steps)
    
    step_data = steps[current_step]
    array = step_data['array']
    active = step_data['active']
    sorted_indices = step_data['sorted']
    title = step_data['title']
    
    colors = []
    for i in range(len(array)):
        if i in sorted_indices:
            colors.append(COLORS['success'])
        elif i in active:
            colors.append(COLORS['danger'])
        else:
            colors.append(COLORS['secondary'])
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=array,
        x=list(range(len(array))),
        marker=dict(color=colors, line=dict(width=1, color='white')),
        showlegend=False,
        hovertemplate='<b>Index: %{x}</b><br><b>Value: %{y}</b><extra></extra>',
        text=array,
        textposition='outside'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Index',
        yaxis_title='Value',
        height=500,
        showlegend=False,
        hovermode='x unified',
        margin=dict(l=40, r=40, t=60, b=40),
        plot_bgcolor='#f9fafb',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12)
    )
    
    step_info = f"Step {current_step + 1} of {len(steps)} | Comparisons: {store_data['comparisons']} | Swaps: {store_data['swaps']}"
    
    return fig, title, step_info, max_steps


# ----------------------
# Run App
# ----------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
