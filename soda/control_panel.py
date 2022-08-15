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

from . import ops


class SodaPanel:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"


class SodaMainPanel(SodaPanel, bpy.types.Panel):
    """ The main soda panel, shown in the tool settings """
    bl_label = "Soda"
    bl_idname = "SODA_PT_main_panel"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.operator(ops.CreateLightGroups.bl_idname)
        row = layout.row(align=True)
        row.operator(ops.UpdateNatron.bl_idname)
        row.operator(ops.RecreateNatron.bl_idname)
