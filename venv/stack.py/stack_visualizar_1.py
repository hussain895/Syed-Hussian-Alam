"""Simple Dash app to visualize a stack with Push, Pop, and Peek controls.

Usage:
    python3 app.py

Open http://127.0.0.1:8050 in your browser.
"""

from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash

app = Dash(__name__)

STACK_ITEM_STYLE = {
    "border": "none",
    "padding": "10px 14px",
    "margin": "8px 0",
    "borderRadius": "12px",
    "background": "linear-gradient(180deg,#ff5fa8 0%, #ff3b81 100%)",
    "color": "white",
    "boxShadow": "0 6px 18px rgba(255,59,129,0.18)",
    "width": "180px",
    "height": "44px",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
    "fontWeight": "600",
    "fontSize": "15px",
    "transition": "transform 200ms ease, box-shadow 200ms ease",
}

# --- Page and component styles ---
PAGE_STYLE = {
    "minHeight": "100vh",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
    "background": "radial-gradient(circle at 10% 10%, #fff0f6 0%, #ffeef4 20%, #fff 60%), linear-gradient(180deg,#ffd6ea 0%, #fff3f6 100%)",
    "fontFamily": "Inter, Arial, sans-serif",
    "padding": "32px",
}

CARD_STYLE = {
    "background": "linear-gradient(180deg,#ffffffcc 0%, #fff 100%)",
    "backdropFilter": "blur(6px)",
    "padding": "28px",
    "borderRadius": "16px",
    "boxShadow": "0 12px 40px rgba(0,0,0,0.06)",
    "maxWidth": "980px",
    "width": "100%",
    "display": "flex",
    "gap": "32px",
    "alignItems": "flex-start",
}

CONTROLS_STYLE = {
    "display": "flex",
    "flexDirection": "column",
    "alignItems": "flex-start",
    "gap": "12px",
    "minWidth": "260px",
}

INPUT_STYLE = {"padding": "10px 12px", "borderRadius": "8px", "border": "1px solid #ffd0e6", "width": "220px"}

BUTTON_STYLE = {
    "border": "none",
    "padding": "10px 14px",
    "borderRadius": "10px",
    "fontWeight": "600",
    "cursor": "pointer",
}

PUSH_BTN = {**BUTTON_STYLE, "background": "linear-gradient(180deg,#7b1fff 0%, #ff3b81 100%)", "color": "#fff"}
POP_BTN = {**BUTTON_STYLE, "background": "#fff", "color": "#ff3b81", "border": "1px solid #ffd0e6"}
PEEK_BTN = {**BUTTON_STYLE, "background": "#ffeef4", "color": "#c81b60"}


app.layout = html.Div(
    style=PAGE_STYLE,
    children=[
        html.Div(
            style=CARD_STYLE,
            children=[
                html.Div(
                    style=CONTROLS_STYLE,
                    children=[
                        html.H2("Stack Visualization", style={"margin": 0, "color": "#a40055"}),
                        html.Div(
                            [
                                dcc.Input(id="push-input", type="text", placeholder="Value to push", style=INPUT_STYLE),
                            ],
                        ),
                        html.Div(
                            [
                                html.Button("Push", id="push-btn", n_clicks=0, style=PUSH_BTN),
                                html.Button("Pop", id="pop-btn", n_clicks=0, style={**POP_BTN, "marginLeft": "8px"}),
                                html.Button("Peek", id="peek-btn", n_clicks=0, style={**PEEK_BTN, "marginLeft": "8px"}),
                            ],
                            style={"marginTop": "6px"},
                        ),
                        html.Div(id="message", style={"minHeight": "28px", "color": "#6b0b3a", "fontSize": "14px"}),
                        html.Div("Tip: Type a value and click Push (or press Enter).", style={"color": "#9a294b", "fontSize": "13px"}),
                    ],
                ),

                # Stack area
                html.Div(
                    style={"flex": "1", "display": "flex", "flexDirection": "column", "alignItems": "center"},
                    children=[
                                            # Store holds the stack and animation/action metadata
                                            dcc.Store(id="stack-store", data={"stack": [], "action": "", "popped": None}),
                                            # Interval used to clear animation state after it runs
                                            dcc.Interval(id="anim-clear-interval", interval=700, n_intervals=0, disabled=True),
                        html.Div(id="stack-container", children=[], style={"display": "flex", "gap": "24px", "alignItems": "flex-start"}),
                        html.Div(
                            "Note: The top of the stack is shown at the top of the column.",
                            style={"marginTop": "12px", "color": "#7a445c", "fontSize": "13px"},
                        ),
                    ],
                ),
            ],
        )
    ],
)

# --- CSS for animations ---
ANIM_CSS = """
.stack-tile { transition: transform 200ms ease, box-shadow 200ms ease; }
@keyframes pushIn {
    0% { transform: translateY(-40px) scale(0.88); opacity: 0 }
    60% { transform: translateY(6px) scale(1.02); opacity: 1 }
    100% { transform: translateY(0) scale(1); opacity: 1 }
}
@keyframes popOut {
    0% { transform: translateY(0) rotate(0deg); opacity: 1 }
    100% { transform: translateX(120px) rotate(12deg); opacity: 0 }
}
.push-anim { animation: pushIn 420ms cubic-bezier(.2,.9,.2,1) both; }
.pop-anim { animation: popOut 520ms cubic-bezier(.2,.9,.2,1) both; }
"""

app.index_string = app.index_string.replace('</head>', f'<style>{ANIM_CSS}</style></head>')


@app.callback(
    Output("stack-store", "data"),
    Output("message", "children"),
    Output("anim-clear-interval", "disabled"),
    Input("push-btn", "n_clicks"),
    Input("pop-btn", "n_clicks"),
    Input("peek-btn", "n_clicks"),
    State("push-input", "value"),
    State("stack-store", "data"),
)
def modify_stack(push_clicks, pop_clicks, peek_clicks, input_value, store):
    """Update the stack in response to Push/Pop/Peek buttons.

    The store is a dict: {"stack": [...], "action": "push|pop|peek|", "popped": <value>}
    """
    if store is None:
        store = {"stack": [], "action": "", "popped": None}

    stack = list(store.get("stack", []))
    ctx = callback_context
    if not ctx.triggered:
        return store, "", True

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Default: no animation interval
    enable_interval = False

    if triggered_id == "push-btn":
        if input_value is None or str(input_value).strip() == "":
            return store, "Enter a value to push.", True
        stack.append(str(input_value))
        store = {"stack": stack, "action": "push", "popped": None}
        enable_interval = True
        return store, f"Pushed: {input_value}", not enable_interval

    if triggered_id == "pop-btn":
        if len(stack) == 0:
            return store, "Stack is empty — nothing to pop.", True
        # pop value but keep metadata so we can animate the popped tile
        val = stack.pop()
        store = {"stack": stack, "action": "pop", "popped": val}
        enable_interval = True
        return store, f"Popped: {val}", not enable_interval

    if triggered_id == "peek-btn":
        if len(stack) == 0:
            return store, "Stack is empty — nothing to peek.", True
        return {"stack": stack, "action": "peek", "popped": None}, f"Top: {stack[-1]}", True

    return store, "", True


@app.callback(Output("stack-container", "children"), Input("stack-store", "data"))
def render_stack(store):
    """Render the visual representation of the stack.

    We show a column where the top item is at the top.
    """
    if store is None:
        return [html.Div("(stack is empty)", style={"color": "#999"})]

    stack = store.get("stack", [])
    action = store.get("action", "")
    popped = store.get("popped", None)

    if not stack and action != "pop":
        return [html.Div("(stack is empty)", style={"color": "#999"})]

    items = []
    for idx, val in enumerate(reversed(stack)):
        is_top = idx == 0
        wrapper_styles = dict(STACK_ITEM_STYLE)
        if is_top:
            wrapper_styles.update({"transform": "translateY(-6px)", "boxShadow": "0 10px 28px rgba(255,59,129,0.22)"})
            # if last action was push, animate the top tile
            tile_class = "stack-tile push-anim" if action == "push" else "stack-tile"
        else:
            tile_class = "stack-tile"

        items.append(html.Div(val, style=wrapper_styles, className=tile_class))

    # If a pop just occurred, show an extra animated tile that flies out
    if action == "pop" and popped is not None:
        pop_tile = html.Div(popped, style={**STACK_ITEM_STYLE, "position": "absolute", "top": "-64px"}, className="stack-tile pop-anim")
        # wrap the column to include the floating pop tile
        column = html.Div([html.Div([pop_tile] + items, style={"position": "relative", "display": "flex", "flexDirection": "column", "alignItems": "center"})],)
    else:
        column = html.Div(items, style={"display": "flex", "flexDirection": "column", "alignItems": "center"})

    return [
        html.Div(
            [
                html.Div("Stack", style={"fontWeight": "700", "marginBottom": "12px", "fontSize": "16px"}),
                column,
            ],
            style={"display": "flex", "flexDirection": "column", "alignItems": "center"},
        )
    ]


if __name__ == "__main__":
    # Dash v4 renamed `run_server` to `run`
    app.run(debug=True)
