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
from . import view_layers
from . import natron

class CreateViewLayers(bpy.types.Operator):
    """Create view layers for each light in the scene"""
    bl_idname = "soda.create_view_layers"
    bl_label = "SODA: Create view layers"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        pass

    def execute(self, context):
        view_layers.setup_global_soda_settings(context)
        layers = view_layers.update_view_layers(context.scene)
        view_layers.create_comp_network(context.scene, layers)
        return {'FINISHED'}


class StartNatron(bpy.types.Operator):
    """Start natron and update the compositing graph"""
    bl_idname = "soda.start_natron"
    bl_label = "SODA: Start Natron"
    bl_options = {'REGISTER'}

    def __init__(self):
        pass

    def execute(self, context):
        natron.setupComp(context)
        return {'FINISHED'}
