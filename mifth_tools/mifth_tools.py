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


class MFTPanelCloning(bpy.types.Panel):
    bl_label = "Cloning"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_category = 'Mifth'
    #bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
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
        #layout.prop(mifthTools, "radialClonesNumber", text='')
        row = layout.row()
        row.prop(mifthTools, "radialClonesAxis", text='')
        row.prop(mifthTools, "radialClonesAxisType", text='')
        #row.prop(mifthTools, "radialClonesAngle", text='')


class MFTPanelCurves(bpy.types.Panel):
    bl_label = "Curves"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_category = 'Mifth'
    #bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        mifthTools = bpy.context.scene.mifthTools

        layout.operator("mft.curveanimator", text="Curve Animator")
        layout.prop(mifthTools, "doUseSceneFrames", text='UseSceneFrames')
        row = layout.row()
        row.prop(mifthTools, "curveAniStartFrame", text='Start')
        row.prop(mifthTools, "curveAniEndFrame", text='End')
        row = layout.row()
        row.prop(mifthTools, "curveAniStepFrame", text='Steps')
        row.prop(mifthTools, "curveAniInterpolation", text='Interpolation')
        


class MFTPanelPlaykot(bpy.types.Panel):
    bl_label = "PlaykotTools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_category = 'Mifth'
    #bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
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

    def execute(self, context):

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

    radialClonesAngle = FloatProperty(
        default = 360.0,
        min = -360.0,
        max = 360.0
    )
    clonez = IntProperty(
            default = 8,
            min = 2,
            max = 300
        )

    def execute(self, context):

        if len(bpy.context.selected_objects) > 0:
            activeObj = bpy.context.scene.objects.active
            selObjects = bpy.context.selected_objects
            mifthTools = bpy.context.scene.mifthTools
            #self.clonez = mifthTools.radialClonesNumber

            activeObjMatrix = activeObj.matrix_world

            for i in range(self.clonez - 1):
                bpy.ops.object.duplicate(linked=True, mode='DUMMY')
                #newObj = bpy.context.selected_objects[0]
                #print(newObj)
                #for obj in bpy.context.selected_objects:
                theAxis = None

                if mifthTools.radialClonesAxis == 'X':
                    if mifthTools.radialClonesAxisType == 'Local':
                        theAxis = (activeObjMatrix[0][0], activeObjMatrix[1][0], activeObjMatrix[2][0])
                    else:
                        theAxis = (1, 0, 0)

                elif mifthTools.radialClonesAxis == 'Y':
                    if mifthTools.radialClonesAxisType == 'Local':
                        theAxis = (activeObjMatrix[0][1], activeObjMatrix[1][1], activeObjMatrix[2][1])
                    else:
                        theAxis = (0, 1, 0)

                elif mifthTools.radialClonesAxis == 'Z':
                    if mifthTools.radialClonesAxisType == 'Local':
                        theAxis = (activeObjMatrix[0][2], activeObjMatrix[1][2], activeObjMatrix[2][2])
                    else:
                        theAxis = (0, 0, 1)
                
                rotateValue = (math.radians(self.radialClonesAngle)/float(self.clonez))
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

    def execute(self, context):

        scene = bpy.context.scene
        nodes = scene.node_tree.nodes
        cropNode = nodes.active

        if cropNode != None:
            if cropNode.type == 'CROP':
                cropNode.min_x = scene.render.border_min_x * scene.render.resolution_x
                cropNode.max_x = scene.render.border_max_x * scene.render.resolution_x
                cropNode.min_y = scene.render.border_max_y * scene.render.resolution_y
                cropNode.max_y = scene.render.border_min_y * scene.render.resolution_y

            elif cropNode.type == 'GROUP':
                cropGroupNode = cropNode.node_tree.nodes.active

                if cropGroupNode != None and cropGroupNode.type == 'CROP':
                    cropGroupNode.min_x = scene.render.border_min_x * scene.render.resolution_x
                    cropGroupNode.max_x = scene.render.border_max_x * scene.render.resolution_x
                    cropGroupNode.min_y = scene.render.border_max_y * scene.render.resolution_y
                    cropGroupNode.max_y = scene.render.border_min_y * scene.render.resolution_y
        else:
            self.report({'INFO'}, "Select Crop Node!")

        return {'FINISHED'}


class MFTOutputCreator(bpy.types.Operator):
    bl_idname = "mft.outputcreator"
    bl_label = "Create Output"
    bl_description = "Output Creator"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

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


class MFTCurveAnimator(bpy.types.Operator):
    bl_idname = "mft.curveanimator"
    bl_label = "Curve Animator"
    bl_description = "Curve Animator"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        mifthTools = bpy.context.scene.mifthTools

        startFrame = bpy.context.scene.frame_start
        if mifthTools.doUseSceneFrames is False:
            startFrame = mifthTools.curveAniStartFrame

        endFrame = bpy.context.scene.frame_end
        if mifthTools.doUseSceneFrames is False:
            endFrame = mifthTools.curveAniEndFrame

        totalFrames = endFrame - startFrame
        frameSteps = mifthTools.curveAniStepFrame - 1

        for curve in bpy.context.selected_objects:
            if curve.type == 'CURVE':

                for frStep in range(frameSteps + 1):
                    aniPos = 1.0 - (float(frStep)/float(frameSteps))
                    goToFrame = int(aniPos * float(totalFrames))
                    goToFrame += startFrame
                    bpy.context.scene.frame_current = goToFrame
                    print(goToFrame)

                    for spline in curve.data.splines:
                        #print(spline.points)
                        # if len(spline.bezier_points) >= 2:
                        spline.use_bezier_u = False
                        spline.use_endpoint_u = True
                        #spline.use_cyclic_u = False

                        aniInterpolation = mifthTools.curveAniInterpolation

                        allPoints = None
                        if spline.type == 'BEZIER':
                            allPoints = spline.bezier_points
                        else:
                            allPoints = spline.points

                        splineSize = len(allPoints)
                        iInterpolation = aniPos-aniInterpolation

                        for i in range(splineSize):
                            point = allPoints[i]
                            iPlace = float(i+1)/float(splineSize)

                            if iPlace >= aniPos and goToFrame != endFrame:
                                point.radius = 0.0

                            elif iPlace < aniPos and iPlace > iInterpolation and goToFrame != endFrame and goToFrame != startFrame:
                                additionalInterpolation = 1.0 - ((iPlace - iInterpolation)/aniInterpolation)
                                point.radius *= additionalInterpolation
                                #print(additionalInterpolation)

                            point.keyframe_insert(data_path="radius", frame=goToFrame)

        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
