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

import os


# We can use app1 here, since this script is passed to Natron on the command line, thus no
# other app object instances will be available yet.
app = app1


def findReader(filename):
    global app
    avgPos = [0, 0]
    numChildren = 0
    for child in app.getChildren():
        if child.isReaderNode() and child.getParam("filename").get() == filename:
            return child
        childPos = child.getPosition()
        avgPos[0] += childPos[0]
        avgPos[1] += childPos[1]
        numChildren += 1
    if numChildren > 0:
        avgPos[0] /= numChildren
        avgPos[1] /= numChildren
    else:
        avgPos[0] = 500
        avgPos[1] = 500
    node = app.createReader(filename)
    name = os.path.basename(filename)
    node.setScriptName(name)
    node.setLabel(name)
    node.setPosition(avgPos[0], avgPos[1]-500)
    return node


def findNode(name, pluginId, group=None):
    global app
    node = app.getNode(name) if group is None else group.getNode(name)
    if node is None:
        node = app.createNode(pluginId, group=group)
        node.setScriptName(name)
        node.setLabel(name.replace("soda_", ""))
    return node


def getLayers(reader):
    allLayers = reader.getAvailableLayers(-1)
    usedLayers = []
    for x in allLayers:
        layerName = x.getLayerName()
        if layerName.startswith("soda_"):
            usedLayers.append(layerName)
    return usedLayers


def setupLight(l, position, reader, group):
    hSpacing = 150
    vSpacing = 75
    shuffleNode = findNode(l, "net.sf.openfx.ShufflePlugin", group)
    shuffleNode.setPosition(position[0], position[1])
    if reader is not None:
        shuffleNode.connectInput(0, reader)
    param = shuffleNode.getParam("outputR")
    channel = "B."+l+".R"
    param.setValue(channel)

    solidNode = findNode(l+"_color", "net.sf.openfx.Solid", group)
    solidNode.setPosition(position[0]+hSpacing, position[1])
    param = solidNode.getParam("color")
    for i in range(3):
        param.setExpression("thisGroup."+l+"_col.getValue(dimension) * thisGroup."+l+"_int.getValue()", False, i)
    applyColorNode = findNode(l+"_apply", "net.sf.openfx.MergePlugin", group)
    applyColorNode.setPosition(position[0], position[1]+vSpacing)
    applyColorNode.getParam("operation").setValue("multiply")
    applyColorNode.connectInput(0, shuffleNode)
    applyColorNode.connectInput(1, solidNode)
    return applyColorNode


def setupComp(exrFile):
    hSpacing = 300
    vSpacing = 200

    reader = findReader(exrFile)
    readerPos = reader.getPosition()

    layers = getLayers(reader)
    numLayers = len(layers)

    lightMixerNode = findNode("lightMixer", "fr.inria.built-in.Group")
    lightMixerParams = lightMixerNode.createPageParam("mixer", "Mixer")
    lightMixerNode.setPosition(readerPos[0], readerPos[1]+vSpacing)
    lightMixerNode.connectInput(0, reader)
    lightMixerInput = findNode("Input1", None, lightMixerNode)
    lightMixerOutput = findNode("Output1", None, lightMixerNode)
    basePos = lightMixerInput.getPosition()

    mergeNodeInput = 0
    mergeNode = findNode("soda_addLayers", "net.sf.openfx.MergePlugin", lightMixerNode)
    mergeNode.getParam("operation").setValue("plus")
    mergeNode.setPosition(basePos[0], basePos[1]+2*vSpacing)
    for i in range(mergeNode.getMaxInputCount()):
        mergeNode.disconnectInput(i)

    lightMixerOutput.setPosition(basePos[0], basePos[1]+3*vSpacing)
    lightMixerOutput.disconnectInput(0)
    lightMixerOutput.connectInput(0, mergeNode)

    for i, l in enumerate(layers):
        # Setup a light
        groupParam = lightMixerNode.createGroupParam(l, l.replace("soda_", ""))
        groupParam.setOpened(True)
        lightMixerParams.addParam(groupParam)
        param = lightMixerNode.createColorParam(l+"_col", "Color", False)
        param.setMinimum(0)
        param.setDisplayMaximum(1)
        param.set(1, 1, 1, 1)
        param.setDefaultValue(1, 0)
        param.setDefaultValue(1, 1)
        param.setDefaultValue(1, 2)
        groupParam.addParam(param)
        param = lightMixerNode.createDoubleParam(l+"_int", "Intensity")
        param.setMinimum(0)
        param.setDisplayMaximum(10)
        param.set(1)
        param.setDefaultValue(1)
        groupParam.addParam(param)
        position = (basePos[0]+(i-0.5*numLayers)*hSpacing, basePos[1]+vSpacing)
        shuffle = setupLight(l, position, lightMixerInput, lightMixerNode)
        # and connect to the merge node
        mergeNode.connectInput(mergeNodeInput, shuffle)
        mergeNodeInput += 1
        if mergeNodeInput == 2:
            mergeNodeInput += 1  # Skip the mask input
