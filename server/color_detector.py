# -*- coding:utf-8 -*-

"""
  Copyright (C) 2019 Gold Sun Tech Intelligent Technology (Zhejiang) Co., Ltd.
  All Rights Reserved

  Name: color_detector.py
  Purpose:

  Created By:    Clive Lau <clivelau@gst-tech.top>
  Created Date:  2019-11-19

  Changelog:
  Date         Desc
  2019-11-19   Created by Clive Lau
"""

# Builtin libraries

# Third-party libraries
import cv2
import numpy as np

# Custom libraries


# LOWER_BLACK = [0, 0, 0]
# UPPER_BLACK = [180, 255, 46]
# LOWER_GRAY = [0, 0, 46]
# UPPER_GRAY = [180, 434, 255]
# LOWER_WHITE = [0, 0, 221]
# UPPER_WHITE = [180, 30, 255]
# LOWER_RED = [156, 43, 46]
# UPPER_RED = [180, 255, 255]
# LOWER_ORANGE = [11, 43, 46]
# UPPER_ORANGE = [25, 255, 255]
# LOWER_YELLOW = [26, 43, 46]
# UPPER_YELLOW = [34, 255, 255]
# LOWER_GREEN = [35, 43, 46]
# UPPER_GREEN = [77, 255, 255]
# LOWER_CYAN = [78, 43, 46]
# UPPER_CYAN = [88, 255, 255]
# LOWER_BLUE = [100, 43, 46]
# UPPER_BLUE = [124, 255, 255]
# LOWER_PURPLE = [125, 43, 46]
# UPPER_PURPLE = [155, 255, 255]


class ColorDetector(object):
    def __init__(self, camera_idx=0):
        self.camera_idx = camera_idx
        self.capture = None
        # self.hsv_dict = {
        #     'black': (HSV.LOWER_BLACK, HSV.UPPER_BLACK),
        #     'gray': (HSV.LOWER_GRAY, HSV.UPPER_GRAY),
        #     'white': (HSV.LOWER_WHITE, HSV.UPPER_WHITE),
        #     'red': (HSV.LOWER_RED, HSV.UPPER_RED),
        #     'orange': (HSV.LOWER_ORANGE, HSV.UPPER_ORANGE),
        #     'yellow': (HSV.LOWER_YELLOW, HSV.UPPER_YELLOW),
        #     'green': (HSV.LOWER_GREEN, HSV.UPPER_GREEN),
        #     'cyan': (HSV.LOWER_CYAN, HSV.UPPER_CYAN),
        #     'blue': (HSV.LOWER_BLUE, HSV.UPPER_BLUE),
        #     'purple': (HSV.LOWER_PURPLE, HSV.UPPER_PURPLE),
        # }
        pass

    def _snap_shot(self):
        # 过滤前50帧图像
        skip_frame = 50
        # 实例化VideoCapture
        self.capture = cv2.VideoCapture(self.camera_idx)
        # NTSC 720*480/29.97fps
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        while self.capture.isOpened() and skip_frame > 0:
            ret, frame = self.capture.read()
            skip_frame -= 1
        self.capture.release()
        return frame[0:370, 285:720]

    def _cal_ratio_white_pixels(self, img):
        while_pixels = 0
        # 获取图像信息
        (width, height) = img.shape
        for row in range(height):
            for col in range(width):
                pixel = img[col, row]
                if pixel == 255:
                    while_pixels += 1
        return while_pixels / (width * height)

    def _separate_color(self, img, hsv_lower, hsv_upper):
        # 色彩空间转换为HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # hsv_range = self.hsv_dict[color]
        # print(type(hsv_range[0]))
        # if hsv_range is not None:
        mask = cv2.inRange(hsv, lowerb=np.array(hsv_lower), upperb=np.array(hsv_upper))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        closing = cv2.erode(closing, None, iterations=4)
        closing = cv2.dilate(closing, None, iterations=4)
        return closing

    def get_label(self):
        ratio_list = []
        ratio_dict = {
            0: 'White',
            1: 'Red',
            2: 'Green',
            3: 'Blue',
        }
        frame = self._snap_shot()
        white_frame = self._separate_color(frame, [0, 0, 221], [180, 30, 255])
        white_ratio = self._cal_ratio_white_pixels(white_frame)
        ratio_list.append(white_ratio)
        red_frame = self._separate_color(frame, [156, 43, 46], [180, 255, 255])
        red_ratio = self._cal_ratio_white_pixels(red_frame)
        ratio_list.append(red_ratio)
        green_frame = self._separate_color(frame, [35, 43, 46], [77, 255, 255])
        green_ratio = self._cal_ratio_white_pixels(green_frame)
        ratio_list.append(green_ratio)
        blue_frame = self._separate_color(frame, [100, 43, 46], [124, 255, 255])
        blue_ratio = self._cal_ratio_white_pixels(blue_frame)
        ratio_list.append(blue_ratio)
        # cv2.imshow('Origin', frame)
        # cv2.imshow('White', white_frame)
        # cv2.imshow('Red', red_frame)
        # cv2.imshow('Green', green_frame)
        # cv2.imshow('Blue', blue_frame)
        # cv2.waitKey(0)
        return ratio_dict.get(ratio_list.index(max(ratio_list)))


if __name__ == '__main__':
    color = ColorDetector()
    print(color.get_label())
    pass
