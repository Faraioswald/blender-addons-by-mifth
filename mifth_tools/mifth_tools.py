# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

import bpy
from bpy.props import *
from bpy.types import Operator, AddonPreferences

import math

bpy.mifthTools = dict()


class MFTPanelBase(bpy.types.Panel):
    bl_label = "Base"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_category = 'Mifth'
    #bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        allObjects = context.scene.objects
        mifthTools = bpy.context.scene.mifthTools

        # GUI
        #row = layout.row()
        #row.label(text="Import/Export Objects")
        #row = layout.row()
        #row.prop(mifthTools, "type", text="")
        #row = layout.row()

        layout.operator("mft.clonetoselected", text="CloneToSelected")

        layout.separator()
        layout.operator("mft.radialclone", text="Radial Clone")
        row = layout.row()
        row.prop(mifthTools, "radialClonesNumber", text='')
        row.prop(mifthTools, "radialClonesAxis", text='')
        #row.prop(mifthTools, "radialClonesAxisType", text='')


class MFTPanelPlaykot(bpy.types.Panel):
    bl_label = "PlaykotTools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_category = 'Mifth'
    #bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        allObjects = context.scene.objects
        mifthTools = bpy.context.scene.mifthTools

        layout.operator("mft.cropnoderegion", text="CropNodeRegion")

        layout.separator()
        layout.operator("mft.outputcreator", text="Create Output")
        layout.prop(mifthTools, "outputFolder")
        row = layout.row()
        row.prop(mifthTools, "outputSubFolder")
        row.prop(mifthTools, "doOutputSubFolder", text='')
        layout.prop(mifthTools, "outputSequence")
        layout.prop(mifthTools, "outputSequenceSize")


class MFTCloneToSelected(bpy.types.Operator):
    bl_idname = "mft.clonetoselected"
    bl_label = "Clone To Selected"
    bl_description = "Clone To Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):

        if len(bpy.context.selected_objects) > 1:
            objToClone = bpy.context.scene.objects.active
            objectsToClone = []

            for obj in bpy.context.selected_objects:
                if obj != objToClone:
                    objectsToClone.append(obj)

            for obj in objectsToClone:
                bpy.ops.object.select_all(action='DESELECT')
                objToClone.select = True

                bpy.ops.object.duplicate(linked=True, mode='DUMMY')
                newDup = bpy.context.selected_objects[0]
                #print(newDup)
                newDup.location = obj.location
                newDup.rotation_euler = obj.rotation_euler
                newDup.scale = obj.scale

            bpy.ops.object.select_all(action='DESELECT')
            for obj3 in objectsToClone:
                obj3.select = True
            bpy.ops.object.delete(use_global=False)

            objectsToClone = None
        else:
            self.report({'INFO'}, "Need more Objects!")

        return {'FINISHED'}


class MFTRadialClone(bpy.types.Operator):
    bl_idname = "mft.radialclone"
    bl_label = "Radial Clone"
    bl_description = "Radial Clone"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):

        if len(bpy.context.selected_objects) > 0:
            activeObj = bpy.context.scene.objects.active
            selObjects = bpy.context.selected_objects
            mifthTools = bpy.context.scene.mifthTools
            clonez = mifthTools.radialClonesNumber

            for i in range(clonez - 1):
                newObj = bpy.ops.object.duplicate(linked=True, mode='DUMMY')
                #for obj in bpy.context.selected_objects:
                theAxis = (1, 0, 0)
                #theAxesGet = 0
                if mifthTools.radialClonesAxis == 'Y':
                    theAxis = (0, 1, 0)
                    #theAxesGet = 1
                elif mifthTools.radialClonesAxis == 'Z':
                    theAxis = (0, 0, 1)
                    #theAxesGet = 2
                
                rotateValue = (math.radians(360)/float(clonez))
                bpy.ops.transform.rotate(value=rotateValue, axis=theAxis)


            bpy.ops.object.select_all(action='DESELECT')

            for obj in selObjects:
                obj.select = True
            selObjects = None
            bpy.context.scene.objects.active = activeObj
        else:
            self.report({'INFO'}, "Select Objects!")

        return {'FINISHED'}


class MFTCropNodeRegion(bpy.types.Operator):
    bl_idname = "mft.cropnoderegion"
    bl_label = "Crop Node Region"
    bl_description = "Crop Node Region"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):

        scene = bpy.context.scene
        nodes = scene.node_tree.nodes
        cropNode = nodes.active

        if cropNode != None and cropNode.type == 'CROP':
            nodes.active.min_x = scene.render.border_min_x * scene.render.resolution_x
            nodes.active.max_x = scene.render.border_max_x * scene.render.resolution_x
            nodes.active.min_y = scene.render.border_min_y * scene.render.resolution_y
            nodes.active.max_y = scene.render.border_max_y * scene.render.resolution_y
        else:
            self.report({'INFO'}, "Select Crop Node!")

        return {'FINISHED'}


class MFTOutputCreator(bpy.types.Operator):
    bl_idname = "mft.outputcreator"
    bl_label = "Create Output"
    bl_description = "Output Creator"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):

        scene = bpy.context.scene
        nodes = scene.node_tree.nodes
        mifthTools = bpy.context.scene.mifthTools

        output_file = nodes.new("CompositorNodeOutputFile")
        output_file.base_path = "//" + mifthTools.outputFolder + "/"

        output_file.file_slots.remove(output_file.inputs[0])
        for i in range(mifthTools.outputSequenceSize):
            idx = str(i + 1)
            if i < 9:
                idx = "0" + idx

            outFile = ""
            if mifthTools.doOutputSubFolder is True:
                outFile = mifthTools.outputSubFolder + "_" + idx + "/"
            outFile += mifthTools.outputSequence + "_" + idx + "_"

            output_file.file_slots.new(outFile)

        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
