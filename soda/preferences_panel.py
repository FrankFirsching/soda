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

import bpy
from . import preferences


class PreferencesPanel(bpy.types.AddonPreferences):
    bl_idname = preferences.id

    # If this is changed, please also change preferences.get_instance()
    # Blender doesn't separate UI and data for preferences.
    soda: bpy.props.PointerProperty(type=preferences.Preferences)

    def draw(self, context):
        layout = self.layout.column()
        layout.prop(self.soda, "natron_executable")
        layout.prop(self.soda, "project_comp_dir")
