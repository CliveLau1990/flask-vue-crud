# -*- coding: utf-8 -*-

"""
  Copyright (C) 2019 Gold Sun Tech Intelligent Technology (Zhejiang) Co., Ltd.
  All Rights Reserved

  Name: xls_reporter.py
  Purpose:

  Created By:    Clive Lau <clivelau@gst-tech.top>
  Created Date:  2019-11-19

  Changelog:
  Date         Desc
  2019-11-19   Created by Clive Lau
"""

# Builtin libraries
# Third-party libraries
import xlwt
# Custom libraries


class XlsReporter(object):
    def __init__(self):
        pass

    def _set_style(self, name='Times New Roman', height=256, align_horz=0x02, align_vert=0x01, bold=False):
        """设置表格样式"""
        style = xlwt.XFStyle()
        align = xlwt.Alignment()
        # VERT_TOP:    0x00 上端对齐
        # VERT_CENTER: 0x01 居中对齐（垂直方向）
        # VERT_BOTTOM: 0x02 底端对齐
        # HORZ_LEFT:   0x01 左端对齐
        # HORZ_CENTER: 0x02 居中对齐（水平方向）
        # HORZ_RIGHT:  0x03 右端对齐
        align.horz = align_horz
        align.vert = align_vert
        style.alignment = align
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        return style

    def _sheet_header(self, sheet):
        """生成Excel Header"""
        row = ["Test Case", "Description", "Min", "Typical", "Max", "Value", "Result"]
        sheet.write_merge(0, 0, 0, len(row) - 1, "EOL测试信息显示区", self._set_style(bold=True))
        for idx in range(0, len(row)):
            sheet.write(1, idx, row[idx], self._set_style(bold=True))
        return sheet

    def _sheet_content(self, sheet, suite):
        """生成Excel Content"""
        # TODO: 判断suite是否为List
        if suite is None:
            return
        for idx in range(0, len(suite)):
            case = suite[idx]
            sheet.write(idx + 2, 0, case.get('title'), self._set_style(align_horz=0x01))
            sheet.write(idx + 2, 1, case.get('description'), self._set_style(align_horz=0x01))
            sheet.write(idx + 2, 2, case.get('min'), self._set_style())
            sheet.write(idx + 2, 3, case.get('typical'), self._set_style())
            sheet.write(idx + 2, 4, case.get('max'), self._set_style())
            sheet.write(idx + 2, 5, case.get('value'), self._set_style())
            sheet.write(idx + 2, 6, case.get('status'), self._set_style())

    def generate_report(self, name, suite):
        # TODO: 判断name/suite是否为None
        # 新建表格
        xls = xlwt.Workbook()
        # 给表格新建工作薄
        sheet = xls.add_sheet(name, cell_overwrite_ok=True)
        # Excel Header
        self._sheet_header(sheet)
        # Excel Content
        self._sheet_content(sheet, suite)
        # 保存表格
        xls.save(name + '.xls')


if __name__ == '__main__':
    XlsReporter().generate_report("QC8JLCAJAM1911200012T", None)
