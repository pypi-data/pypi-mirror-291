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

from .deps import load_SoGL, load_SwarmECS

import pygameGL.draw
import pygameGL.event
import pygameGL.audio

GL:bool=load_SoGL()
ECS:bool=load_SwarmECS()

def init() -> None:
    GL.soglInit()

import os, platform
if "PYGAME_GL_HIDE_SUPPORT_PROMPT" not in os.environ:
    print(f"PygameGL [ OpenGL 430 | GLFW 3.4 | GLEW 2.2.0 | Python {platform.python_version()} ]")
