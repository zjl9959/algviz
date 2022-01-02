#!/usr/bin/env python3

'''
@author:zjl9959@gmail.com
@license:GPLv3
'''


_getElemColor = (0, 255, 127)      # SpringGreen
_setElemColor = (255, 165, 0)      # Orange


class TraceColorStack():
    '''
    @class: Manage multiple colors on an element, perform color fusion operations.
    '''

    def __init__(self, bgcolor=(255, 255, 255)):
        '''
        @param: (bgcolor->(R,G,B)) R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
        '''
        self._colors = list()
        self._bgcolor = bgcolor
    

    def add(self, color):
        '''
        @function: Add a new color into TraceColorStack.
        @param: (color->(R,G,B)) R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
        '''
        if not len(self._colors) or color != self._colors[-1]:
            self._colors.append(color)
    

    def remove(self, color):
        '''
        @function: Remove color from TraceColorStack.
        @param: (color->(R,G,B)) R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
        return: (bool) Return False if can't color. Return True if successfully deleted color.
        '''
        colors_new = list()
        for i in range(len(self._colors)):
            if color != self._colors[i]:
                colors_new.append(self._colors[i])
        res = False
        if len(colors_new) < len(self._colors):
            res = True
        self._colors = colors_new
        return res
    

    def color(self):
        '''
        @function: Get the merged color in TraceColorStack.
        @return: (color->(R,G,B)) R, G, B stand for color channel for red, green, blue.
        '''
        if len(self._colors) == 0:
            return self._bgcolor
        return self._colors[-1]


class ConsecutiveIdMap():
    '''
    @class: Allocate contiguous integer numbers for hashable objects.
    '''

    def __init__(self, offset=0):
        '''
        @param: (offset->int) The initial value of the initial mapping ID.
        '''
        self._offset = offset
        self._next_id = offset
        self._attr2id = dict()
        self._id2attr = list()
    

    def toConsecutiveId(self, attr_id):
        '''
        @function: Create or get the continuous ID for an unordered ID.
        @param: (attr_id->hashable) Unordered ID object.
        @return: (int) Continuous ID value.
        '''
        if attr_id in self._attr2id.keys():
            return self._attr2id[attr_id]
        else:
            self._attr2id[attr_id] = self._next_id
            self._id2attr.append(attr_id)
            self._next_id += 1
            return self._next_id - 1
    

    def toAttributeId(self, cons_id):
        '''
        @function: Given a continuous ID, return it's correspond unordered ID.
        @param: (cons_id->int) Continuous ID value.
        @return: (hashable) Unordered ID object.
        '''
        return self._id2attr[cons_id - self._offset]
    

def find_tag_by_id(node, tag_name, tag_id):
    '''
    @function: Find the first match node in XML node and its sub nodes.
    @param: (node->xmldom.Node) The XML node object to search.
    @param: (tag_name->str) The tag name of the element.
    @param: (tag_id->str) The id value of the element.
    @return: (xmldom.Node or None) Return the XML node object if found it, otherwise return None.
    '''
    tags = node.getElementsByTagName(tag_name)
    for tag in tags:
        if tag.getAttribute('id') == tag_id:
            return tag
    return None


def clear_svg_animates(svg):
    '''
    @function: Clear all the animation effects in SVG.
    @param: (svg->xmldom.Document) The SVG object to be cleared.
    '''
    gg = svg.getElementsByTagName('g')
    for g in gg:
        animates_appear = g.getElementsByTagName('animate')
        if len(animates_appear):
            g.removeAttribute('style')
        animates_move = g.getElementsByTagName('animateMotion')
        for animate in animates_appear + animates_move:
            g.removeChild(animate)


def add_animate_move_into_node(g, animate, move, time, bessel):
    '''
    @param: (g->xmldom.Node) The SVG node to add move animation into.
    @param: (move->tuple(float, float)) (delt_x, delt_y) The delt move distance along x axis and y axis for this element.
    @param: (time->tuple(float, float)) (begin, end) The begin and end time of this animation.
    @param: (bessel->bool) Whether to set the path of this move animation as bezier curve.
    '''
    g.appendChild(animate)
    if bessel:
        animate.setAttribute('path', 'm0,0 q{:.2f},{:.2f} {:.2f},{:.2f}'.format(move[0]*0.5-move[1]*0.2, move[1]*0.5+move[0]*0.2, move[0], move[1]))
    else:
        animate.setAttribute('path', 'm0,0 l{:.2f},{:.2f}'.format(move[0], move[1]))
    animate.setAttribute('begin', '{:.2f}s'.format(time[0]))
    animate.setAttribute('dur', '{:.2f}s'.format(time[1]-time[0]))
    animate.setAttribute('fill', 'freeze')


def add_animate_appear_into_node(g, animate, time, appear=True):
    '''
    @param: (g->xmldom.Node) The SVG node to add appear animation into.
    @param: (time->tuple(float, float)) (begin, end) The begin and end time of this animation.
    @param: (appear->bool) True for appear animation; False for disappear animation.
    '''
    g.setAttribute('style', 'opacity:{:.0f}'.format(not appear))
    g.appendChild(animate)
    animate.setAttribute('attributeName', 'opacity')
    animate.setAttribute('from', '{:.0f}'.format(not appear))
    animate.setAttribute('to', '{:.0f}'.format(appear))
    animate.setAttribute('begin', '{:.2f}s'.format(time[0]))
    animate.setAttribute('dur', '{:.2f}s'.format(time[1]-time[0]))
    animate.setAttribute('fill', 'freeze')


def auto_text_color(back_color):
    '''
    @function: Auto pick one text stroke color according to it's background color.
    @param: (back_color->(R,G,B)) Text background color. R, G, B stand for color channel for red, green, blue.
            R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
    @return: (str) Text stroke color value formatted with hexadecimal number(SVG format).
            eg: '#FFFFFF'
    '''
    rgb_sum = back_color[0]+back_color[1]+back_color[2]
    if rgb_sum < 150:
        return '#FFFFFF'
    else:
        return '#000000'


def rgbcolor2str(color):
    '''
    @function: Convert (R, G, B) formatted color into hexadecimal formatted string.
    @param: (color->(R,G,B)) R, G, B stand for color channel for red, green, blue.
            R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
    @return: (str) Hexadecimal formatted string. (SVG format). eg: '#FFFFFF'
    '''
    return '#{:0>2x}{:0>2x}{:0>2x}'.format(color[0], color[1], color[2])


def str2rgbcolor(color_str):
    '''
    @function: Convert hexadecimal formatted string into (R, G, B) formatted color.
    @param: (color_str->str) Hexadecimal formatted string. (SVG format). eg: '#FFFFFF'
    @return: ((R,G,B)) R, G, B stand for color channel for red, green, blue.
            R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
    '''
    color_str = color_str.strip('#')
    return (int(color_str[0:2], 16), int(color_str[2:4], 16), int(color_str[4:6], 16))


def text_font_size(text_width, text):
    '''
    @function: Calculate the font size based on the total width of the text and the text content.
    @param: (text_width->float) The total width of the text.
    @param: (text->str) The text content (should be unicode format string).
    @return: (float) Text font size.
    '''
    display_len = text_char_num(text)
    if display_len > 0:
        return min(16, text_width*1.6/display_len, text_width*0.8)
    else:
        return 0


def text_char_num(text):
    '''
    @function: Count the number of characters in the text.
    @param: (text->str) The text content (should be unicode format string).
    @return: (int) The number of characters in the text.
    '''
    count = 0
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            count += 2
        else:
            count += 1
    return count
