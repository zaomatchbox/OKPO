from flask import Flask, request, render_template
from .mccabe.src.mccabe import run_ast, run_viz
from .sql_injection.sql1 import search as search1
from .sql_injection.sql2 import search as search2
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/mccabe', methods=['GET', 'POST'])
def mccabe():
    if request.method == 'GET':
        context = {
            'graph': '',
            'mccabe': 0,
            'code': None,
            'code_graph': '',
            'error': '',
        }
    else:
        code = request.form['source']
        error = None
        try:
            graph = run_viz(code)
            code_graph = run_ast(code)
        except Exception as e:
            error = repr(e)
            graph = ''
            code_graph = ''
            raise e
        context = {
            'graph': '' if error is not None else json.dumps(graph.serialize()),
            'mccabe': 0 if error is not None else graph.get_mccabe(),
            'code': code,
            'code_graph': '' if error is not None else code_graph,
            'error': error,
        }
    return render_template('mccabe.html', **context)


@app.route('/sql1', methods=['GET', 'POST'])
def sql_first():
    if request.method == 'GET':
        context = {
            'results': search1(),
        }
    else:
        context = {
            'results': search1(request.form['q'])
        }
    return render_template('sql/1.html', **context)


@app.route('/sql2', methods=['GET', 'POST'])
def sql_second():
    if request.method == 'GET':
        context = {
            'status': False,
        }
    else:
        context = {
            'status': search2(request.form['login'], request.form['password'])
        }
    return render_template('sql/2.html', **context)
