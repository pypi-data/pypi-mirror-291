#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/08/20
# @Author  : zx
# @File    : Drawer.py
# @Version : 1.1.3
# @Explain : 两种方式兼容代码,默认采用freetype-cv2 也可以备选freetype-fy

import copy
import time
import traceback  ## log
import  math
import cv2
import freetype  ## Freetypechinese
import numpy as np
import yaml

Version_num = '1.1.3'  ###版本号


##发布 标记类把下面代码注释掉打开logger打印代码
# from common.utils.loginfo import logger
class logger():
    def info(message):
        print(message)


##  父类标记类   子类两种标记方法
class Drawer(object):
    def __init__(self, font_path='',  Type='py'):
        self.font_path = font_path+'/msyh.ttc'
        self.alg_path = font_path+'/alg_name.yaml'
        self.draw_type = Type  ##py 或者 cv2 两种方式

        logger.info(f'标记类的版本号为:{Version_num}')
        logger.info(f'字体路径:{self.font_path} ')
        logger.info(f'中英对照表路径:{self.alg_path} ')
        logger.info(f'标记类方式:{self.draw_type} ')

        if self.init_font() and self.init_alg() and self.init_colors() and self.init_param():
            self.init_flag = True
        else:
            self.init_flag = False
            logger.info(f'初始化失败！！！！！')
        return

    def init_font(self):
        try:
            if self.draw_type == "cv2":
                self.drawclass = Freetype_cv(self.font_path)
            elif self.draw_type == "py":
                self.drawclass = Freetype_py(self.font_path)
            else:
                return False
        except Exception as e:
            logger.info(traceback.format_exc())
            return False
        return True

    def init_alg(self):
        try:
            with open(self.alg_path, 'r', encoding='utf-8') as f:
                self.alg_name = yaml.safe_load(f.read())
                f.close()
        except Exception as e:
            logger.info(traceback.format_exc())
            return False
        return True

    def init_param(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.bg_color = self.gold  ##标签背景颜色
        self.rect_color = self.green  ##矩形框的颜色
        self.text_color = self.black  ##标签颜色
        self.font_scale = 1  ##缩放系数
        self.linethickness = 1  ##线条粗细
        self.pointr = 1  ##点的半径
        self.draw_param = {
            "text_color": self.text_color,
            "rect_color": self.rect_color,
            "bg_color": self.bg_color,
            "thickness": self.linethickness,
            "font_scale": self.font_scale,
            "rect_flag": True
        }
        return True

    def _update_param(self, position, text):
        self.draw_param = {
            "position": position,
            "text": text,
            "text_color": self.text_color,
            "rect_color": self.rect_color,
            "bg_color": self.bg_color,
            "thickness": self.linethickness,
            "font_scale": self.font_scale,
            "rect_flag": True
        }

    def _init_param(self):

        self.text_color = self.black  ##标签颜色
        self.font = cv2.FONT_HERSHEY_SIMPLEX  ##文本字体
        self.font_scale = 1  ##缩放系数
        self.linethickness = 1  ##线条粗细
        self.pointr = 1  ##点的半径

    def init_colors(self):
        ## 初始化各个颜色类型
        self.red = self.hex2bgr('FF0000')
        self.orange = self.hex2bgr('FF701F')
        self.green = self.hex2bgr('00FF00')
        self.blue = self.hex2bgr('0083d4')
        self.purple = self.hex2bgr('8438FF')
        self.pink = self.hex2bgr('FF95C8')
        self.black = self.hex2bgr('333333')
        self.white = self.hex2bgr('FFFFFF')
        self.yellow = self.hex2bgr('FFFF00')
        self.gold = self.hex2bgr('FFD700')
        self.gray = self.hex2bgr('D3D3D3')
        return True

    ## PIL 十六进制颜色值转换为RGB颜色值
    def hex2rgb(self, hex_color):
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b)

    def hex2bgr(self, hex_color):
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (b, g, r)

    def seg_diff_normalized(self, coords, x_scale, y_scale):
        normalized_coords = list(map(lambda shape: list(
            map(lambda points: list(map(lambda point: [point[0] * x_scale, point[1] * y_scale], points)), shape)),
                                     coords))
        return normalized_coords

    def Resizemessage(self, srcframe, message):
        h, w = srcframe.shape[:2]
        x_scale = w
        y_scale = h

        lResults = message['lResults']
        if lResults['rect']:
            lResults['rect'] = [[x * x_scale, y * y_scale, w * x_scale, h * y_scale, c] for x, y, w, h, c in
                                lResults['rect']]
        if lResults['track']:
            lResults['track'] = [[x * x_scale, y * y_scale, w * x_scale, h * y_scale, n] for x, y, w, h, n in
                                 lResults['track']]
        if lResults['region']:
            for key in lResults['region'].keys():
                lResults['region'][key] = self.seg_diff_normalized(lResults['region'][key], x_scale, y_scale)
        if lResults['line']:
            lResults['line'] = [[x * x_scale, y * y_scale, w * x_scale, h * y_scale] for x, y, w, h in
                                lResults['line']]
        if lResults['point']:
            lResults['point'] = [[x * x_scale, y * y_scale, w * x_scale, h * y_scale, c] for x, y, w, h, c in
                                 lResults['point']]
        message['lResults'] = lResults

        return message

    ### 软件接口函数
    def draw_frame_box(self, srcframe, outmessage):
        t1 = time.time()
        outframe = srcframe
        if not self.init_flag:
            logger.info('初始化失败 ！！！')
            return outframe, False

        try:
            outframe = self.draw_frame_main(srcframe, outmessage)
        except Exception as e:
            logger.info(traceback.format_exc())
            logger.info(f'!!!!!!!!!!!!!!!!!!!!!!!!标记类错误message:{outmessage}')
            return outframe, False

        t2 = time.time()
        costtime = 1000 * (t2 - t1)  ##标记类时间
        # logger.info(f'message={outmessage}')
        if costtime > 5:
            logger.info(f'标记类的时间:{costtime}ms')
        return outframe, True

    def draw_frame_main(self, srcframe, srcmessage):
        dstframe = srcframe
        message = copy.deepcopy(srcmessage)

        ## 数据异常 直接返回
        if message['error']:
            return dstframe

        ## message进行过归一化处理，这里要还原回图像的参数
        message = self.Resizemessage(srcframe, message)

        bState = message['bState']
        ## 报警状态不同标记不同
        if bState:
            self.line_color = self.red
            self.rect_color = self.red
        else:
            self.rect_color = self.green
            self.line_color = self.green

        ## 标记矩形
        if message['lResults']["rect"]:
            dstframe = self.draw_rect(dstframe, message)

        ## 标记跟踪
        if message['lResults']["track"]:
            dstframe = self.draw_track(dstframe, message)

        ## 标记区域
        if message['lResults']["region"]:
            dstframe = self.draw_region(dstframe, message)

        ## 标记线段
        if message['lResults']["line"]:
            dstframe = self.draw_line(dstframe, message)

        ## 标记点
        if message['lResults']["point"]:
            dstframe = self.draw_point(dstframe, message)

        return dstframe

    def draw_rect(self, srcframe, message):

        rects = list(message['lResults']["rect"])
        texts = list(message['lResults']["text"])
        label = '空标记'
        outframe = srcframe

        ## 循环处理所有rects
        for num, target_rect in enumerate(rects):
            iX = int(target_rect[0])
            iY = int(target_rect[1])
            iW = int(target_rect[2])
            iH = int(target_rect[3])
            position = (iX, iY, iX + iW, iY + iH)

            if message["sType"] in ['Digital', 'Pointer', 'Valve']:
                label = texts[num][0]  ##标签
                self.font_scale = 3 * self.font_scale  ##字体大小
            elif message["sType"] == "HKIR":
                label = str(int(texts[num][0])) + '_' + str(int(texts[num][1]))  ##标签
                self.font_scale = 3 * self.font_scale  ##字体大小
            elif message["sType"] == "DialLoc":
                label = self.alg_name[texts[num][0].split('_')[0]] + self.alg_name[texts[num][0].split('_')[1]]
                self.font_scale = 3 * self.font_scale  ##字体大小
            elif message["sType"] in ['LPR', 'HLPR']:
                self.font_scale = 1.5 * self.font_scale  ##字体大小
                label = texts[num][0]
            elif message["sType"] in ['CarJudge']:
                label = texts[num][0]
                try:
                    label = self.alg_name[label]
                except Exception as e:
                    label = label
            elif message["sType"] in ['FaceRec'] and texts:
                label = texts[num][0]
                self.font_scale = 2 * self.font_scale  ##字体大小
            elif message["sType"] == "PersonandFace":

                name = 'person'
                try:
                    label = self.alg_name[name]
                except Exception as e:
                    label = name

            elif message["sType"] == "ArcFace":
                self.font_scale = 1.5 * self.font_scale  ##字体大小
                label = texts[num][0]
            elif message["sType"] == 'WorkWear':
                self.rect_color = self.purple
                label = '工装'
            elif message["sType"] in ["SmogFire", "PersonCar", "IRPersonCar", "Sand", "Door", 'FireHydrant', "EQ",
                                      "Car", 'DoorWindow', 'MeterBox', 'ChemicalDrip', 'Hat', 'Pothole', 'XJPersonCar',
                                      'Facelocal', 'LPRlocal', 'SmokeFire', "YoloWorld", "WorldRanging", "RetinaFace",
                                      "MonkeyPerson", "WarningClass"]:
                label = texts[num][0]
                self.font_scale = 1.5 * self.font_scale  ##字体大小
                try:
                    label = self.alg_name[label]
                except Exception as e:
                    label = label

            elif message["sType"] in ['PersonTrack', 'IRPersonTrack', 'CarTrack', 'FaceTrack']:
                ##不标记矩形框
                break

            else:
                label = texts[num][0]
                try:
                    label = self.alg_name[label]
                except Exception as e:
                    label = label

            self._update_param(position, label)
            outframe = self.drawclass.Draw_String(outframe, self.draw_param)
            self._init_param()
        return outframe

    def draw_region(self, srcframe, message):
        outframe = srcframe
        if message['sType'] == 'FireHydrant' or message['sType'] == 'ChemicalDrip' or message[
            'sType'] == 'IndoorFlooding':
            ## 循环region 进行标记
            for key in message['lResults']["region"].keys():
                reg = message['lResults']["region"][key]
                self.linethickness = 2 * self.linethickness
                if len(reg) != 0:
                    reg = [cv2.UMat(np.array(cn).astype("int")) for cn in reg]
                    if key == "seg":
                        if message['sType'] == 'FireHydrant':
                            outframe = cv2.drawContours(image=outframe, contours=reg, contourIdx=-1, color=self.green,
                                                        thickness=self.linethickness)
                        else:
                            outframe = cv2.drawContours(image=outframe, contours=reg, contourIdx=-1, color=self.red,
                                                        thickness=self.linethickness)
                    elif key == "diff":
                        outframe = cv2.drawContours(image=outframe, contours=reg, contourIdx=-1, color=self.blue,
                                                    thickness=self.linethickness)
                    outframe = np.asarray(outframe.get())

            self._init_param()
        return outframe

    def draw_track(self, srcframe, message):
        outframe = srcframe
        tracks = list(message['lResults']["track"])
        texts = list(message['lResults']["text"])

        for num, track_rect in enumerate(tracks):
            iX = int(track_rect[0])
            iY = int(track_rect[1])
            iW = int(track_rect[2])
            iH = int(track_rect[3])
            labelnum = int(track_rect[4])
            position = (iX, iY, iX + iW + 20, iY + iH)
            if message["sType"] == 'PersonandFace':
                label = texts[num][0]

                self._update_param(position, label)
                outframe = self.drawclass.Draw_String(outframe, self.draw_param)
            ##行人跟踪及热成像行人跟踪及车辆跟踪
            if message["sType"] in ['PersonTrack', 'IRPersonTrack', 'CarTrack', 'FaceTrack']:
                label = texts[num][0]
                label = self.alg_name[label]

                self._update_param(position, label)
                outframe = self.drawclass.Draw_String(outframe, self.draw_param)

            if message["sType"] == 'WorkWear':
                if texts[num] == 'warning':
                    color = self.red
                elif texts[num] == 'ok':
                    color = self.green
                else:
                    color = self.yellow
                cv2.rectangle(outframe, position, color, thickness=self.linethickness, lineType=cv2.LINE_AA)

            if message["sType"] not in ['PersonandFace', 'WorkWear', 'ArcFace']:
                cv2.putText(outframe, str(labelnum), (iX + iW, iY+iH), self.font, 0.8*self.font_scale, self.orange,
                             2*self.linethickness)
            self._init_param()
        return outframe

    def draw_line(self, srcframe, message):
        outframe = srcframe
        lines = list(message['lResults']["line"])
        texts = list(message['lResults']["text"])

        for num, target_line in enumerate(lines):
            p1 = (int(target_line[0]), int(target_line[1]))
            p2 = (int(target_line[2]), int(target_line[3]))
            cv2.line(outframe, p1, p2, self.line_color, self.linethickness)
            position = (int(target_line[0]), int(target_line[1]), int(target_line[2]), int(target_line[3]))
            label = texts[num][0]  ##标签
            if message["sType"] == 'Mesh':
                label = self.alg_name[label]
                self._update_param(position, label)
                self.draw_param["rect_flag"] = False
                outframe = self.drawclass.Draw_String(outframe, self.draw_param)

            cv2.line(outframe, p1, p2, self.line_color, 3 * self.linethickness)

            self._init_param()
        return outframe

    def draw_point(self, srcframe, message):
        outframe = srcframe
        points = list(message['lResults']["point"])
        for num, target_point in enumerate(points):
            p1 = (int(target_point[0]), int(target_point[1]))
            p2 = (int(target_point[2]), int(target_point[3]))
            cv2.circle(outframe, (p1, p2), self.pointr, self.red, self.linethickness)

            self._init_param()
        return outframe


###  freetype_py 的方式  只要字体库
class Freetype_py(object):

    def __init__(self, font_path=''):

        self._face = freetype.Face(font_path)
        self.textdiv = 6
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def read_param(self, draw_param):
        self.text_color = draw_param["text_color"]
        self.rect_color = draw_param["rect_color"]
        self.linethickness = draw_param["thickness"]
        self.font_scale = draw_param["font_scale"]
        self.rect_flag = draw_param["rect_flag"]
        self.bg_color = draw_param["bg_color"]

    def Draw_String(self, image, draw_param):

        '''
        draw chinese(or not) text with ttf
        :param image:     image(numpy.ndarray) to draw text
        :param pos:       where to draw text
        :param text:      the context, for chinese should be unicode type
        :param text_size: text size
        :param text_color:text color
        :return:          image
        '''
        self.read_param(draw_param)
        h, w = image.shape[:2]
        position = draw_param["position"]
        text = draw_param["text"]
        p1 = [int(position[0]), int(position[1])]
        p2 = [int(position[2]), int(position[3])]

        ## 画矩形框
        if self.rect_flag:
            cv2.rectangle(image, (p1[0], p1[1]), (p2[0], p2[1]), self.rect_color, thickness=self.linethickness,
                          lineType=cv2.LINE_AA)


        ## 由目标矩形框大小获得 背景框的高度值
        bl = 0.1
        rect_width = int(p2[0] - p1[0])
        rect_height = int(p2[1] - p1[1])
        bg_height = int(bl * rect_height)





        ## 画标签区域 由cv2计算而得到
        (text_width,text_height),text_bottom = \
            cv2.getTextSize(text, self.font, fontScale=self.font_scale, thickness=self.linethickness)  # text width, height

        bg_height=text_height+text_bottom

        if text_height>bg_height:
            bl = text_height / bg_height
            bl = math.ceil(bl)
            bg_height = int(bg_height / bl)



        text_width=text_width/2  ##py方式中文字符是英文计算方式的1/2

        bg_width=rect_width

        if bg_height < 20:
            bg_height = 20

        ## 标签区域大小  P3 P4为标记区域左上和右下的点  p5为labeltext的点
        p3 = [0, 0]
        p4 = [0, 0]
        p5 = [0, 0]
        if p1[1] < bg_height:  # 矩形框内部上
            p3 = [int(p1[0]), p1[1]]
            p4 = [int(p3[0] + bg_width), p3[1]+bg_height]
            p5 = [int(p3[0]+bg_width/2-text_width/2), p3[1]+text_height]
        else:  # 矩形框外面上
            p3 = [int(p1[0]), int(p1[1] - bg_height)]
            p4 = [int(p3[0] + bg_width), p3[1] + bg_height]
            p5 = [int(p3[0]+bg_width/2-text_width/2), p3[1]+text_height]

        ## 背景框不超过矩形框
        if p4[0] > p2[0]:
            p4[0] = p2[0]

        cv2.rectangle(image, (p3[0], p3[1]), (p4[0], p4[1]), self.bg_color, int(-1), cv2.LINE_AA)  ##背景框
        cv2.rectangle(image, (p3[0], p3[1]), (p4[0], p4[1]), self.rect_color, self.linethickness, cv2.LINE_AA)  ##背景的矩形框

        self._face.set_char_size(text_height * 64)
        # metrics = self._face.size
        # ascender = metrics.ascender / 64.0
        # ypos = int(ascender)

        img = self.draw_string(image, p5[0], p5[1], text, self.text_color)

        return img

    def draw_string(self, img, x_pos, y_pos, text, color):
        '''
        draw string
        :param x_pos: text x-postion on img
        :param y_pos: text y-postion on img
        :param text:  text (unicode)
        :param color: text color
        :return:      image
        '''
        prev_char = 0
        pen = freetype.Vector()

        pen.x = x_pos << self.textdiv
        pen.y = y_pos << self.textdiv

        hscale = 1.5
        matrix = freetype.Matrix(int(hscale) * 0x10000, int(0.2 * 0x10000), \
                                 int(0.0 * 0x10000), int(1.1 * 0x10000))
        cur_pen = freetype.Vector()
        pen_translate = freetype.Vector()

        image = copy.deepcopy(img)
        for cur_char in text:
            self._face.set_transform(matrix, pen_translate)

            self._face.load_char(cur_char)
            kerning = self._face.get_kerning(prev_char, cur_char)
            pen.x += kerning.x
            slot = self._face.glyph
            bitmap = slot.bitmap

            cur_pen.x = pen.x
            cur_pen.y = pen.y - slot.bitmap_top * (2 ** self.textdiv)
            self.draw_ft_bitmap(image, bitmap, cur_pen, color)

            pen.x += slot.advance.x
            prev_char = cur_char

        return image

    def draw_ft_bitmap(self, img, bitmap, pen, color):
        '''
        draw each char
        :param bitmap: bitmap
        :param pen:    pen
        :param color:  pen color e.g.(0,0,255) - red
        :return:       image
        '''

        x_pos = pen.x >> self.textdiv
        y_pos = pen.y >> self.textdiv
        cols = bitmap.width
        rows = bitmap.rows

        glyph_pixels = bitmap.buffer
        for row in range(rows):
            for col in range(cols):
                if glyph_pixels[row * cols + col] != 0:
                    if y_pos + row < len(img) and x_pos + col < len(img[0]):
                        img[y_pos + row][x_pos + col][0] = color[0]
                        img[y_pos + row][x_pos + col][1] = color[1]
                        img[y_pos + row][x_pos + col][2] = color[2]
                    else:
                        # logger.info(f' x_pos:{x_pos}  y_pos:{y_pos}  row:{row} col:{col}')
                        pass


###freetype_cv的方式
class Freetype_cv(object):

    def __init__(self, font_path=''):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.puttxt_type = cv2.freetype.createFreeType2()
        self.puttxt_type.loadFontData(font_path, 0)

    def read_param(self, draw_param):
        self.text_color = draw_param["text_color"]
        self.rect_color = draw_param["rect_color"]
        self.linethickness = draw_param["thickness"]
        self.font_scale = draw_param["font_scale"]
        self.rect_flag = draw_param["rect_flag"]
        self.bg_color = draw_param["bg_color"]

    def Draw_String(self, image, draw_param):
        self.read_param(draw_param)
        h, w = image.shape[:2]
        position = draw_param["position"]
        text = draw_param["text"]
        p1 = [int(position[0]), int(position[1])]
        p2 = [int(position[2]), int(position[3])]

        ## 画矩形框
        if self.rect_flag:
            cv2.rectangle(image, (p1[0], p1[1]), (p2[0], p2[1]), self.rect_color, thickness=self.linethickness,
                          lineType=cv2.LINE_AA)

        ## 由目标矩形框大小获得 背景框的高度值
        bl = 0.1
        rect_width = int(p2[0] - p1[0])
        rect_height = int(p2[1] - p1[1])
        bg_height = int(bl * rect_height)

        ## 最小背景高度为20pixel
        if bg_height < 20:
            bg_height = 20

        ## 通过背景高度 确定字符的高度和宽度
        text_size = self.puttxt_type.getTextSize(text, bg_height, self.linethickness)
        text_width = text_size[0][0]
        text_height = text_size[0][1]
        text_bottom = text_size[1]
        bg_width = text_width  ##背景框宽度等于 字符框宽度

        ## 标签区域大小   这里p3为标签左上角 P4为标签右下角 p5为字符起点
        p3 = [0, 0]
        p4 = [0, 0]
        p5 = [0, 0]

        ## 字符框宽度大于矩形框  则中心对称

        if bg_width > rect_width:
            fix_pixel = (bg_width - rect_width) / 2
        else:
            bg_width = rect_width
            fix_pixel = 0  ##修正像素值

        if p1[1] < rect_height:  # 矩形框内部上
            p3 = [int(p1[0] - fix_pixel), int(p1[1])]
            p4 = [p3[0] + bg_width, p3[1] + bg_height]
            p5 = [int(p3[0] + bg_width / 2 - text_width / 2), int(p3[1]-text_bottom)]    ##中文存在特殊的bottom 剪去即可
            # if (p2[1] + text_height) > h:  ##标越界签先放在最上角吧
            #     p3 = [int(p1[0]), 0]
            #     p4 = [int(p1[0] + text_width), text_height]
            #     p5 = [int(p1[0]), p3[1] + text_height]
            # else:  ##标签在最下面
            #     p3 = [int(p1[0]), int(p2[1])]
            #     p4 = [int(p1[0] + text_width), int(p2[1] + text_height)]
            #     p5 = [int(p3[0]), p3[1] + text_height]
        else:  # 矩形框外面上
            p3 = [int(p1[0] - fix_pixel), int(p1[1] - bg_height)]
            p4 = [int(p3[0] + bg_width), p3[1] + bg_height]
            p5 = [int(p3[0] + bg_width / 2 - text_width / 2), int(p3[1]-text_bottom)]

        cv2.rectangle(image, (p3[0], p3[1]), (p4[0], p4[1]), self.bg_color, int(-1), cv2.LINE_AA)  ##背景框填充
        cv2.rectangle(image, (p3[0], p3[1]), (p4[0], p4[1]), self.rect_color, self.linethickness, cv2.LINE_AA)  ##背景的矩形框

        self.puttxt_type.putText(
            img=image,
            text=text,
            org=(p5[0], p5[1]),
            fontHeight=bg_height,
            color=self.text_color,  # Make sure the text color is set correctly
            thickness=-1,  # Use 1 for thickness
            line_type=cv2.LINE_AA,
            bottomLeftOrigin=False  ##原点左上角
        )
        # cv2.imshow("3", image)
        # cv2.waitKey(10)
        return image
