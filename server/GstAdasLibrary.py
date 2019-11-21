# -*- coding: utf-8 -*-

"""
  Copyright (C) 2019 Gold Sun Tech Intelligent Technology (Zhejiang) Co., Ltd.
  All Rights Reserved

  Name: GstLibrary.py
  Purpose:

  Created By:    Clive Lau <clivelau@gst-tech.top>
  Created Date:  2019-11-19

  Changelog:
  Date         Desc
  2019-11-19   Created by Clive Lau
"""

# Builtin libraries
from time import sleep

# Third-party libraries
# from robot.api import logger
import usb1

# Custom libraries
from color_detector import ColorDetector
from USB2XXX.CommCAN import USB2CAN


def isReadyMcuBoardCard(case):
    """ 检测MCU控制板卡是否就绪

    :param case: 输入测试用例实例

    :return: True if ready or not
    """
    is_existed = False
    if case is None:
        return False
    with usb1.USBContext() as context:
        for device in context.getDeviceIterator(skip_on_error=True):
            if (device.getVendorID() == int('0x0483', base=16)) and (device.getProductID() == int('0x7918', base=16)):
                is_existed = True
    case['value'] = 'True' if is_existed else 'False'
    return is_existed


def isReadyCvbsBoardCard(case):
    """ 检测CVBS采集板卡是否就绪

    :param case: 输入测试用例实例

    :return: True if ready or not
    """
    is_existed = False
    if case is None:
        return False
    with usb1.USBContext() as context:
        for device in context.getDeviceIterator(skip_on_error=True):
            if (device.getVendorID() == int('0x0483', base=16)) and (device.getProductID() == int('0x7918', base=16)):
                is_existed = True
    case['value'] = 'True' if is_existed else 'False'
    return is_existed


def isNormalMachineCurrent(case):
    """ 检测整机电流是否处于正常范围

    :param case: 输入测试用例实例

    :return: True if ready or not
    """
    if case is None:
        return False
    # TODO: 通过可编程电源获取整机电流值
    case['value'] = '0.49'
    # 比较整机电流值是否在最小值与最大值范围
    if (case.get('min') is not None) and (case.get('max') is not None):
        if (float(case.get('value')) > float(case.get('min'))) and (float(case.get('value')) < float(case.get('max'))):
            return True
    return False


def isNormalFrontCameraVoltage(case):
    """ 检测前视摄像头电压是否处于正常范围

    :param case: 输入测试用例实例

    :return: True if ready or not
    """
    if case is None:
        return False
    # TODO: 通过ADC获取摄像头电压值
    case['value'] = '5.1'
    # 比较摄像头电压值是否在最小值与最大值范围
    if (case.get('min') is not None) and (case.get('max') is not None):
        if (float(case.get('value')) > float(case.get('min'))) and (float(case.get('value')) < float(case.get('max'))):
            return True
    return False


def isNormalRearCameraVoltage(case):
    """ 检测后视摄像头电压是否处于正常范围

    :param case: 输入测试用例实例

    :return: True if ready or not
    """
    if case is None:
        return False
    # TODO: 通过ADC获取摄像头电压值
    case['value'] = '4.9'
    # 比较摄像头电压值是否在最小值与最大值范围
    if (case.get('min') is not None) and (case.get('max') is not None):
        if (float(case.get('value')) > float(case.get('min'))) and (float(case.get('value')) < float(case.get('max'))):
            return True
    return False


def isNormalLeftCameraVoltage(case):
    """ 检测左视摄像头电压是否处于正常范围

    :param case: 输入测试用例实例

    :return: True if ready or not
    """
    if case is None:
        return False
    # TODO: 通过ADC获取摄像头电压值
    case['value'] = '4.9'
    # 比较摄像头电压值是否在最小值与最大值范围
    if (case.get('min') is not None) and (case.get('max') is not None):
        if (float(case.get('value')) > float(case.get('min'))) and (float(case.get('value')) < float(case.get('max'))):
            return True
    return False


def isNormalRightCameraVoltage(case):
    """ 检测右视摄像头电压是否处于正常范围

    :param case: 输入测试用例实例

    :return: True if ready or not
    """
    if case is None:
        return False
    # TODO: 通过ADC获取摄像头电压值
    case['value'] = '5.1'
    # 比较摄像头电压值是否在最小值与最大值范围
    if (case.get('min') is not None) and (case.get('max') is not None):
        if (float(case.get('value')) > float(case.get('min'))) and (float(case.get('value')) < float(case.get('max'))):
            return True
    return False


def isCorrectFrontCameraColor(case):
    """ 检测前视摄像头图像颜色是否正确

    :return: color string
    """
    if case is None:
        return False
    # 请求切换前视摄像头
    USB2CAN().write((int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x01)))
    sleep(0.1)
    # 检测前视图像颜色
    case['value'] = ColorDetector().get_label()
    print('<>>>>>>>>>>>>>>>>>>>>>>>>>isCorrectFrontCameraColor>: typical/value:', case.get('typical'), case.get('value'))
    return (case.get('typical') == case.get('value'))


def isCorrectRearCameraColor(case):
    """ 检测后视摄像头图像颜色是否正确

    :return: color string
    """
    if case is None:
        return False
    # 请求切换后视摄像头
    USB2CAN().write((int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x02)))
    sleep(0.1)
    # 检测后视图像颜色
    case['value'] = ColorDetector().get_label()
    print('<>>>>>>>>>>>>>>>>>>>>>>>isCorrectFrontCameraColor>: typical/value:', case.get('typical'), case.get('value'))
    return (case.get('typical') == case.get('value'))


def isCorrectLeftCameraColor(case):
    """ 检测左视摄像头图像颜色是否正确

    :return: color string
    """
    if case is None:
        return False
    # 请求切换左视摄像头
    USB2CAN().write((int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x03)))
    sleep(0.1)
    # 检测左视图像颜色
    case['value'] = ColorDetector().get_label()
    return (case.get('typical') == case.get('value'))


def isCorrectRightCameraColor(case):
    """ 检测右视摄像头图像颜色是否正确

    :return: color string
    """
    if case is None:
        return False
    # 请求切换右视摄像头
    USB2CAN().write((int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x04)))
    sleep(0.1)
    # 检测右视图像颜色
    case['value'] = ColorDetector().get_label()
    return (case.get('typical') == case.get('value'))


if __name__ == '__main__':
    pass
    # 检测MCU控制板卡是否就绪
    print(isReadyMcuBoardCard(None))
    # 检测AV采集板卡是否就绪
    print(isReadyCvbsBoardCard(None))
    # 切换前视摄像头
    print(isCorrectFrontCameraColor(None))
    # 切换后视摄像头
    print(isCorrectRearCameraColor(None))
    # 切换左视摄像头
    print(isCorrectLeftCameraColor(None))
    # 切换右视摄像头
    print(isCorrectRightCameraColor())
