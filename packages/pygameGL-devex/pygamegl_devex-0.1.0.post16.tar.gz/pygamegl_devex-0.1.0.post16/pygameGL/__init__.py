# pygameGL - Python Game-Development Library
# Copyright (C) 2023-2024 Izaiyah Stokes
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Izaiyah Stokes
# zeroth.bat@gmail.com
"""PygameGL is a set of Python modules designed for developing games in python.
It is written leveraging software within the powerful OpenGL ecosystem. This allows you
to create full-fleged games in python with features and performance like never before."""

import ctypes

from .swarm import load_SwarmECS
from .sogl import load_SoGL, SGcontext

import pygameGL.draw
import pygameGL.event
import pygameGL.audio

SOGL=load_SoGL()
if SOGL == None:
    print("Error loading SoGL Library!\n")
    raise ModuleNotFoundError

ECS:bool=load_SwarmECS()

def init() -> None:
    SOGL.soglInit()

def make_context() -> SGcontext: return SGcontext()

def debug_context(ctx:SGcontext) -> None:
    SOGL.sgContextDebug()

def should_quit(win) -> bool:
    return SOGL.sgShouldQuit(win) == 1

def poll_events() -> None:
    SOGL.sgPollEvents()

def set_icon(win, icon) -> None:
    SOGL.sgSetWindowIcon(win, icon)

def set_title(win, title:str) -> None:
    SOGL.sgSetWindowTitle(win, title)

def make_window(w:int, h:int, title:str):
    win = SOGL.sgMakeWindow(w, h, title)
    return ctypes.c_void_p(win)

def clear_color(r:int, g:int, b:int, a:int) -> None:
    SOGL.sgClearColor(r, g, b, a)

def buffer_swap(win) -> None:
    SOGL.sgBufferSwap(win)

def window_valid(win) -> None:
    SOGL.sgWindowValid(win)

import os, platform
if "PYGAME_GL_HIDE_SUPPORT_PROMPT" not in os.environ:
    print("\n---------------------------------------------------------------")
    print(f"PygameGL [ OpenGL 430 | GLFW 3.4 | GLEW 2.2.0 | Python {platform.python_version()} ]")
    print("---------------------------------------------------------------\n")
