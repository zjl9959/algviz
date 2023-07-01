#!/usr/bin/env python3

"""Sequencer can sequence different svg animation frames.

Author: zjl9959@gmail.com

License: GPLv3

"""


from xml.dom.minidom import parseString, Document


class Sequencer:
    def __init__(self, vid, display_obj, root_dom, uid):
        self._vid = vid                     # This id bound with the Visualizer and Layouter.
        self._display_obj = display_obj     # The data object to be displayed.
        self._root_dom = root_dom           # The root dom Document to contain all the new created nodes.
        self._uid = uid                     # Unique id for this sequencer.
        self._size = list()                 # The svg size at each frame.
        self._frames = list()               # list(xmldom.Element) frame group node.

    def size(self, start_frame, end_frame):
        """Return the maximum size of all the svg frames.
        Returns:
            (int, int): (max_width, max_height).
        """
        max_width, max_height = 0, 0
        for i in range(start_frame, end_frame):
            (width, height) = self._size[i]
            if max_width < width:
                max_width = width
            if max_height < height:
                max_height = height
        return (max_width, max_height)

    def same_as(self, display_obj):
        """Check if the display_obj is the same as sequencer manager's obj.
        """
        return id(self._display_obj) == id(display_obj)

    def update(self, frame_count, skip=False):
        """Update the svg content of current frame.

        This function just cache the svg nodes of display_obj,
        But will not modify the content.

        """
        # Wrap the svg's child node with a frame group.
        g_frame = self._root_dom.createElement('g')
        g_frame.setAttribute('class', 'frame')
        g_frame.setAttribute('style', 'opacity:0')
        if not skip:
            if len(self._frames) != frame_count:
                raise Exception("Sequence:{}.update frame count({}) error!".format(self, frame_count))
            # Get svg xmldom tree from display_obj.
            dom = parseString(self._display_obj._repr_svg_())
            if type(dom) != Document:
                return
            svgs = dom.getElementsByTagName('svg')
            if len(svgs) == 0:
                return
            svg = svgs[0]
            # Try update svg max size.
            width = int(svg.getAttribute('width')[0:-2])
            height = int(svg.getAttribute('height')[0:-2])
            self._size.append((width, height))
            cache_child_nodes = list()
            for child in svg.childNodes:
                if hasattr(child, 'tagName') and (child.tagName == 'g' or child.tagName == 'svg'):
                    cache_child_nodes.append(child)
            for child in cache_child_nodes:
                g_frame.appendChild(child)
        else:
            self._size.append((0, 0))
        # Cache the g_frame node.
        self._frames.append(g_frame)

    def export(self, pos_offset, frame_delays, start_frame, end_frame, logo):
        """Return the merged dom tree which contain all the svg frames.

        This will traverse all the <g>...</g> nodes in svg and update all
        the 'x' and 'y' attributes by pos_offset. At the same time, all
        the 'begin' attribute in <animate> and <animateMotion> nodes will
        be changed into event base on key frame animations.

        Args:
            pos_offset (float, float): The x and y position's offset of the nodes.

        Returns:
            dict_values(xmldom.Element): The svg nodes for all the frames.

        """
        start_frame = max(start_frame, 0)
        end_frame = min(end_frame, len(self._frames))
        for frame in range(start_frame, end_frame):
            g_frame = self._frames[frame]
            g_frame.setAttribute('transform', 'translate({},{})'.format(pos_offset[0], pos_offset[1]))
            self._update_gframe_animates_(g_frame, frame)
            animate_appear = None
            if frame == start_frame:
                if logo:
                    animate_appear = self._create_first_frame_animate(start_frame, end_frame + 1, frame, end_frame - 1, frame_delays)
                else:
                    animate_appear = self._create_first_frame_animate(start_frame, end_frame, frame, end_frame - 1, frame_delays)
            else:
                animate_appear = self._create_frame_appear_animate_(frame, frame - 1)
            g_frame.appendChild(animate_appear)
            animate_disappear = self._create_frame_disappear_animate_(frame, frame_delays[frame])
            g_frame.appendChild(animate_disappear)
        return self._frames

    def export_logo(self, pos_offset, frame_delays, start_frame, end_frame):
        start_frame = max(start_frame, 0)
        end_frame = min(end_frame, len(self._frames))
        frame = end_frame
        g_frame = self._frames[frame]
        g_frame.setAttribute('transform', 'translate({},{})'.format(pos_offset[0], pos_offset[1]))
        self._update_gframe_animates_(g_frame, frame)
        animate_appear = self._create_first_frame_animate(start_frame, end_frame, frame, frame, frame_delays)
        g_frame.appendChild(animate_appear)
        animate_disappear = self._create_frame_disappear_animate_(frame, frame_delays[frame])
        g_frame.appendChild(animate_disappear)
        return g_frame

    def _create_first_frame_animate(self, frame_start, frame_end, first_frame, last_frame, frame_delays):
        animate = self._root_dom.createElement('animate')
        animate.setAttribute('attributeName', 'opacity')
        animate.setAttribute('id', 'V{}_{}S{}'.format(self._vid, self._uid, first_frame))
        animate.setAttribute('from', '0')
        animate.setAttribute('to', '1')
        start_delay_time = 0
        for i in range(frame_start, first_frame):
            start_delay_time += frame_delays[i]
        end_delay_time = 0
        for i in range(last_frame + 1, frame_end):
            end_delay_time += frame_delays[i]
        animate.setAttribute('begin', '{}s;V{}_{}E{}.end+{}s'.format(
            start_delay_time, self._vid, self._uid, last_frame, start_delay_time + end_delay_time))
        animate.setAttribute('dur', '0.01s')
        animate.setAttribute('fill', 'freeze')
        return animate

    def _create_frame_appear_animate_(self, frame, last_frame):
        animate = self._root_dom.createElement('animate')
        animate.setAttribute('attributeName', 'opacity')
        animate.setAttribute('id', 'V{}_{}S{}'.format(self._vid, self._uid, frame))
        animate.setAttribute('from', '0')
        animate.setAttribute('to', '1')
        animate.setAttribute('begin', 'V{}_{}E{}.begin'.format(self._vid, self._uid, last_frame))
        animate.setAttribute('dur', '0.01s')
        animate.setAttribute('fill', 'freeze')
        return animate

    def _create_frame_disappear_animate_(self, frame, delay):
        animate = self._root_dom.createElement('animate')
        animate.setAttribute('attributeName', 'opacity')
        animate.setAttribute('id', 'V{}_{}E{}'.format(self._vid, self._uid, frame))
        animate.setAttribute('begin', 'V{}_{}S{}.begin+{}s'.format(self._vid, self._uid, frame, delay))
        animate.setAttribute('from', '1')
        animate.setAttribute('to', '0')
        animate.setAttribute('dur', '0.01s')
        animate.setAttribute('fill', 'freeze')
        return animate

    def _update_animate_opacity_(self, animate_node, frame):
        begin = animate_node.getAttribute('begin')
        animate_node.setAttribute('begin', 'V{}_{}S{}.end+{}'.format(self._vid, self._uid, frame, begin))
        parent_node = animate_node.parentNode
        if parent_node:
            from_opacity = float(animate_node.getAttribute('from'))
            to_opacity = float(animate_node.getAttribute('to'))
            # Reset node opacity after frame end.
            fade_animate = self._root_dom.createElement('animate')
            fade_animate.setAttribute('attributeName', 'opacity')
            fade_animate.setAttribute('from', '{:.0f}'.format(1 - from_opacity))
            fade_animate.setAttribute('to', '{:.0f}'.format(1 - to_opacity))
            fade_animate.setAttribute('begin', 'V{}_{}E{}.end'.format(self._vid, self._uid, frame))
            fade_animate.setAttribute('dur', '0.01s')
            fade_animate.setAttribute('fill', 'freeze')
            parent_node.appendChild(fade_animate)

    def _update_animate_motion(self, animate_node, frame):
        begin = animate_node.getAttribute('begin')
        animate_node.setAttribute('begin', 'V{}_{}S{}.end+{}'.format(self._vid, self._uid, frame, begin))
        parent_node = animate_node.parentNode
        # Reset node position after frame end.
        if parent_node:
            reset_animate = self._root_dom.createElement('animateMotion')
            reset_animate.setAttribute('path', 'm0,0 l0,0')
            reset_animate.setAttribute('begin', 'V{}_{}E{}.end'.format(self._vid, self._uid, frame))
            reset_animate.setAttribute('dur', '0.01s')
            reset_animate.setAttribute('fill', 'freeze')
            parent_node.appendChild(reset_animate)

    def _update_text_animate(self, animate_node, frame):
        begin = animate_node.getAttribute('begin')
        animate_node.setAttribute('begin', 'V{}_{}S{}.end+{}'.format(self._vid, self._uid, frame, begin))
        parent_node = animate_node.parentNode
        if parent_node:
            from_font_size = animate_node.getAttribute('from')
            to_font_size = animate_node.getAttribute('to')
            reset_animate = self._root_dom.createElement('animate')
            reset_animate.setAttribute('attributeName', 'font-size')
            reset_animate.setAttribute('from', to_font_size)
            reset_animate.setAttribute('to', from_font_size)
            reset_animate.setAttribute('begin', 'V{}_{}E{}.end'.format(self._vid, self._uid, frame))
            reset_animate.setAttribute('dur', '0.01s')
            reset_animate.setAttribute('fill', 'freeze')
            parent_node.appendChild(reset_animate)

    def _update_gframe_animates_(self, g_frame, frame):
        node_stack = [g_frame]
        while len(node_stack):
            node = node_stack.pop()
            if not hasattr(node, 'tagName'):
                continue
            tag = node.tagName
            if tag == 'animate':
                node_attr = node.getAttribute('attributeName')
                if node_attr == 'opacity':
                    self._update_animate_opacity_(node, frame)
                elif node_attr == 'font-size':
                    self._update_text_animate(node, frame)
            elif tag == 'animateMotion':
                self._update_animate_motion(node, frame)
            elif tag == 'g' or tag == 'text':
                for child in node.childNodes:
                    node_stack.append(child)
