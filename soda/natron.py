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

import subprocess
import os
import bpy

from . import preferences

def rendered_file_path(context):
    # Find the file output node
    tree = context.scene.node_tree
    output_node = None
    for n in tree.nodes:
        if n.type == "OUTPUT_FILE":
            output_node = n
            break
    if output_node is None:
        raise RuntimeError("No output node in compositor found.")
    
    rendered_file = output_node.base_path
    if rendered_file.startswith("//"):
        rendered_file = os.path.join(os.path.dirname(bpy.data.filepath), rendered_file[2:])
        rendered_file = os.path.abspath(rendered_file)
    if context.scene.render.use_file_extension:
        # The output node still has the same format as the global, so we ask that one, since the node itself
        # doesn't provide the extension
        rendered_file += context.scene.render.file_extension
    return rendered_file


def setupComp(context):
    rendered_file = rendered_file_path(context)
    print(rendered_file)
    natron_exec = preferences.get_instance(context).natron_executable
    if not os.path.exists(natron_exec):
        raise RuntimeError(f"Invalid natron executable given: '{natron_exec}'")
    script_path = os.path.join(os.path.dirname(__file__), "natron_scripts", "natron_setup.py")
    trigger = f"setupComp('{rendered_file}')"
    exec_args = [natron_exec, '-c', f"exec(open('{script_path}').read())", '-c', trigger]
    print("Setting up natron comp:", exec_args)
    result = subprocess.Popen(exec_args)
