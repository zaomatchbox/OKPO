from flask import Flask, request, render_template
from .src.mccabe import run_ast, run_viz
import json

app = Flask(__name__)


@app.route('/')
def home():
    context = {
        'graph': {},
        'mccabe': 0,
        'code': '',
        'code_graph': '',
    }
    return render_template('index.html', **context)


@app.route('/mccabe', methods=['POST'])
def mccabe():
    code = request.form['source']
    graph = run_viz(code)
    code_graph = run_ast(code)
    context = {
        'graph': json.dumps(graph.serialize()),
        'mccabe': graph.get_mccabe(),
        'code': code,
        'code_graph': code_graph,
    }
    return render_template('index.html', **context)
