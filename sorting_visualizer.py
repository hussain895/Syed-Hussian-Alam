# Sorting Algorithm Visualizer
# Web-based interactive visualizer for sorting algorithms using Dash and Plotly

import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import numpy as np
from collections import deque

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
        """Record a step in the sorting process"""
        self.steps.append({
            'array': array.copy(),
            'active': active_indices or [],
            'sorted': sorted_indices or [],
            'title': title
        })
    
    def bubble_sort(self):
        """Bubble Sort - O(n²)"""
        self.reset()
        n = len(self.array)
        
        for i in range(n):
            swapped = False
            for j in range(0, n-i-1):
                self.comparisons += 1
                self.record_step(self.array, active_indices=[j, j+1], 
                               sorted_indices=list(range(n-i, n)),
                               title=f"Comparing {self.array[j]} and {self.array[j+1]}")
                
                if self.array[j] > self.array[j+1]:
                    self.array[j], self.array[j+1] = self.array[j+1], self.array[j]
                    self.swaps += 1
                    self.record_step(self.array, active_indices=[j, j+1],
                                   sorted_indices=list(range(n-i, n)),
                                   title=f"Swapped {self.array[j+1]} and {self.array[j]}")
                    swapped = True
            
            if not swapped:
                break
        
        self.record_step(self.array, sorted_indices=list(range(n)), 
                       title="Sorting Complete!")
        return self.steps
    
    def selection_sort(self):
        """Selection Sort - O(n²)"""
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
                               title=f"Comparing {self.array[min_idx]} and {self.array[j]}")
                
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
            
            if min_idx != i:
                self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
                self.swaps += 1
                self.record_step(self.array, active_indices=[i, min_idx],
                               sorted_indices=list(range(i+1)),
                               title=f"Swapped {self.array[min_idx]} to position {i}")
        
        self.record_step(self.array, sorted_indices=list(range(n)), 
                       title="Sorting Complete!")
        return self.steps
    
    def insertion_sort(self):
        """Insertion Sort - O(n²)"""
        self.reset()
        n = len(self.array)
        
        for i in range(1, n):
            key = self.array[i]
            j = i - 1
            
            self.record_step(self.array, active_indices=[i], 
                           sorted_indices=list(range(i)),
                           title=f"Inserting {key}")
            
            while j >= 0 and self.array[j] > key:
                self.comparisons += 1
                self.record_step(self.array, active_indices=[j, j+1],
                               sorted_indices=list(range(i)),
                               title=f"Comparing {self.array[j]} and {key}")
                
                self.array[j+1] = self.array[j]
                self.swaps += 1
                j -= 1
                
                self.record_step(self.array, active_indices=[j+1],
                               sorted_indices=list(range(i+1)),
                               title=f"Shifting elements")
            
            self.array[j+1] = key
            self.record_step(self.array, sorted_indices=list(range(i+1)),
                           title=f"Placed {key}")
        
        self.record_step(self.array, sorted_indices=list(range(n)), 
                       title="Sorting Complete!")
        return self.steps
    
    def merge_sort_helper(self, arr, left, right, sorted_indices):
        """Helper function for merge sort"""
        if left >= right:
            return arr
        
        mid = (left + right) // 2
        
        # Sort left half
        self.merge_sort_helper(arr, left, mid, sorted_indices)
        
        # Sort right half
        self.merge_sort_helper(arr, mid+1, right, sorted_indices)
        
        # Merge
        self.merge(arr, left, mid, right, sorted_indices)
        
        return arr
    
    def merge(self, arr, left, mid, right, sorted_indices):
        """Merge function for merge sort"""
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
        
        self.record_step(self.array, sorted_indices=sorted_indices,
                       title=f"Merged segment [{left}:{right}]")
    
    def merge_sort(self):
        """Merge Sort - O(n log n)"""
        self.reset()
        n = len(self.array)
        self.merge_sort_helper(self.array, 0, n-1, list(range(n)))
        self.record_step(self.array, sorted_indices=list(range(n)), 
                       title="Sorting Complete!")
        return self.steps
    
    def heapify(self, n, i, sorted_indices):
        """Heapify function for heap sort"""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n:
            self.comparisons += 1
            self.record_step(self.array, active_indices=[largest, left],
                           sorted_indices=sorted_indices,
                           title=f"Comparing {self.array[largest]} and {self.array[left]}")
            if self.array[left] > self.array[largest]:
                largest = left
        
        if right < n:
            self.comparisons += 1
            self.record_step(self.array, active_indices=[largest, right],
                           sorted_indices=sorted_indices,
                           title=f"Comparing {self.array[largest]} and {self.array[right]}")
            if self.array[right] > self.array[largest]:
                largest = right
        
        if largest != i:
            self.array[i], self.array[largest] = self.array[largest], self.array[i]
            self.swaps += 1
            self.record_step(self.array, active_indices=[i, largest],
                           sorted_indices=sorted_indices,
                           title=f"Swapped {self.array[largest]} and {self.array[i]}")
            self.heapify(n, largest, sorted_indices)
    
    def heap_sort(self):
        """Heap Sort - O(n log n)"""
        self.reset()
        n = len(self.array)
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(n, i, [])
        
        # Extract elements from heap
        for i in range(n - 1, 0, -1):
            self.array[0], self.array[i] = self.array[i], self.array[0]
            self.swaps += 1
            self.record_step(self.array, active_indices=[0, i],
                           sorted_indices=list(range(i+1, n)),
                           title=f"Moving {self.array[i]} to sorted position")
            self.heapify(i, 0, list(range(i+1, n)))
        
        self.record_step(self.array, sorted_indices=list(range(n)), 
                       title="Sorting Complete!")
        return self.steps
    
    def partition(self, low, high, sorted_indices):
        """Partition function for quick sort"""
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
                               title=f"Swapped {self.array[j]} and {self.array[i]}")
        
        self.array[i+1], self.array[high] = self.array[high], self.array[i+1]
        self.swaps += 1
        self.record_step(self.array, active_indices=[i+1, high],
                       sorted_indices=sorted_indices,
                       title=f"Pivot {pivot} placed at position {i+1}")
        
        return i + 1
    
    def quick_sort_helper(self, low, high, sorted_indices):
        """Helper function for quick sort"""
        if low < high:
            pi = self.partition(low, high, sorted_indices)
            self.quick_sort_helper(low, pi - 1, sorted_indices)
            self.quick_sort_helper(pi + 1, high, sorted_indices)
    
    def quick_sort(self):
        """Quick Sort - O(n log n) average"""
        self.reset()
        n = len(self.array)
        self.quick_sort_helper(0, n - 1, [])
        self.record_step(self.array, sorted_indices=list(range(n)), 
                       title="Sorting Complete!")
        return self.steps


# ----------------------
# Dash App Setup
# ----------------------

app = dash.Dash(__name__)
app.title = "Sorting Algorithm Visualizer"

# ----------------------
# Styles
# ----------------------

container_style = {
    'backgroundColor': '#f5f5f5',
    'padding': '2rem',
    'fontFamily': 'Arial, sans-serif',
    'minHeight': '100vh'
}

header_style = {
    'textAlign': 'center',
    'color': '#2c3e50',
    'marginBottom': '2rem'
}

control_panel_style = {
    'backgroundColor': 'white',
    'padding': '1.5rem',
    'borderRadius': '8px',
    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
    'marginBottom': '2rem'
}

button_style = {
    'padding': '10px 20px',
    'margin': '5px',
    'border': 'none',
    'borderRadius': '4px',
    'cursor': 'pointer',
    'fontSize': '14px',
    'fontWeight': 'bold',
    'backgroundColor': '#3498db',
    'color': 'white',
    'transition': 'background-color 0.3s'
}

button_start_style = {**button_style, 'backgroundColor': '#27ae60'}
button_reset_style = {**button_style, 'backgroundColor': '#e74c3c'}

stats_style = {
    'display': 'flex',
    'justifyContent': 'space-around',
    'marginTop': '1rem',
    'padding': '1rem',
    'backgroundColor': '#ecf0f1',
    'borderRadius': '4px'
}

stat_item_style = {
    'textAlign': 'center',
    'fontSize': '14px'
}

stat_value_style = {
    'fontSize': '24px',
    'fontWeight': 'bold',
    'color': '#2c3e50'
}

# ----------------------
# Layout
# ----------------------

app.layout = html.Div([
    dcc.Store(id='visualizer-store', data={}),
    dcc.Store(id='autoplay-store', data={'playing': False}),
    
    html.Div([
        html.H1("🎨 Sorting Algorithm Visualizer", style=header_style),
        html.P("Interactive visualization of different sorting algorithms", 
               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '16px'}),
        
        # Control Panel
        html.Div([
            html.H3("Controls", style={'marginBottom': '1rem'}),
            
            html.Div([
                html.Label("Enter Array (comma-separated numbers):", style={'fontWeight': 'bold', 'marginBottom': '0.5rem', 'display': 'block'}),
                dcc.Input(
                    id='array-input',
                    type='text',
                    placeholder='e.g., 64, 34, 25, 12, 22, 11, 90',
                    value='64, 34, 25, 12, 22, 11, 90, 88, 45, 50',
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'fontSize': '14px',
                        'borderRadius': '4px',
                        'border': '1px solid #bdc3c7',
                        'boxSizing': 'border-box',
                        'marginBottom': '0.5rem'
                    }
                ),
                html.P("(Or use the slider below to generate random data)", 
                       style={'fontSize': '12px', 'color': '#7f8c8d', 'marginTop': '0.5rem'})
            ], style={'marginBottom': '1.5rem'}),
            
            html.Div([
                html.Label("Generate Random Array:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
                dcc.Slider(
                    id='array-size-slider',
                    min=5,
                    max=100,
                    step=5,
                    value=30,
                    marks={i: str(i) for i in range(5, 101, 10)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.P("(Adjust slider to generate random array with this size)", 
                       style={'fontSize': '12px', 'color': '#7f8c8d', 'marginTop': '0.5rem'})
            ], style={'marginBottom': '1.5rem'}),
            
            html.Div([
                html.Label("Algorithm:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
                dcc.Dropdown(
                    id='algorithm-dropdown',
                    options=[
                        {'label': '🫧 Bubble Sort', 'value': 'bubble'},
                        {'label': '📍 Selection Sort', 'value': 'selection'},
                        {'label': '📥 Insertion Sort', 'value': 'insertion'},
                        {'label': '🔀 Merge Sort', 'value': 'merge'},
                        {'label': '📚 Heap Sort', 'value': 'heap'},
                        {'label': '⚡ Quick Sort', 'value': 'quick'}
                    ],
                    value='bubble',
                    style={'width': '100%'}
                )
            ], style={'marginBottom': '1.5rem'}),
            
            html.Div([
                html.Label("Speed:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
                dcc.Slider(
                    id='speed-slider',
                    min=10,
                    max=1000,
                    step=50,
                    value=100,
                    marks={10: 'Fast', 500: 'Medium', 1000: 'Slow'},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], style={'marginBottom': '1.5rem'}),
            
            html.Div([
                html.Button('Start Sorting', id='start-button', style=button_start_style),
                html.Button('Pause', id='pause-button', style={**button_style, 'backgroundColor': '#f39c12'}),
                html.Button('Reset', id='reset-button', style=button_reset_style),
            ], style={'textAlign': 'center'}),
            
            # Statistics
            html.Div([
                html.Div([
                    html.Div('Comparisons', style=stat_item_style),
                    html.Div(id='comparisons-stat', style=stat_value_style, children='0')
                ]),
                html.Div([
                    html.Div('Swaps', style=stat_item_style),
                    html.Div(id='swaps-stat', style=stat_value_style, children='0')
                ]),
                html.Div([
                    html.Div('Steps', style=stat_item_style),
                    html.Div(id='steps-stat', style=stat_value_style, children='0')
                ]),
            ], style=stats_style)
            
        ], style=control_panel_style),
        
        # Visualization
        html.Div([
            html.H3(id='chart-title', style={'textAlign': 'center', 'marginBottom': '1rem'}),
            dcc.Graph(id='sorting-chart', style={'height': '600px'}),
            
            html.Div([
                html.Label("Playback:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
                dcc.Slider(
                    id='playback-slider',
                    min=0,
                    max=100,
                    step=1,
                    value=0,
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
                html.P(id='step-info', style={'textAlign': 'center', 'marginTop': '0.5rem', 'color': '#7f8c8d'})
            ], style={'marginTop': '1.5rem'}),
            
        ], style={'backgroundColor': 'white', 'padding': '1.5rem', 'borderRadius': '8px', 
                 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'})
        
    ], style=container_style),
    
    dcc.Interval(id='animation-interval', interval=50, disabled=False)
], style={'margin': '0', 'padding': '0'})


# ----------------------
# Callbacks
# ----------------------

@callback(
    Output('visualizer-store', 'data'),
    Output('comparisons-stat', 'children'),
    Output('swaps-stat', 'children'),
    Input('start-button', 'n_clicks'),
    Input('reset-button', 'n_clicks'),
    Input('array-size-slider', 'value'),
    Input('algorithm-dropdown', 'value'),
    State('array-input', 'value'),
    State('visualizer-store', 'data'),
    prevent_initial_call=False
)
def update_sorting(start_clicks, reset_clicks, size, algorithm, array_input, store_data):
    # Parse user input or generate random array
    try:
        if array_input and array_input.strip():
            # Parse comma-separated input
            array = [int(x.strip()) for x in array_input.split(',')]
            array = array[:100]  # Limit to 100 elements
        else:
            # Generate random array if input is empty
            array = np.random.randint(10, 100, size=size).tolist()
    except (ValueError, AttributeError):
        # If parsing fails, show error and generate random array
        array = np.random.randint(10, 100, size=size).tolist()
    
    viz = SortingVisualizer(array)
    
    if algorithm == 'bubble':
        steps = viz.bubble_sort()
    elif algorithm == 'selection':
        steps = viz.selection_sort()
    elif algorithm == 'insertion':
        steps = viz.insertion_sort()
    elif algorithm == 'merge':
        steps = viz.merge_sort()
    elif algorithm == 'heap':
        steps = viz.heap_sort()
    elif algorithm == 'quick':
        steps = viz.quick_sort()
    
    store_data = {
        'steps': steps,
        'comparisons': viz.comparisons,
        'swaps': viz.swaps,
        'current_step': 0
    }
    
    return store_data, str(viz.comparisons), str(viz.swaps)


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
    
    # Start button - enable autoplay
    if start_clicks and start_clicks > (autoplay_data.get('last_start', 0) or 0):
        autoplay_data['playing'] = True
        autoplay_data['last_start'] = start_clicks
    
    # Pause button - disable autoplay
    if pause_clicks and pause_clicks > (autoplay_data.get('last_pause', 0) or 0):
        autoplay_data['playing'] = False
        autoplay_data['last_pause'] = pause_clicks
    
    # Reset button - disable autoplay and reset
    if reset_clicks and reset_clicks > (autoplay_data.get('last_reset', 0) or 0):
        autoplay_data['playing'] = False
        autoplay_data['last_reset'] = reset_clicks
    
    return autoplay_data


@callback(
    Output('playback-slider', 'value'),
    Input('animation-interval', 'n_intervals'),
    State('playback-slider', 'value'),
    State('playback-slider', 'max'),
    State('autoplay-store', 'data'),
    State('speed-slider', 'value'),
)
def auto_advance_slider(n_intervals, current_value, max_value, autoplay_data, speed):
    if not autoplay_data or not autoplay_data.get('playing', False):
        return current_value
    
    if current_value >= max_value:
        return current_value  # Stop at end
    
    # Calculate step size based on speed (inverse: higher speed = smaller interval)
    speed_factor = (1100 - speed) / 100  # Range from 0.1 to 10
    step = max(1, int(speed_factor))
    
    return min(current_value + step, max_value)


@callback(
    Output('playback-slider', 'value'),
    Output('sorting-chart', 'figure'),
    Output('chart-title', 'children'),
    Output('step-info', 'children'),
    Output('playback-slider', 'max'),
    Input('playback-slider', 'value'),
    Input('reset-button', 'n_clicks'),
    State('visualizer-store', 'data'),
    prevent_initial_call=False
)
def update_chart(step, reset_clicks, store_data):
    # Check if reset was clicked
    if reset_clicks:
        step = 0
    
    if not store_data or 'steps' not in store_data or not store_data['steps']:
        fig = go.Figure()
        fig.add_trace(go.Bar(y=[]))
        fig.update_layout(title="Click 'Start Sorting' to begin", height=500)
        return 0, fig, "", "", 100
    
    steps = store_data['steps']
    max_steps = len(steps) - 1
    current_step = min(int(step), max_steps)
    
    step_data = steps[current_step]
    array = step_data['array']
    active = step_data['active']
    sorted_indices = step_data['sorted']
    title = step_data['title']
    
    # Create color array
    colors = []
    for i in range(len(array)):
        if i in sorted_indices:
            colors.append('#27ae60')  # Green for sorted
        elif i in active:
            colors.append('#e74c3c')  # Red for active
        else:
            colors.append('#3498db')  # Blue for normal
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=array,
        marker=dict(color=colors),
        showlegend=False,
        hovertemplate='<b>Value: %{y}</b><extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Index',
        yaxis_title='Value',
        height=500,
        showlegend=False,
        hovermode='x unified',
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    step_info = f"Step {current_step + 1} of {len(steps)}"
    
    return current_step, fig, title, step_info, max_steps


# ----------------------
# Run App
# ----------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
