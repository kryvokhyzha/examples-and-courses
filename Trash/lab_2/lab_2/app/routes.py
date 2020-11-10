# -*- coding: utf-8 -*-
import os
import time
import pandas as pd
import numpy as np
import json
import shutil

from app import app
from flask import render_template, send_from_directory
from flask import Flask, flash, request, redirect, url_for

from app.models.LABA_2 import *

from werkzeug.utils import secure_filename

import warnings
warnings.filterwarnings('ignore')

ALLOWED_EXTENSIONS = set(['csv'])

working_path = app.config['WORKING_FOLDER']
upload_path = working_path + 'data/uploads/'
graphic_path = working_path + 'templates/graphics/'
json_path_params = working_path +'data/parameters/js_param.json'
json_path_show_res = working_path +'data/result_data/js_show.json'

def read_json(json_path):
    data = {}
    with open(json_path, "r") as json_file:
        data = json.load(json_file)
    return data

def write_json(json_path, data):
    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent = 4)


def check_path(path):
    os.system("if [ ! -d " + path + " ]; then mkdir -p " + path + "; fi")

def get_name_files(path):
    check_path(path)
    name_files = os.listdir(path)
    return name_files

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        sample_size = request.form['sample_size']
        if not(sample_size):
            sample_size = 45
        else:
            sample_size = int(sample_size)


        vec_size = ['2','2','3','4']
        for i in range(4):
            value = request.form['vec_size_'+str(i+1)]
            if value:
                vec_size[i] = value
            vec_size[i] = int(vec_size[i])

        type_polinom = int(request.form['type_polinom'])

        degrees = ['15','15','15']
        for i in range(3):
            value = request.form['degree_'+str(i+1)]
            if value:
                degrees[i] = value
            degrees[i] = int(degrees[i])

        weights = int(request.form['coef_weight'])

        if request.form.get('find_lambda'):
            lambda_multiblock = 1
        else:
            lambda_multiblock = 0

        method = request.form['method']

        use_default_input = False

        input_path = ''

        if 'file' not in request.files:
            use_default_input = True
        else:
            file = request.files['file']
            if file.filename == '':
                use_default_input = True
            else:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    input_path = 'app/data/uploads/' + filename
                    file.save(os.path.join(upload_path, filename))

        if use_default_input:
            input_path = 'app/data/default_input/input.csv'


        params = dict(poly_type=type_polinom, degrees=degrees,
                  dimensions=vec_size, samples=sample_size, input_file=input_path, output_file='output.txt',
                    weights=weights, lambda_multiblock=lambda_multiblock, method=method)

        write_json(json_path_params, params)

        return redirect(url_for('calculation'))

    return render_template('index.html', title='Main page')

@app.route('/calculation', methods=['GET', 'POST'])
def calculation():

    params = read_json(json_path_params)

    graph_names = get_name_files(graphic_path)
    if len(graph_names) > 0:
        for name in graph_names:
            os.remove(graphic_path + name)

    print('\n\n Attention:')
    print(get_name_files(graphic_path))
    print('yep')

    solver = Solve(params)
    solver.prepare()
    solution = PolynomialBuilder(solver)
    solution.plot_graphs(path='app/templates/graphics/')

    show_res = solver.show_dict()
    write_json(json_path_show_res, show_res)

    res_str = solution.get_results() #solver.show()+'\n\n'+

    text_file = open("app/data/result_data/output.txt", "w")
    text_file.write(res_str)
    text_file.close()

    return redirect(url_for('result'))

@app.route('/result', methods=['GET', 'POST'])
def result():

    text_file = open("app/data/result_data/output.txt", "r")
    lines = text_file.readlines()
    text_file.close()

    show_res = read_json(json_path_show_res)
    headers = list(show_res.keys())

    return render_template('result.html', title='Result', lines=lines, headers=headers, show_res=show_res)

@app.route('/graphic', methods=['GET', 'POST'])
def graphic():

    show_res = read_json(json_path_show_res)
    error = show_res['Error normalised (Y - F)']

    len_graphic_names = len(get_name_files(graphic_path))
    range_index = range(len_graphic_names)

    print(range_index)

    return render_template('graphic.html', title='Graphic', range_index=range_index, error = error)


@app.route('/graph/<num>', methods=['GET', 'POST'])
def graph(num):
    path = 'graphics/graph_' + str(num) +'.html'
    print(path)
    return render_template(path, title='Graphic')


#-----------------------------------------------------
#--------Routes----------------------


#-----------------
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
