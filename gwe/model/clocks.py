# This file is part of gwe.
#
# Copyright (c) 2020 Roberto Leinardi
#
# gst is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gst is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gst.  If not, see <http://www.gnu.org/licenses/>.
from dataclasses import dataclass
from typing import Optional

@dataclass
class Clocks:
    graphic_current: Optional[int] = None
    graphic_max: Optional[int] = None
    sm_current: Optional[int] = None
    sm_max: Optional[int] = None
    memory_current: Optional[int] = None
    memory_max: Optional[int] = None
    video_current: Optional[int] = None
    video_max: Optional[int] = None
