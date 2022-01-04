#!/usr/bin/env python3

'''
@author: zjl9959@gmail.com
@license: GPLv3
'''

import xml.dom.minidom as xmldom

from . import utility as util

class SvgTable():
    def __init__(self, width, height):
        '''
        @function: Create an XML object to represent SVG table.
        @param: (width->float) The width of svg table.
        @param: (heigt->float) The height of svg table.
        '''
        self._dom = xmldom.Document()
        self._cur_id = 0
        self._svg = self._dom.createElement('svg')
        self._svg.setAttribute('width', '{:.0f}pt'.format(width))
        self._svg.setAttribute('height', '{:.0f}pt'.format(height))
        self._svg.setAttribute('viewBox', '0.00 0.00 {:.2f} {:.2f}'.format(width, height))
        self._svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
        self._dom.appendChild(self._svg)


    def update_svg_size(self, width, height):
        '''
        @function: Update the width and height of this svg table.
        @param: (width->float) The width of svg table.
        @param: (heigt->float) The height of svg table.
        '''
        self._svg.setAttribute('width', '{:.0f}pt'.format(width))
        self._svg.setAttribute('height', '{:.0f}pt'.format(height))
        self._svg.setAttribute('viewBox', '0.00 0.00 {:.2f} {:.2f}'.format(width, height))
        

    def add_rect_element(self, rect, text=None, fill=(255,255,255), stroke=(123,123,123), angle=True):
        '''
        @function: Add a new rectangle element into this SvgTable.
        @param: (rect->(x, y, w, h)) The left bottom corner position(x,y) and width height of this new rectangle.
                eg:(0.0, 50.0, 100.0, 50.0).
        @param: (text:str) The text string to be displayed in this rectangle.
        @param: (fill->(R,G,B)) Rectangle's background color. R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
        @param: (stroke->(R,G,B)) Rectangle's stroke color. (R, G, B) type is the same as fill parameter.
        @param: (angle->bool) The shape of this new rectangle's corner.
                True for round corner; False for sharp corner.
        @return: (int) Unique ID number for the new added rect element in this SvgTable。
        '''
        gid = str(self._cur_id)
        self._cur_id += 1
        g = self._dom.createElement('g')
        g.setAttribute('id', gid)
        self._svg.appendChild(g)
        r = self._dom.createElement('rect')
        r.setAttribute('x', '{:.2f}'.format(rect[0]))
        r.setAttribute('y', '{:.2f}'.format(rect[1]))
        r.setAttribute('width', '{:.2f}'.format(rect[2]))
        r.setAttribute('height', '{:.2f}'.format(rect[3]))
        if angle is True:
            r.setAttribute('rx', '{:.2f}'.format(min(rect[2], rect[3])*0.1))
            r.setAttribute('ry', '{:.2f}'.format(min(rect[2], rect[3])*0.1))
        r.setAttribute('fill', util.rgbcolor2str(fill))
        r.setAttribute('stroke', util.rgbcolor2str(stroke))
        g.appendChild(r)
        if text is not None:
            t = self._dom.createElement('text')
            t.setAttribute('alignment-baseline', 'middle')
            t.setAttribute('text-anchor', 'middle')
            t.setAttribute('font-family', 'Times,serif')
            t.setAttribute('x', '{:.2f}'.format(rect[0]+rect[2]*0.5))
            t.setAttribute('y', '{:.2f}'.format(rect[1]+rect[3]*0.5))
            t.setAttribute('font-size', '{:.2f}'.format(util.text_font_size(rect[2], '{}'.format(text))))
            t.setAttribute('fill', util.auto_text_color(fill))
            tt = self._dom.createTextNode('{}'.format(text))
            t.appendChild(tt)
            g.appendChild(t)
        return int(gid)
    

    def add_text_element(self, pos, text, font_size=16, fill=(123,123,123)):
        '''
        @function: Add a new text element into this SvgTable.
        @param: (pos->(x,y)) The left bottom corner position(x,y), x and y are both float number.
        @param: (text->str) The text string.
        @param: (font_size->int) Text font size.
        @param: (fill->(R,G,B)) Stroke color of this text element. R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 0, 0)
        @return: (int) Unique ID number for the new added text element in this SvgTable。
        '''
        gid = str(self._cur_id)
        self._cur_id += 1
        g = self._dom.createElement('g')
        g.setAttribute('id', gid)
        self._svg.appendChild(g)
        t = self._dom.createElement('text')
        t.setAttribute('x', '{:.2f}'.format(pos[0]))
        t.setAttribute('y', '{:.2f}'.format(pos[1]))
        t.setAttribute('font-size', '{:.2f}'.format(font_size))
        t.setAttribute('font-family', 'Times,serif')
        t.setAttribute('fill', util.rgbcolor2str(fill))
        tt = self._dom.createTextNode('{}'.format(text))
        t.appendChild(tt)
        g.appendChild(t)
        return int(gid)
    

    def update_rect_element(self, gid, rect=None, text=None, fill=None, stroke=None, opacity=None):
        '''
        @function: Update the color, text, fill, stroke and opacity attribute of specific rectangle element.
        @param: (gid->int) The unique ID of the rectangle to be updated.
        @param: (rect->(x, y, w, h) or None) New position and size for this rectangle. (x, y) is rectangle's left bottom corner. Keep old position and size if rect is None.
        @param: (text->str or None) The text string to be displayed in this rectangle.
        @param: (fill->(R,G,B) or None) New background color for this rectangle. Keep old background color if fill is None.
        @param: (stroke->(R,G,B) or None) New stroke color for this rectangle. Keep old stroke color if stroke is None.
        @param: (opacity->float or None) New opacity arrtibute for this rectangle. Keep old opacity if opacity is None.
        '''
        g = util.find_tag_by_id(self._svg, 'g', str(gid))
        if g is None:
            return
        r = g.getElementsByTagName('rect')[0]
        t = g.getElementsByTagName('text')
        if opacity is not None:
            g.setAttribute('style', 'opacity:{:.0f}'.format(opacity))
        if fill is not None:
            r.setAttribute('fill', util.rgbcolor2str(fill))
            if len(t):
                t[0].setAttribute('fill', util.auto_text_color(fill))
        if rect is not None:
            r.setAttribute('x', '{:.2f}'.format(rect[0]))
            r.setAttribute('y', '{:.2f}'.format(rect[1]))
            r.setAttribute('width', '{:.2f}'.format(rect[2]))
            r.setAttribute('height', '{:.2f}'.format(rect[3]))
            if r.getAttribute('rx') != '':
                r.setAttribute('rx', '{:.2f}'.format(min(rect[2],rect[3])*0.1))
                r.setAttribute('ry', '{:.2f}'.format(min(rect[2],rect[3])*0.1))
            if len(t):
                t[0].setAttribute('x', '{:.2f}'.format(rect[0]+rect[2]*0.5))
                t[0].setAttribute('y', '{:.2f}'.format(rect[1]+rect[3]*0.5))
                new_font = util.text_font_size(rect[2], '{}'.format(t[0].firstChild.nodeValue))
                t[0].setAttribute('font-size', '{:.2f}'.format(new_font))
        if text is not None:
            if len(t) == 0:
                t = self._dom.createElement('text')
                g.appendChild(t)
            else:
                t = t[0]
            rx = float(r.getAttribute('x'))
            ry = float(r.getAttribute('y'))
            width = float(r.getAttribute('width'))
            height = float(r.getAttribute('height'))
            fc = util.str2rgbcolor(r.getAttribute('fill'))
            t.setAttribute('alignment-baseline', 'middle')
            t.setAttribute('text-anchor', 'middle')
            t.setAttribute('font-family', 'Times,serif')
            t.setAttribute('x', '{:.2f}'.format(rx+width*0.5))
            t.setAttribute('y', '{:.2f}'.format(ry+height*0.5))
            t.setAttribute('font-size', '{:.2f}'.format(util.text_font_size(width, '{}'.format(text))))
            t.setAttribute('fill', util.auto_text_color(fc))
            for t_child in t.childNodes:
                t.removeChild(t_child)
            tt = self._dom.createTextNode('{}'.format(text))
            t.appendChild(tt)
        if stroke is not None:
            r.setAttribute('stroke', util.rgbcolor2str(stroke))
    

    def delete_element(self, gid):
        '''
        @function: Delete specific element from this SvgTable.
        @param: (gid->int) The unique ID of the element to be deleted.
        '''
        g = util.find_tag_by_id(self._svg, 'g', str(gid))
        if g is not None:
            self._svg.removeChild(g)
    

    def add_animate_move(self, gid, move, time, bessel=True):
        '''
        @function: Add move animation for specific element.
        @param: (gid->int) The unique ID of the element to add animation.
        @param: (move->tuple(float, float)) (delt_x, delt_y) The delt move distance along x axis and y axis for this element.
        @param: (time->tuple(float, float)) (begin, end) The begin and end time of this animation.
        @param: (bessel->bool) Whether to set the path of this move animation as bezier curve.
        '''
        g = util.find_tag_by_id(self._svg, 'g', str(gid))
        if g is not None:
            animate = self._dom.createElement('animateMotion')
            util.add_animate_move_into_node(g, animate, move, time, bessel)
    

    def add_animate_appear(self, gid, time, appear=True):
        '''
        @function: Add appear animate for specific element.
        @param: (gid->int) The unique ID of the element to add animation.
        @param: (time->(begin, end)) The begin and end time of this animation.
        @param: (appear->bool) True for appear animation; False for disappear animation.
        '''
        g = util.find_tag_by_id(self._svg, 'g', str(gid))
        if g is not None:
            animate = self._dom.createElement('animate')
            util.add_animate_appear_into_node(g, animate, time, appear)
    

    def clear_animates(self):
        '''
        @function: Clear all the animations in this SvgTable.
        '''
        util.clear_svg_animates(self._svg)
    

    def _repr_svg_(self):
        '''
        @function: Internal function for jupyter notebook display refresh.
        '''
        return self._dom.toxml()
