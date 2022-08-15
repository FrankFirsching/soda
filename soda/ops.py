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
from . import core
from . import natron

class CreateLightGroups(bpy.types.Operator):
    """Create view layers for each light in the scene"""
    bl_idname = "soda.create_light_groups"
    bl_label = "SODA: Create light groups"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        pass

    def execute(self, context):
        core.setup_global_soda_settings(context)
        core.update_light_groups(context.scene, context.view_layer)
        core.create_comp_network_light_groups(context.scene)
        return {'FINISHED'}


class UpdateNatron(bpy.types.Operator):
    """Start natron and update the compositing graph"""
    bl_idname = "soda.update_natron"
    bl_label = "SODA: Update Natron"
    bl_options = {'REGISTER'}

    def __init__(self):
        pass

    def execute(self, context):
        natron.setupComp(context, True)
        return {'FINISHED'}

class RecreateNatron(bpy.types.Operator):
    """Start natron and update the compositing graph"""
    bl_idname = "soda.recreate_natron"
    bl_label = "SODA: Recreate Natron"
    bl_options = {'REGISTER'}

    def __init__(self):
        pass

    def execute(self, context):
        natron.setupComp(context, False)
        return {'FINISHED'}
