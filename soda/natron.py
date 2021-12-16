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

BLEND_EXT = ".blend"
NATRON_EXT = ".ntp"


def find_latest_version(file):
    if os.path.exists(file):
        return file
    no_ext = file.removesuffix(NATRON_EXT)
    num_digits = 0
    while no_ext[-num_digits-1].isdigit():
        num_digits += 1
    num = int(no_ext[-num_digits:]) if num_digits > 0 else 0
    no_num = no_ext[:-num_digits]
    if num > 0:
        str_num = f"{num-1}"
        str_num = "0"*(num_digits-len(str_num))+str_num
        new_check = no_num+str_num+NATRON_EXT
        return find_latest_version(new_check)
    elif num_digits > 0:
        return find_latest_version(no_num + NATRON_EXT)
    return ""


def find_natron_file(context):
    blend_file = bpy.data.filepath
    filename = os.path.basename(blend_file)
    filename = filename.replace(BLEND_EXT, NATRON_EXT)
    comp_dir = preferences.get_instance(context).project_comp_dir
    comp_dir = comp_dir.removeprefix("//")
    natron_file = os.path.join(os.path.dirname(blend_file), comp_dir, filename)
    natron_file = os.path.abspath(natron_file)
    return find_latest_version(natron_file)


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


def setupComp(context, update_natron):
    rendered_file = rendered_file_path(context)
    comp_file = find_natron_file(context) if update_natron else ""
    print("comp_file:", comp_file)
    natron_exec = preferences.get_instance(context).natron_executable
    if not os.path.exists(natron_exec):
        raise RuntimeError(f"Invalid natron executable given: '{natron_exec}'")
    script_path = os.path.join(os.path.dirname(__file__), "natron_scripts", "natron_setup.py")
    trigger = f"setupComp('{rendered_file}', '{comp_file}')"
    exec_args = [natron_exec, '-c', f"exec(open('{script_path}').read())", '-c', trigger]
    print("Setting up natron comp:", exec_args)
    result = subprocess.Popen(exec_args)
