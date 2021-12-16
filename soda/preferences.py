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

from bpy.props import StringProperty
from bpy.types import PropertyGroup


# Get the root level module name as our ID
id = __package__.split('.')[0]


def get_instance(context):
    """ Gets the blender managed instance of these preferences """
    global id
    # Unfortunately we need to reference a member of the preferences panel, since
    # blender doesn't separate UI and data for the preferences.
    return context.preferences.addons[id].preferences.soda


class Preferences(PropertyGroup):
    """ The preferences object for the soda add-on """
    natron_executable: StringProperty(name="Natron executable",
                                      description="The installation path of Natron (use an absolute path, so it "+
                                                  "works for every project).",
                                      subtype="FILE_PATH",
                                      options=set())
    project_comp_dir: StringProperty(name="Compositing projects directory",
                                     default="//../compositing/",
                                     description="The directory, where the Natron projects should be stored (use a " +
                                                 "relative path, so your projects are located nearby your blender " +
                                                 "scenes).",
                                     subtype="DIR_PATH", options=set())
