#!/usr/bin/env python3

"""Layouter can merge different svg animatins into single svg animation.

The Layouter class amied to implement some interfaces in IPython.display for algviz server environment.

Author: zjl9959@gmail.com

License: GPLv3

"""


from xml.dom.minidom import Document
from os import path as os_path
from platform import uname
from ctypes import c_int
from ctypes import Structure as ctypes_Structure
from math import ceil

from algviz.utility import add_default_text_style, text_char_num, AlgvizRuntimeError, FONT_FAMILY
from algviz.sequencer import Sequencer
from algviz.logo import get_logo, get_logo_size


LOGO_SHOW_TIME = 3
WEB_URL = 'https://algviz.com/'
SVG_MARGIN = 5
NAME_MARGIN = 5


class Layouter:
    def __init__(self, vid):
        self._vid = vid                     # Identify different layouter.
        self._display_id2seq = dict()       # Key:display_id; Value:Sequencer
        self._display_id2name = dict()      # Key:display_id; Value:(ObjNameString, title_font)
        self._delays = list()               # Record the delay time for each frame.
        self._next_seq_id = 0               # The unique id for next sequencer.
        # Create xmldom object and svg.
        self._dom = Document()
        self._svg = self._dom.createElement('svg')
        self._svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
        self._svg.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        self._dom.appendChild(self._svg)
        add_default_text_style(self._dom)
        self._link = self._dom.createElement('a')
        self._link.setAttribute('xlink:href', WEB_URL)
        self._svg.appendChild(self._link)
        logo_size = get_logo_size()
        # Initial svg size same as logo size.
        self._svg_width = logo_size[0]
        self._svg_height = logo_size[1]
        self._max_width = 800
        self._svg_str = None
        self._update_svg_size_()

    def solve_layout(self, strip_width, start_frame, end_frame):
        """Layout all the svg animation pictures.
        Returns:
            dict(str, (float, float)): Key:display_id; Value:(x_offset, y_offset).
        """
        width, height = 0, 0
        rects_num = len(self._display_id2seq)
        RectArrayType = RectType * rects_num
        rects_data = RectArrayType()
        id_map = dict()
        next_id = 0
        max_rect_width = 0
        for did, seq in self._display_id2seq.items():
            rects_data[next_id].id = next_id
            id_map[next_id] = did
            seq_size = seq.size(start_frame, end_frame)
            title_font = 0
            if did in self._display_id2name:
                title = self._display_id2name[did][0]
                title_char_num = text_char_num(title)
                title_font = 0
                if title_char_num > 0:
                    temp_title_font = seq_size[0] * 1.2 / title_char_num
                    title_font = ceil(min(12, temp_title_font, seq_size[0] * 0.8))
                self._display_id2name[did][1] = title_font
            rects_data[next_id].w = seq_size[0] + SVG_MARGIN
            rects_data[next_id].h = ceil(seq_size[1] + title_font * 1.5 + SVG_MARGIN)
            max_rect_width = max(max_rect_width, rects_data[next_id].w)
            next_id = next_id + 1
        strip_w = c_int(max(strip_width, max_rect_width + 50))
        rect_num_c = c_int(rects_num)
        try:
            packing_solver = load_dll()
            packing_solver.solve_strip_packing(strip_w, rect_num_c, rects_data)
        except Exception as e:
            print('Error when call packing solver:', e)
            return None
        display_offsets = dict()
        for i in range(len(rects_data)):
            did = id_map[rects_data[i].id]
            title_font = 0
            if did in self._display_id2name:
                title_font = self._display_id2name[did][1]
            display_offsets[did] = (
                rects_data[i].x + SVG_MARGIN,
                rects_data[i].y + title_font * 1.5 + SVG_MARGIN,
                rects_data[i].w, rects_data[i].h
            )
            width = max(width, rects_data[i].x + rects_data[i].w)
            height = max(height, rects_data[i].y + rects_data[i].h + title_font * 1.5)
        if width > 0 and height > 0:
            self._svg_width = width + SVG_MARGIN
            self._svg_height = height + SVG_MARGIN
            self._update_svg_size_()
        return display_offsets

    def _update_svg_size_(self):
        self._svg.setAttribute('width', '{:.0f}pt'.format(self._svg_width))
        self._svg.setAttribute('height', '{:.0f}pt'.format(self._svg_height))
        self._svg.setAttribute('viewBox', '0.00 0.00 {:.2f} {:.2f}'.format(self._svg_width, self._svg_height))

    def display(self, display_obj, display_id):
        from algviz.visual import _NameDisplay
        if isinstance(display_obj, _NameDisplay):
            title = display_obj.__repr__()
            if len(title) > 1:
                display_id = display_id.replace('algviz_', '')
                self._display_id2name[display_id] = [title, 0]     # Record title string and font size.
        elif display_id not in self._display_id2seq:
            seq = Sequencer(self._vid, display_obj, self._dom, self._next_seq_id)
            for i in range(len(self._delays)):
                seq.update(i, skip=True)    # Skip none displayed frames.
            seq.update(len(self._delays))
            display_id = display_id.replace('algviz', '')
            self._display_id2seq[display_id] = seq
            self._next_seq_id += 1

    def update_display(self, display_obj, display_id):
        display_id = display_id.replace('algviz', '')
        if display_id in self._display_id2seq:
            seq = self._display_id2seq[display_id]
            if seq.same_as(display_obj):
                seq.update(len(self._delays))

    def next_frame(self, delay):
        self._delays.append(delay)

    def _add_logo_(self, start_frame, end_frame):
        logo = get_logo(self._svg_width, self._svg_height)
        seq = Sequencer(self._vid, logo, self._dom, self._next_seq_id)
        for i in range(end_frame):
            seq.update(i, skip=True)
        seq.update(end_frame)
        offset = (logo.offset_x, logo.offset_y)
        obj_node = seq.export_logo(offset, self._delays, start_frame, end_frame)
        self._link.appendChild(obj_node)

    def _add_backgrounds_(self, display_offsets, start_frame, end_frame):
        bg_group = self._dom.createElement('g')
        # Add disappear animate.
        bg_disappear = self._dom.createElement('animate')
        bg_disappear.setAttribute('attributeName', 'opacity')
        bg_disappear.setAttribute('begin', 'V{}_{}S{}.begin'.format(self._vid, self._next_seq_id, end_frame))
        bg_disappear.setAttribute('from', '1')
        bg_disappear.setAttribute('to', '0')
        bg_disappear.setAttribute('dur', '0.01s')
        bg_disappear.setAttribute('fill', 'freeze')
        bg_group.appendChild(bg_disappear)
        # Add appear animate.
        bg_appear = self._dom.createElement('animate')
        bg_appear.setAttribute('attributeName', 'opacity')
        bg_appear.setAttribute('from', '0')
        bg_appear.setAttribute('to', '1')
        bg_appear.setAttribute('begin', 'V{}_{}E{}.end'.format(self._vid, self._next_seq_id, end_frame))
        bg_appear.setAttribute('dur', '0.01s')
        bg_appear.setAttribute('fill', 'freeze')
        bg_group.appendChild(bg_appear)
        # Add display object title name.
        for display_id, title_info in self._display_id2name.items():
            offset = display_offsets[display_id]
            title, txt_font = title_info[0], title_info[1]
            t = self._dom.createElement('text')
            t.setAttribute('x', '{:.2f}'.format(offset[0] + NAME_MARGIN))
            t.setAttribute('y', '{:.2f}'.format(offset[1] - txt_font * 0.3))
            t.setAttribute('font-family', FONT_FAMILY)
            t.setAttribute('font-weight', 'bold')
            t.setAttribute('font-size', '{:.2f}'.format(txt_font))
            t.setAttribute('fill', '#808080')
            tt = self._dom.createTextNode(title)
            t.appendChild(tt)
            bg_group.appendChild(t)
        # Add outline rectangle.
        self.layout_info = dict()
        if len(self._display_id2seq) > 1:
            for display_id, seq in self._display_id2seq.items():
                seq_size = seq.size(start_frame, end_frame)
                offset = display_offsets[display_id]
                txt_font = 0
                if display_id in self._display_id2name:
                    txt_font = self._display_id2name[display_id][1]
                r = self._dom.createElement('rect')
                r.setAttribute('x', '{:.2f}'.format(offset[0]))
                r.setAttribute('y', '{:.2f}'.format(offset[1] - txt_font * 1.5))
                r.setAttribute('width', '{:.2f}'.format(seq_size[0]))
                r.setAttribute('height', '{:.2f}'.format(seq_size[1] + txt_font * 1.5))
                r.setAttribute('stroke', '#C0C0C0')
                r.setAttribute('stroke-dasharray', '1, 5')
                r.setAttribute('fill', 'none')
                bg_group.appendChild(r)
                self.layout_info[display_id] = (offset[0], offset[1] - txt_font * 1.5, seq_size[0], seq_size[1] + txt_font * 1.5)
        self._link.appendChild(bg_group)

    def _repr_svg_(self):
        if self._svg_str is None:
            self._svg_str = self.export(self._max_width, 0, None)
        return self._svg_str

    def export(self, max_width, start_frame, end_frame):
        # Layout and add nodes into dom tree.
        if end_frame is None:
            end_frame = len(self._delays)
        display_offsets = self.solve_layout(max_width, start_frame, end_frame)
        if display_offsets is None:
            return
        self._delays.insert(end_frame, LOGO_SHOW_TIME)
        for display_id, seq in self._display_id2seq.items():
            offset = display_offsets[display_id]
            obj_nodes = seq.export(offset, self._delays, start_frame, end_frame, True)
            for i in range(start_frame, end_frame):
                self._link.appendChild(obj_nodes[i])
        self._add_logo_(start_frame, end_frame)
        self._add_backgrounds_(display_offsets, start_frame, end_frame)
        duration = 0
        for i in range(start_frame, end_frame):
            duration += self._delays[i]
        duration += LOGO_SHOW_TIME
        info = {
            "size": (self._svg_width, self._svg_height),
            "duration": duration,
            "frames": end_frame - start_frame,
            "layout": self.layout_info
        }
        return self._dom.toxml(), info


class RectType(ctypes_Structure):
    _fields_ = [
        ('id', c_int),
        ('w', c_int),
        ('h', c_int),
        ('x', c_int),
        ('y', c_int)
    ]


# Dll releated.
LIB_PATH = {
    'Windows': {
        'amd64': 'lib\\packing_solver_win_amd64.dll',
        'x86_64': 'lib\\packing_solver_win_amd64.dll',
    },
    'Linux': {
        'amd64': 'lib/packing_solver_linux_amd64.so',
        'x86_64': 'lib/packing_solver_linux_amd64.so',
    }
}


def load_dll():
    platform_info = uname()
    sys = platform_info.system
    machine = platform_info.machine.lower()
    if sys in LIB_PATH and machine in LIB_PATH[sys]:
        script_path = os_path.split(os_path.realpath(__file__))[0]
        lib_path = os_path.join(script_path, LIB_PATH[sys][machine])
        if sys == 'Windows':
            return load_dll_win(lib_path)
        elif sys == 'Linux':
            return load_dll_linux(lib_path)
    raise AlgvizRuntimeError('Not supported platform:{}_{}!'.format(sys, machine))


def load_dll_win(dll_path):
    from win32api import LoadLibraryEx
    from win32con import LOAD_WITH_ALTERED_SEARCH_PATH
    from ctypes import WinDLL
    dll_handle = LoadLibraryEx(dll_path, 0, LOAD_WITH_ALTERED_SEARCH_PATH)
    packing_solver = WinDLL(dll_path, handle=dll_handle)
    return packing_solver


def load_dll_linux(dll_path):
    from ctypes import cdll
    return cdll.LoadLibrary(dll_path)


def is_layout_supported():
    try:
        load_dll()
        return True
    except Exception:
        return False
