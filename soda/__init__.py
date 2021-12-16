# This file is part of soda.
#
# soda is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# soda is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with soda.  If not, see <http://www.gnu.org/licenses/>.

# <pep8 compliant>

from . import ops
from . import preferences
from . import preferences_panel
from . import control_panel

import bpy


bl_info = {
    "name": "soda",
    "author": "Frank Firsching",
    "description": "A bridge to the compositing application Natron",
    "blender": (3, 0, 0),
    "version": (0, 1, 0),
    "location": "",
    "doc_url": "https://github.com/FrankFirsching/soda",
    "warning": "",
    "category": "Compositing"
}

classes = (
    ops.CreateViewLayers,
    ops.UpdateNatron,
    ops.RecreateNatron,
    preferences.Preferences,
    preferences_panel.PreferencesPanel,
    control_panel.SodaMainPanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
