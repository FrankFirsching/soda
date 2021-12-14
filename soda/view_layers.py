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

def setup_global_soda_settings(context):
    context.scene.render.image_settings.file_format = "OPEN_EXR_MULTILAYER"

def layer_name(light):
    return "soda_"+light.name

def find_wrapped_collection(layer, collection):
    if layer.collection==collection:
        return layer
    for l in layer.children:
        x = find_wrapped_collection(l, collection)
        if x is not None:
            return x
    return None

def update_view_layers(scene):
    # Remove all old view layers
    for layer in scene.view_layers:
        if layer.name.startswith("soda_"):
            print(f"Removing old layer {layer.name}")
            scene.view_layers.remove(layer)
    
    # Collect all lights and ensure they are in their own collection
    all_lights = []
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT':
            collections = obj.users_collection
            for collection in collections:
                if len(collection.objects) > 1 or len(collection.children)>0:
                    # Need to move light into its own collection
                    new_collection = bpy.data.collections.new(obj.name)
                    collection.children.link(new_collection)
                    new_collection.objects.link(obj)
                    collection.objects.unlink(obj)
            all_lights.append(obj)
    
    # Create individual light layers
    all_layers = []
    for layer_light in all_lights:
        name = layer_name(layer_light)
        all_layers.append(name)
        layer = scene.view_layers.new(name)
        layer.use_sky = False
        for other_light in all_lights:
            enabled = (other_light==layer_light)
            # Now we can ensure, that the object is only in a single collection
            collection = other_light.users_collection[0]
            wrapped = find_wrapped_collection(layer.layer_collection, collection)
            wrapped.exclude = not enabled
    
    # Create the world HDRI layer
    hdri_layer_name = "soda_world_HDRI"
    layer = scene.view_layers.new(hdri_layer_name)
    layer.use_pass_ambient_occlusion = True
    layer.use_pass_cryptomatte_object = True
    layer.use_pass_z = True
    all_layers.append(hdri_layer_name)
    layer.use_sky = True
    for other_light in all_lights:
        enabled = False
        # Now we can ensure, that the object is only in a single collection
        collection = other_light.users_collection[0]
        wrapped = find_wrapped_collection(layer.layer_collection, collection)
        wrapped.exclude = not enabled

    return all_layers


def create_comp_network(scene, layers):
    tree = scene.node_tree
    tree.nodes.clear()
    spacing = (300, 250)

    output_node = tree.nodes.new("CompositorNodeOutputFile")
    output_node.location[0] = 3*spacing[0]
    output_node.location[1] = -0.5*len(layers)*spacing[1]
    output_node.layer_slots.clear()
    output_node.format.file_format = "OPEN_EXR_MULTILAYER"

    for i, l in enumerate(layers):
        node = tree.nodes.new("CompositorNodeRLayers")
        node.layer = l
        node.name = l
        node.label = l
        node.location[0] = (i%2)*spacing[0]
        node.location[1] = -i*spacing[1]
        # Link image slot to the respective light layer
        to_slot = output_node.layer_slots.new(l)
        tree.links.new(to_slot, node.outputs['Image'])
        # Link remaining data slots to the respective data layers
        for slot in node.outputs:
            if slot.enabled and slot.identifier not in ["Image", "Alpha", "Noisy Image"]:
                to_slot = output_node.layer_slots.new(slot.identifier)
                tree.links.new(to_slot, slot)
