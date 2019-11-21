#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2019 Gold Sun Tech Intelligent Technology(Zhejiang) Co., Ltd.
  All Rights Reserved
  Name: main.py
  Purpose:
  Created By:    Clive Lau <clivelau@gst-tech.top>
  Created Date:  2019-11-14
  Changelog:
  Date         Desc
  2019-11-14   Created by Clive Lau
"""

# Builtin libraries
import json
import time
# Third-party libraries
from flask import Flask, jsonify, request
from flask_cors import CORS
# Customized libraries
from suite_parser import ProjectTestSuite


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

project = ProjectTestSuite("B15C.xml")


@app.route('/testsuite', methods=['GET'])
def get_suite():
    response_object = dict()
    response_object['status'] = 'success'
    if request.method == 'GET':
        response_object['project'] = project.get_project()
        response_object['caseidx'] = project.get_case_idx()
        print('caseidx/status:', project.get_case_idx(), project.get_suite()[project.get_case_idx()].get('status'))
        response_object['suite'] = project.get_suite()
    return jsonify(response_object)


@app.route('/testcase/start', methods=['POST'])
def start_case():
    response_object = dict()
    response_object['status'] = 'success'
    if request.method == 'POST':
        # post_data = request.get_json()
        project.start()
    return jsonify(response_object)


@app.route('/testcase/stop', methods=['POST'])
def stop_case():
    response_object = dict()
    response_object['status'] = 'success'
    if request.method == 'POST':
        # post_data = request.get_json()
        project.stop()
    return jsonify(response_object)


@app.route('/testcase/report', methods=['POST'])
def generate_report():
    response_object = dict()
    response_object['status'] = 'success'
    if request.method == 'POST':
        # post_data = request.get_json()
        project.get_report()
    return jsonify(response_object)


def main():
    app.run()


if __name__ == '__main__':
    main()
