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
import time
# Third-party libraries
from xml.dom.minidom import parse
import xml.dom.minidom
# Customized libraries
import GstAdasLibrary
from xls_reporter import XlsReporter


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
        self.is_running = False
        self.case_idx = 0
        self.project = ''
        self.suite = []
        self.suite_dict = {
            # MCU控制板卡
            0: GstAdasLibrary.isReadyMcuBoardCard,
            # CVBS采集板卡
            1: GstAdasLibrary.isReadyCvbsBoardCard,
            # 16V整机电流
            2: GstAdasLibrary.isNormalMachineCurrent,
            # 12V整机电流
            3: GstAdasLibrary.isNormalMachineCurrent,
            # 9V整机电流
            4: GstAdasLibrary.isNormalMachineCurrent,
            # 前视摄像头电压
            5: GstAdasLibrary.isNormalFrontCameraVoltage,
            # 后视摄像头电压
            6: GstAdasLibrary.isNormalRearCameraVoltage,
            # 左视摄像头电压
            7: GstAdasLibrary.isNormalLeftCameraVoltage,
            # 右视摄像头电压
            8: GstAdasLibrary.isNormalRightCameraVoltage,
            # 前视摄像头图像
            9: GstAdasLibrary.isCorrectFrontCameraColor,
            # 后视摄像头图像
            10: GstAdasLibrary.isCorrectRearCameraColor,
            # 左视摄像头图像
            11: GstAdasLibrary.isCorrectLeftCameraColor,
            # 右视摄像头图像
            12: GstAdasLibrary.isCorrectRightCameraColor,
            # 硬线开关
            13: GstAdasLibrary.isCorrectButtonSignal,
        }
        self._parse()

    def _parse(self):
        """解析xml获取测试用例"""
        case_cnt = 0
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
            case_cnt += 1
            dict_case = {}
            if case.hasAttribute("title"):
                dict_case['title'] = case.getAttribute("title")
            if len(case.getElementsByTagName('description')):
                dict_case['description'] = case.getElementsByTagName('description')[0].childNodes[0].data
            if len(case.getElementsByTagName('min')):
                dict_case['min'] = case.getElementsByTagName('min')[0].childNodes[0].data
            if len(case.getElementsByTagName('typical')):
                dict_case['typical'] = case.getElementsByTagName('typical')[0].childNodes[0].data
            if len(case.getElementsByTagName('max')):
                dict_case['max'] = case.getElementsByTagName('max')[0].childNodes[0].data
            if len(case.getElementsByTagName('transmit')):
                li_cmd = []
                for cmd in case.getElementsByTagName('transmit'):
                    li_cmd.append(cmd.childNodes[0].data)
                dict_case['transmit'] = li_cmd
            dict_case['index'] = case_cnt
            dict_case['value'] = ""
            # status: init / inprocess / pass / fail
            dict_case['status'] = "init"
            self.suite.append(dict_case)

    def start(self):
        """设置测试用例状态"""
        if self.is_running:
            return
        self.is_running = True
        self.case_idx = 0
        for idx in range(0, len(self.suite)):
            case = self.suite[idx]
            case['value'] = ''
            case['status'] = 'init'

        print('>>>>>>>>>>>>>>>>>>Start>>>>>>>>>>>>>>>>>>>>')

        for idx in range(0, len(self.suite)):
            if not self.is_running:
                break
            self.case_idx = idx
            case = self.suite[idx]
            case['status'] = 'inprocess'
            print('<start>: case_idx:', self.case_idx)
            if self.suite_dict.get(idx) is None:
                case['status'] = 'fail'
                continue
            if self.suite_dict.get(idx)(case):
                case['status'] = 'pass'
            else:
                case['status'] = 'fail'
                break
            

    def stop(self):
        """设置测试用例状态"""
        if not self.is_running:
            return
        self.is_running = False
        self.case_idx = 0
        # 处于InProcess状态，更改状态为Init状态
        for idx in range(0, len(self.suite)):
            case = self.suite[idx]
            if case['status'] == 'inprocess':
                case['status'] = 'init'

    def get_project(self):
        """获取项目名称"""
        return self.project

    def get_suite(self):
        """获取全部测试用例"""
        return self.suite

    def get_case_idx(self):
        """获取当前测试用例的序号"""
        return self.case_idx

    def get_report(self):
        """生成测试报告"""
        XlsReporter().generate_report("CliveLau20191122", self.suite)


def main():
    import json
    project = ProjectTestSuite("B15C.xml")
    response_object = dict()
    response_object["project"] = project.get_project()
    response_object["suite"] = project.get_suite()
    print(json.dumps(response_object, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
