from dash import Dash, html
import dash_cytoscape as cyto

app = Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-compound',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '600px'},
        stylesheet=[
            {
                'selector': 'node',
                'style': {'content': 'data(label)'}
            },
            {
                'selector': '.killzone',
                'style': {'width': 5}
            },
            {
                'selector': '.points',
                'style': {'line-style': 'dashed'}
            }
        ],
        elements=[
            # Parent Nodes
            {
                'data': {'id': 'asia', 'label': 'Asia Range'}
            },
            {
                'data': {'id': 'londono', 'label': 'London Open'}
            },
            {
                'data': {'id': 'newyork', 'label': 'New York Open'}
            },
            {
                'data': {'id': 'londonc', 'label': 'London Close'}
            },

            # Children Nodes
            {
                'data': {'id': 'asia_open', 'label': 'Asia Open', 'parent': 'asia'},
                'position': {'x': 100, 'y': 100}
            },
            {
                'data': {'id': 'asia_close', 'label': 'Asia Close', 'parent': 'asia'},
                'position': {'x': 500, 'y': 100}
            },
            {
                'data': {'id': 'asia_high', 'label': 'Asia High', 'parent': 'asia'},
                'position': {'x': 300, 'y': 300}
            },
            {
                'data': {'id': 'asia_low', 'label': 'Asia low', 'parent': 'asia'},
                'position': {'x': 300, 'y': 0}
            },

            # Edges
            {
                'data': {'source': 'asia_open', 'target': 'asia_close'},
                'classes': 'killzone'
            }
        ]
    )
])

if __name__ == '__main__':
    app.run(debug=True)