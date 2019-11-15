#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2019 Gold Sun Tech Intelligent Technology(Zhejiang) Co., Ltd.
  All Rights Reserved
  Name: suite_parser.py
  Purpose:
  Created By:    Clive Lau <clivelau@gst-tech.top>
  Created Date:  2019-11-14
  Changelog:
  Date         Desc
  2019-11-14   Created by Clive Lau
"""

# Builtin libraries
# Third-party libraries
from xml.dom.minidom import parse
import xml.dom.minidom
# Customized libraries


class ProjectTestSuite(object):
    """Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, path):
        """Inits SampleClass with blah."""
        self.path = path
        self.project = ''
        self.suite = []
        self._parse()

    def _parse(self):
        """解析xml获取测试用例"""
        # TODO(CliveLau): 合理性检查
        # 清空列表
        self.suite.clear()
        # 使用minidom解析器打开XML文档
        dom_tree = xml.dom.minidom.parse(self.path)
        suite = dom_tree.documentElement
        if suite.hasAttribute("project"):
            self.project = suite.getAttribute("project")
        # 在集合中获取所有测试用例
        cases = suite.getElementsByTagName("case")
        # 打印每个测试用例的详细信息
        for case in cases:
            dict_case = {}
            if case.hasAttribute("title"):
                dict_case['title'] = case.getAttribute("title")
            if len(case.getElementsByTagName('index')):
                dict_case['index'] = case.getElementsByTagName('index')[0].childNodes[0].data
            if len(case.getElementsByTagName('description')):
                dict_case['description'] = case.getElementsByTagName('description')[0].childNodes[0].data
            if len(case.getElementsByTagName('min')):
                dict_case['min'] = case.getElementsByTagName('min')[0].childNodes[0].data
            if len(case.getElementsByTagName('typical')):
                dict_case['typical'] = case.getElementsByTagName('typical')[0].childNodes[0].data
            if len(case.getElementsByTagName('max')):
                dict_case['max'] = case.getElementsByTagName('max')[0].childNodes[0].data
            if len(case.getElementsByTagName('data')):
                li_cmd = []
                for cmd in case.getElementsByTagName('data'):
                    li_cmd.append(cmd.childNodes[0].data)
                dict_case['data'] = li_cmd
            # status: init / inprocess / pass / fail
            dict_case['status'] = "init"
            self.suite.append(dict_case)

    def get_project(self):
        """获取项目名称"""
        return self.project

    def get_suite(self):
        """获取全部测试用例"""
        return self.suite

    def update_case(self, index, attr, value):
        """更新测试用例"""
        self.suite[index - 1][attr] = value


def main():
    import json
    project = ProjectTestSuite("B15C.xml")
    response_object = dict()
    response_object["project"] = project.get_project()
    response_object["suite"] = project.get_suite()
    print(json.dumps(response_object, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
