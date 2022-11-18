import threading
import dash
import plotly
import plotly.graph_objs as go
import time
from dash import  dcc, html, Input, Output

X = []
Y = []


def fun():
    while True:
        gmt = time.gmtime(time.time())
        time.sleep(5)
        X.append(gmt.tm_min)
        Y.append(gmt.tm_sec)
        # print(X, Y)


threading.Thread(target=fun).start()
app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id='live-graph',
                  animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1000,
            n_intervals=0
        )
    ]

)


@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    data = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode='lines+markers'
    )

    return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                yaxis=dict(range=[min(Y), max(Y)]), )}


if __name__ == '__main__':
    app.run_server()
