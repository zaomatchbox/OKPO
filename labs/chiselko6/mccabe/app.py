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
    error = None
    try:
        graph = run_viz(code)
        code_graph = run_ast(code)
    except Exception as e:
        error = repr(e)
        graph = ''
        code_graph = ''
    context = {
        'graph': '' if error is not None else json.dumps(graph.serialize()),
        'mccabe': 0 if error is not None else graph.get_mccabe(),
        'code': code,
        'code_graph': '' if error is not None else code_graph,
        'error': error,
    }
    return render_template('index.html', **context)
