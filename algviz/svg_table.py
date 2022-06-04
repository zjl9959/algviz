#!/usr/bin/env python3

"""Define low-level SVG animation refresh related classes for table.

This module was used by vector and table module.
Please don't use this module unless you want to create new data classes
for algviz and knows exactly the meaning of this module.

Author: zjl9959@gmail.com

License: GPLv3

"""

from xml.dom.minidom import Document
from algviz.utility import add_desc_into_svg, add_default_text_style, rgbcolor2str, text_font_size 
from algviz.utility import auto_text_color, find_tag_by_id, str2rgbcolor, clamp
from algviz.utility import add_animate_move_into_node, add_animate_appear_into_node, clear_svg_animates


class SvgTable():
    def __init__(self, width, height):
        """Create an XML object to represent SVG table.
        
        Args:
            width (float): The width of svg table.
            heigt (float): The height of svg table.
        """
        self._dom = Document()
        self._cur_id = 0
        self._svg = self._dom.createElement('svg')
        self._svg.setAttribute('width', '{:.0f}pt'.format(width))
        self._svg.setAttribute('height', '{:.0f}pt'.format(height))
        self._svg.setAttribute('viewBox', '0.00 0.00 {:.2f} {:.2f}'.format(width, height))
        self._svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
        self._dom.appendChild(self._svg)
        add_desc_into_svg(self._dom)
        add_default_text_style(self._dom)


    def update_svg_size(self, width, height):
        """Update the width and height of this svg table.
        
        Args:
            width (float): The width of svg table.
            heigt (float): The height of svg table.
        """
        self._svg.setAttribute('width', '{:.0f}pt'.format(width))
        self._svg.setAttribute('height', '{:.0f}pt'.format(height))
        self._svg.setAttribute('viewBox', '0.00 0.00 {:.2f} {:.2f}'.format(width, height))
        

    def add_rect_element(self, rect, text=None, fill=(255,255,255), stroke=(123,123,123), angle=True):
        """Add a new rectangle element into this SvgTable.
        
        Args:
            rect ((x, y, w, h)): The left bottom corner position(x,y) and width height of this new rectangle.
                eg:(0.0, 50.0, 100.0, 50.0).
            text (str): The text string to be displayed in this rectangle.
            fill ((R,G,B)): Rectangle's background color. R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
            stroke ((R,G,B)): Rectangle's stroke color. (R, G, B) type is the same as fill parameter.
            angle (bool): The shape of this new rectangle's corner.
                True for round corner; False for sharp corner.
        
        Returns:
            int: Unique ID number for the new added rect element in this SvgTable.
        """
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
        r.setAttribute('fill', rgbcolor2str(fill))
        r.setAttribute('stroke', rgbcolor2str(stroke))
        g.appendChild(r)
        if text is not None:
            t = self._dom.createElement('text')
            t.setAttribute('class', 'txt')
            t.setAttribute('x', '{:.2f}'.format(rect[0]+rect[2]*0.5))
            t.setAttribute('y', '{:.2f}'.format(rect[1]+rect[3]*0.5))
            txt_font_size = min(rect[3]-1, text_font_size(rect[2], '{}'.format(text)))
            t.setAttribute('font-size', '{:.2f}'.format(txt_font_size))
            t.setAttribute('fill', auto_text_color(fill))
            tt = self._dom.createTextNode('{}'.format(text))
            t.appendChild(tt)
            g.appendChild(t)
        return int(gid)
    

    def add_text_element(self, pos, text, font_size=16, fill=(123,123,123)):
        """Add a new text element into this SvgTable.
        
        Args:
            pos ((x,y)): The left bottom corner position(x,y), x and y are both float number.
            text (str): The text string.
            font_size (int): Text font size.
            fill ((R,G,B)): Stroke color of this text element. R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 0, 0)
        
        Returns:
            int: Unique ID number for the new added text element in this SvgTable.
        """
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
        t.setAttribute('fill', rgbcolor2str(fill))
        tt = self._dom.createTextNode('{}'.format(text))
        t.appendChild(tt)
        g.appendChild(t)
        return int(gid)
    

    def update_text_element(self, gid, pos=None, text=None, font_size=None, fill=None):
        """Update the text element's position and text string/font/color in this SvgTable.
        
        Args:
            gid (int): The unique ID of the rectangle to be updated.
            pos ((x,y)): The left bottom corner position(x,y), x and y are both float number.
            text (str): The text string.
            font_size (int): Text font size.
            fill ((R,G,B)): Stroke color of this text element. R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 0, 0)
        """
        g = find_tag_by_id(self._svg, 'g', str(gid))
        if g is None:
            return
        t = g.getElementsByTagName('text')
        if len(t) == 0:
            return
        txt = t[0]
        if pos != None:
            txt.setAttribute('x', '{:.2f}'.format(pos[0]))
            txt.setAttribute('y', '{:.2f}'.format(pos[1]))
        if text != None:
            for t_child in txt.childNodes:
                txt.removeChild(t_child)
            tt = self._dom.createTextNode('{}'.format(text))
            txt.appendChild(tt)
        if font_size != None:
            txt.setAttribute('font-size', '{:.2f}'.format(font_size))
        if fill != None:
            txt.setAttribute('fill', rgbcolor2str(fill))


    def update_rect_element(self, gid, rect=None, text=None, fill=None, stroke=None, opacity=None):
        """Update the color, text, fill, stroke and opacity attribute of specific rectangle element.
        
        Args:
            gid (int): The unique ID of the rectangle to be updated.
            rect ((x, y, w, h) or None): New position and size for this rectangle. (x, y) is rectangle's left bottom corner. Keep old position and size if rect is None.
            text (str or None): The text string to be displayed in this rectangle.
            fill ((R,G,B) or None): New background color for this rectangle. Keep old background color if fill is None.
            stroke ((R,G,B) or None): New stroke color for this rectangle. Keep old stroke color if stroke is None.
            opacity (float or None): New opacity arrtibute for this rectangle. Keep old opacity if opacity is None.
        """
        g = find_tag_by_id(self._svg, 'g', str(gid))
        if g is None:
            return
        rects = g.getElementsByTagName('rect')
        if len(rects) == 0:
            return
        r = rects[0]
        t = g.getElementsByTagName('text')
        if opacity is not None:
            g.setAttribute('style', 'opacity:{:.0f}'.format(opacity))
        if fill is not None:
            r.setAttribute('fill', rgbcolor2str(fill))
            if len(t):
                t[0].setAttribute('fill', auto_text_color(fill))
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
                new_font = text_font_size(rect[2], '{}'.format(t[0].firstChild.nodeValue))
                t[0].setAttribute('font-size', '{:.2f}'.format(min(new_font, rect[3]-1)))
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
            fc = str2rgbcolor(r.getAttribute('fill'))
            t.setAttribute('class', 'txt')
            t.setAttribute('x', '{:.2f}'.format(rx+width*0.5))
            t.setAttribute('y', '{:.2f}'.format(ry+height*0.5))
            txt_font_size = text_font_size(width, '{}'.format(text))
            txt_font_size = min(height-1, txt_font_size)
            t.setAttribute('font-size', '{:.2f}'.format(txt_font_size))
            t.setAttribute('fill', auto_text_color(fc))
            for t_child in t.childNodes:
                t.removeChild(t_child)
            tt = self._dom.createTextNode('{}'.format(text))
            t.appendChild(tt)
        if stroke is not None:
            r.setAttribute('stroke', rgbcolor2str(stroke))
    

    def delete_element(self, gid):
        """Delete specific element from this SvgTable.
        
        Args:
            gid (int): The unique ID of the element to be deleted.
        """
        g = find_tag_by_id(self._svg, 'g', str(gid))
        if g is not None:
            self._svg.removeChild(g)
    

    def add_animate_move(self, gid, move, time, bessel=True):
        """Add move animation for specific element.
        
        Args:
            gid (int): The unique ID of the element to add animation.
            move (tuple(float, float)): (delt_x, delt_y) The delt move distance along x axis and y axis for this element.
            time (tuple(float, float)): (begin, end) The begin and end time of this animation.
            bessel (bool): Whether to set the path of this move animation as bezier curve.
        """
        g = find_tag_by_id(self._svg, 'g', str(gid))
        if g is not None:
            animate = self._dom.createElement('animateMotion')
            add_animate_move_into_node(g, animate, move, time, bessel)
    

    def add_animate_appear(self, gid, time, appear=True):
        """Add appear animate for specific element.
        
        Args:
            gid (int): The unique ID of the element to add animation.
            time ((begin, end)): The begin and end time of this animation.
            appear (bool): True for appear animation; False for disappear animation.
        """
        g = find_tag_by_id(self._svg, 'g', str(gid))
        if g is not None:
            animate = self._dom.createElement('animate')
            add_animate_appear_into_node(g, animate, time, appear)


    def add_cursor_element(self, cursor, color=(123,123,123), name=None, dir='U'):
        """Add a cursor into SVG table.
        
        A cursor is an arrow to indicate the current index of rect element.
        It will be displayed in the SVG and you need to choose the proper position to put it.

        Args:
            cursor (float, float, float, float, float): The x, y, offset, width, height of the arrow in cursor.
                x, y is the arrow's top point position, relative to the SVG's top left point.
                Offset is the x offset of the arrow relative to x position.
                width, height is the total width and height of cursor, including arrow and name.
            color: ((int, int, int)): The (Red, Green, Blue) stroke color of the cursor's arrow and name.
            name (str): The name to be displayed close to the arrow.
            dir (str): The direction of the arrow (U:up; D:down; L:left; R:right).

        Returns:
            int: Unique ID number for the new added cursor element in this SvgTable.
        """
        gid = str(self._cur_id)
        self._cur_id += 1
        g = self._dom.createElement('g')
        g.setAttribute('id', gid)
        self._svg.appendChild(g)
        # Create the arrow "^" node of the cursor.
        arrow_width = clamp(cursor[2]*0.2, 4, 10)*0.5
        arrow_top_x = cursor[0] + cursor[2]
        arrow_top_y = cursor[1]
        arrow_left_x = arrow_top_x - arrow_width
        arrow_left_y = arrow_top_y + arrow_width
        arrow_right_x = arrow_top_x + arrow_width
        arrow_right_y = arrow_top_y + arrow_width
        if dir == 'D':
            arrow_left_x = arrow_top_x - arrow_width
            arrow_left_y = arrow_top_y - arrow_width
            arrow_right_x = arrow_top_x + arrow_width
            arrow_right_y = arrow_top_y - arrow_width
        elif dir == 'L':
            arrow_top_x = cursor[0]
            arrow_top_y = cursor[1] + cursor[2]
            arrow_left_x = arrow_top_x + arrow_width
            arrow_left_y = arrow_top_y + arrow_width
            arrow_right_x = arrow_top_x + arrow_width
            arrow_right_y = arrow_top_y - arrow_width
        elif dir == 'R':
            arrow_top_x = cursor[0]
            arrow_top_y = cursor[1] + cursor[2]
            arrow_left_x = arrow_top_x - arrow_width
            arrow_left_y = arrow_top_y - arrow_width
            arrow_right_x = arrow_top_x - arrow_width
            arrow_right_y = arrow_top_y + arrow_width
        arrow_points = '{:.2f},{:.2f} {:.2f},{:.2f} {:.2f},{:.2f}'.format(
            arrow_left_x, arrow_left_y,     # Left point of the arrow.
            arrow_top_x, arrow_top_y,       # Top point of the arrow.
            arrow_right_x, arrow_right_y    # Right point of the arrow.
        )
        svg_arrow = self._dom.createElement('polyline')
        svg_arrow.setAttribute('points', arrow_points)
        svg_arrow.setAttribute('fill', 'none')
        svg_arrow.setAttribute('stroke', rgbcolor2str(color))
        g.appendChild(svg_arrow)
        # Create the text name node.
        txt_font_size = text_font_size(cursor[3], '{}'.format(name))
        txt_font_size = min(14, txt_font_size)
        if name is not None and txt_font_size < cursor[4]:
            t = self._dom.createElement('text')
            t.setAttribute('class', 'txt')
            txt_pos_x, txt_pos_y = cursor[0], cursor[1] + cursor[4] - txt_font_size*0.5
            if dir == 'D':
                txt_pos_y = cursor[1] - cursor[4] + txt_font_size*0.5
            elif dir == 'L':
                txt_pos_x = cursor[0] + cursor[4] - txt_font_size*0.5
                txt_pos_y = cursor[1]
                t.setAttribute('transform', 'rotate(-90, {}, {})'.format(txt_pos_x, txt_pos_y))
            elif dir == 'R':
                txt_pos_x = cursor[0] - cursor[4] + txt_font_size*0.5
                txt_pos_y = cursor[1]
                t.setAttribute('transform', 'rotate(-90, {}, {})'.format(txt_pos_x, txt_pos_y))
            t.setAttribute('x', '{:.2f}'.format(txt_pos_x))
            t.setAttribute('y', '{:.2f}'.format(txt_pos_y))
            t.setAttribute('font-size', '{:.2f}'.format(txt_font_size))
            t.setAttribute('fill', rgbcolor2str(color))
            tt = self._dom.createTextNode('{}'.format(name))
            t.appendChild(tt)
            g.appendChild(t)
        # Create the tail line node of the cursor's arrow.
        svg_line = self._dom.createElement('line')
        svg_line.setAttribute('x1', '{:.2f}'.format(arrow_top_x))
        svg_line.setAttribute('y1', '{:.2f}'.format(arrow_top_y))
        svg_line.setAttribute('stroke', rgbcolor2str(color))
        line_x2, line_y2 = arrow_top_x, max(arrow_top_y + cursor[4] - txt_font_size * 1.1, arrow_top_y)
        if dir == 'D':
            line_y2 = min(arrow_top_y - cursor[4] + txt_font_size*1.1, arrow_top_y)
        elif dir == 'L':
            line_x2 = max(arrow_top_x + cursor[4] - txt_font_size*1.1, arrow_top_x)
            line_y2 = arrow_top_y
        elif dir == 'R':
            line_x2 = min(arrow_top_x - cursor[4] + txt_font_size*1.1, arrow_top_x)
            line_y2 = arrow_top_y
        svg_line.setAttribute('x2', '{:.2f}'.format(line_x2))
        svg_line.setAttribute('y2', '{:.2f}'.format(line_y2))
        g.appendChild(svg_line)
        return int(gid)


    def update_cursor_element(self, gid, new_pos):
        """Update the cursor's position.

        Args:
            gid (int): The unique ID of the cursor to be updated.
            new_pos (delt_x:float, delt_y:float): New position of the cursor's arrow top, relative to cursor's old position.
        """
        g = find_tag_by_id(self._svg, 'g', str(gid))
        if g is None:
            return
        # Update cursor arrow polyine's position.
        arrows = g.getElementsByTagName('polyline')
        for svg_arrow in arrows:
            arrow_points = svg_arrow.getAttribute('points')
            new_arrow_points = ''
            for points in arrow_points.split(' '):
                (point_x, point_y) = points.split(',')
                new_arrow_points += '{:.2f},{:.2f} '.format(
                    float(point_x)+new_pos[0], float(point_y)+new_pos[1])
            svg_arrow.setAttribute('points', new_arrow_points.strip(' '))
        # Update cursor text's position.
        txts = g.getElementsByTagName('text')
        for t in txts:
            if t.hasAttribute('transform'):
                text_pos_x = float(t.getAttribute('x')) - new_pos[1]
                text_pos_y = float(t.getAttribute('y')) + new_pos[0]
            else:
                text_pos_x = float(t.getAttribute('x')) + new_pos[0]
                text_pos_y = float(t.getAttribute('y')) + new_pos[1]
            t.setAttribute('x', '{:.2f}'.format(text_pos_x))
            t.setAttribute('y', '{:.2f}'.format(text_pos_y))
        # Update cursor tail line's position.
        lines = g.getElementsByTagName('line')
        for svg_line in lines:
            line_x1  = float(svg_line.getAttribute('x1')) + new_pos[0]
            line_y1  = float(svg_line.getAttribute('y1')) + new_pos[1]
            line_x2  = float(svg_line.getAttribute('x2')) + new_pos[0]
            line_y2  = float(svg_line.getAttribute('y2')) + new_pos[1]
            svg_line.setAttribute('x1', '{:.2f}'.format(line_x1))
            svg_line.setAttribute('y1', '{:.2f}'.format(line_y1))
            svg_line.setAttribute('x2', '{:.2f}'.format(line_x2))
            svg_line.setAttribute('y2', '{:.2f}'.format(line_y2))


    def clear_animates(self):
        """Clear all the animations in this SvgTable.
        """
        clear_svg_animates(self._svg)
    

    def _repr_svg_(self):
        """Internal function for jupyter notebook display refresh.
        """
        return self._dom.toxml()
