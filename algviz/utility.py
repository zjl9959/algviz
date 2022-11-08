#!/usr/bin/env python3

"""Some utility functions and classes used by other modules.

Author: zjl9959@gmail.com

License: GPLv3

"""

_version = '0.1.7'                  # algviz version
_url = 'https://algviz.com'         # The homepage for algviz
KFATAL_HELP_INFO = """You can report this bug from link: https://github.com/zjl9959/algviz/issues"""


# Define exceptions for algviz runtime.
class AlgvizParamError(Exception):
    def __init__(self, message):
        super().__init__('[AlgvizParamError] {}'.format(message))


class AlgvizRuntimeError(Exception):
    def __init__(self, message):
        super().__init__('[AlgvizRuntimeError] {}\n{}'.format(message, KFATAL_HELP_INFO))


class AlgvizFatalError(Exception):
    def __init__(self, message):
        super().__init__('[AlgvizFatalError] {}\n{}'.format(message, KFATAL_HELP_INFO))


class AlgvizTypeError(Exception):
    def __init__(self, obj):
        super().__init__('[AlgvizTypeError] Type {} not support!\n{}'.format(type(obj), KFATAL_HELP_INFO))


# Parameter limit for display data objects.
kMinAnimDelay = 0.1         # The minimum animation delay time is 0.1 seconds.
kMaxAnimDelay = 100.0       # The maximum animation delay time is 100.0 seconds.
kMinCellWidth = 10.0        # The minimum vector/table cell display width.
kMaxCellWidth = 100.0       # The maximum vector/table cell display width.
kMinCellHeight = 10.0       # The minimum vector/table cell display height.
kMaxCellHeight = 100.0      # The maximum vector/table cell display height.
kMaxBarHight = 1000.0       # The maximum histogram bar height of vector.
kMaxNameChars = 50          # The Maximum name character numbers.


class TraceColorStack():
    """Manage multiple colors on an element, perform color fusion operations.
    """

    def __init__(self, bgcolor=(255, 255, 255)):
        """
        Args:
            bgcolor ((R,G,B)): R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
        """
        self._colors = list()
        self._bgcolor = bgcolor
    

    def add(self, color):
        """Add a new color into TraceColorStack.
        
        Args:
            color ((R,G,B)): R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
        """
        if not len(self._colors) or color != self._colors[-1]:
            self._colors.append(color)
    

    def remove(self, color):
        """Remove color from TraceColorStack.
        
        Args:
            color ((R,G,B)): R, G, B stand for color channel for red, green, blue.
                R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
        
        Returns:
            bool: Return False if can't color. Return True if successfully deleted color.
        """
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
        """Get the merged color in TraceColorStack.
        
        Returns:
            color ((R,G,B)): R, G, B stand for color channel for red, green, blue.
        """
        if len(self._colors) == 0:
            return self._bgcolor
        return self._colors[-1]


class ConsecutiveIdMap():
    """Allocate contiguous integer numbers for hashable objects.
    """

    def __init__(self, offset=0):
        """
        Args:
            offset (int): The initial value of the initial mapping ID.
        """
        self._offset = offset
        self._next_id = offset
        self._attr2id = dict()
        self._id2attr = list()
    

    def toConsecutiveId(self, attr_id):
        """Create or get the continuous ID for an unordered ID.
        
        Args:
            attr_id (hashable): Unordered ID object.
        
        Returns:
            int: Continuous ID value.
        """
        if attr_id in self._attr2id.keys():
            return self._attr2id[attr_id]
        else:
            self._attr2id[attr_id] = self._next_id
            self._id2attr.append(attr_id)
            self._next_id += 1
            return self._next_id - 1
    

    def toAttributeId(self, cons_id):
        """Given a continuous ID, return it's correspond unordered ID.
        
        Args:
            cons_id (int): Continuous ID value.
       
        Returns:
            hashable: Unordered ID object.
        """
        return self._id2attr[cons_id - self._offset]


# TODO: Deprecated this function, use a more effective way to find node.
# Or, just cache the node object directly.
def find_tag_by_id(node, tag_name, tag_id):
    """Find the first match node in XML node and its sub nodes.
    Args:
        node (xmldom.Node): The XML node object to search.
        tag_name (str): The tag name of the element.
        tag_id (str) The id value of the element.
    
    Returns:
        xmldom.Node or None: Return the XML node object if found it, otherwise return None.
    """
    tags = node.getElementsByTagName(tag_name)
    for tag in tags:
        if tag.getAttribute('id') == tag_id:
            return tag
    return None


def clear_svg_animates(svg):
    """Clear all the animation effects in SVG.
    Args:
        svg (xmldom.Node): The SVG object to be cleared.
    """
    gg = svg.getElementsByTagName('g')
    for g in gg:
        animates_appear = g.getElementsByTagName('animate')
        if len(animates_appear):
            g.removeAttribute('style')
        animates_move = g.getElementsByTagName('animateMotion')
        for animate in animates_appear + animates_move:
            g.removeChild(animate)


def add_animate_move_into_node(g, animate, move, time, bessel):
    """
    Args:
        g (xmldom.Node): The SVG node to add move animation into.
        animate (xmldom.Node): The animate node to be added into node g.
        move (tuple(float, float)): (delt_x, delt_y) The delt move distance along x axis and y axis for this element.
        time (tuple(float, float)): (begin, end) The begin and end time of this animation.
        bessel (bool): Whether to set the path of this move animation as bezier curve.
    """
    g.appendChild(animate)
    if bessel:
        animate.setAttribute('path', 'm0,0 q{:.2f},{:.2f} {:.2f},{:.2f}'.format(move[0]*0.5-move[1]*0.2, move[1]*0.5+move[0]*0.2, move[0], move[1]))
    else:
        animate.setAttribute('path', 'm0,0 l{:.2f},{:.2f}'.format(move[0], move[1]))
    animate.setAttribute('begin', '{:.2f}s'.format(time[0]))
    animate.setAttribute('dur', '{:.2f}s'.format(time[1]-time[0]))
    animate.setAttribute('fill', 'freeze')


def add_animate_appear_into_node(g, animate, time, appear=True):
    """
        g (xmldom.Node): The SVG node to add appear animation into.
        animate (xmldom.Node): The animate node to be added into node g.
        time (tuple(float, float)) (begin, end) The begin and end time of this animation.
        appear (bool): True for appear animation; False for disappear animation.
    """
    g.setAttribute('style', 'opacity:{:.0f}'.format(not appear))
    g.appendChild(animate)
    animate.setAttribute('attributeName', 'opacity')
    animate.setAttribute('from', '{:.0f}'.format(not appear))
    animate.setAttribute('to', '{:.0f}'.format(appear))
    animate.setAttribute('begin', '{:.2f}s'.format(time[0]))
    animate.setAttribute('dur', '{:.2f}s'.format(time[1]-time[0]))
    animate.setAttribute('fill', 'freeze')


def auto_text_color(back_color):
    """Auto pick one text stroke color according to it's background color.
    
    Args:
        back_color ((R,G,B)): Text background color. R, G, B stand for color channel for red, green, blue.
            R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
    
    Returns:
        str: Text stroke color value formatted with hexadecimal number(SVG format).
            eg: '#FFFFFF'
    """
    rgb_sum = back_color[0]+back_color[1]+back_color[2]
    if rgb_sum < 150:
        return '#FFFFFF'
    else:
        return '#000000'


def rgbcolor2str(color):
    """Convert (R, G, B) formatted color into hexadecimal formatted string.
    
    Args:
        color ((R,G,B)): R, G, B stand for color channel for red, green, blue.
            R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
    
    Returns:
        str: Hexadecimal formatted string. (SVG format). eg: '#FFFFFF'
    """
    return '#{:0>2x}{:0>2x}{:0>2x}'.format(color[0], color[1], color[2])


def str2rgbcolor(color_str):
    """Convert hexadecimal formatted string into (R, G, B) formatted color.
    
    Args:
        color_str (str): Hexadecimal formatted string. (SVG format). eg: '#FFFFFF'
    
    Returns:
        (R,G,B): R, G, B stand for color channel for red, green, blue.
            R,G,B should be int value and 0 <= R,G,B <= 255. eg:(0, 255, 0)
    """
    color_str = color_str.strip('#')
    return (int(color_str[0:2], 16), int(color_str[2:4], 16), int(color_str[4:6], 16))


def text_font_size(text_width, text):
    """Calculate the font size based on the total width of the text and the text content.
        
    Args:
        text_width (float): The total width of the text.
        text (str): The text content (should be unicode format string).
    
    Returns:
        float: Text font size.
    """
    display_len = text_char_num(text)
    if display_len > 0:
        return min(16, text_width*1.6/display_len, text_width*0.8)
    else:
        return 0


def text_char_num(text):
    """Count the number of characters in the text.
    
    Args:
        text (str): The text content (should be unicode format string).
    
    Returns:
        int: The number of characters in the text.
    """
    count = 0
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            count += 2
        else:
            count += 1
    return count


def clamp(val, min_val, max_val):
    """
    Returns:
        The clamped value between min_val and max_val.
    """
    return max(min(val, max_val), min_val)


def add_desc_into_svg(dom):
    """Add description meta data into SVG dom tree.
    
    Args:
        dom (xmldom.document) The dom object to contain the description.
    """
    # Check if there is already a description in svg.
    svgs = dom.getElementsByTagName('svg')
    if len(svgs) == 0:
        return
    svg = svgs[0]
    descs = svg.getElementsByTagName('desc')
    if len(descs) > 0:
        return
    desc_str = 'Generated by algviz-{}(see {}).'.format(_version, _url)
    desc = dom.createElement('desc')
    text = dom.createTextNode('{}'.format(desc_str))
    desc.appendChild(text)
    svg.appendChild(desc)


def add_default_text_style(dom):
    """Add the default text style into svg.
    
    Args:
        dom (xmldom.document) The dom object to contain the description.
    """
    svgs = dom.getElementsByTagName('svg')
    if len(svgs) == 0:
        return
    svg = svgs[0]
    style = dom.createElement('style')
    style_content = r".txt { alignment-baseline:middle; text-anchor:middle; font-family:Times,serif; }"
    text = dom.createTextNode(style_content)
    style.appendChild(text)
    svg.appendChild(style)
