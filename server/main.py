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


@app.route('/testsuite', methods=['GET', 'POST'])
def get_suite():
    response_object = dict()
    response_object['status'] = 'success'
    if request.method == 'POST':
        # post_data = request.get_json()
        print("request.method == POST")
        project.update_case(1, 'status', 'inprocess')
    else:
        response_object['project'] = project.get_project()
        response_object['suite'] = project.get_suite()
    return jsonify(response_object)


def main():
    app.run()


if __name__ == '__main__':
    main()
