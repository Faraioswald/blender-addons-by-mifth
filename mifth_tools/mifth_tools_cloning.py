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
from bpy_extras import view3d_utils

import math
import mathutils
import random

bpy.mifthTools = dict()

prevClonePos = None

class MFTDrawClones(bpy.types.Operator):
    bl_idname = "mft.draw_clones"
    bl_label = "Draw Clones"
    bl_description = "Draw Clones with Mouse"
    bl_options = {'REGISTER', 'UNDO'}


    def modal(self, context, event):
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            # allow navigation
            return {'PASS_THROUGH'}
        elif event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            mft_pick_and_clone(context, event)
            return {'RUNNING_MODAL'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        mifthTools = bpy.context.scene.mifthTools

        if mifthTools.drawForClonesObj == "":
            self.report({'WARNING'}, "Pick Object to Clone")
            return {'CANCELLED'}

        if context.space_data.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}


class MFTPickObjToDrawClone(bpy.types.Operator):
    bl_idname = "mft.pick_obj_to_clone_draw"
    bl_label = "Pick"
    bl_description = "Pick To Clone"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mifthTools = context.scene.mifthTools

        if len(context.selected_objects) > 0:
            mifthTools.drawForClonesObj = context.selected_objects[0].name

        return {'FINISHED'}


def mft_pick_and_clone(context, event, ray_max=1000.0):
    """Run this function on left mouse, execute the ray cast"""
    # get the context arguments
    scene = context.scene
    region = context.region
    rv3d = context.region_data
    coord = event.mouse_region_x, event.mouse_region_y

    # get the ray from the viewport and mouse
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

    if rv3d.view_perspective == 'ORTHO':
        # move ortho origin back
        ray_origin = ray_origin - (view_vector * (ray_max / 2.0))

    ray_target = ray_origin + (view_vector * ray_max)


    def mft_selected_objects_and_duplis():
        """Loop over (object, matrix) pairs (mesh only)"""

        for obj in context.selected_objects:
            if obj.type == 'MESH':
                yield (obj, obj.matrix_world.copy())

            if obj.dupli_type != 'NONE':
                obj.dupli_list_create(scene)
                for dob in obj.dupli_list:
                    obj_dupli = dob.object
                    if obj_dupli.type == 'MESH':
                        yield (obj_dupli, dob.matrix.copy())

            obj.dupli_list_clear()


    def mft_obj_ray_cast(obj, matrix):
        """Wrapper for ray casting that moves the ray into object space"""

        # get the ray relative to the object
        matrix_inv = matrix.inverted()
        ray_origin_obj = matrix_inv * ray_origin
        ray_target_obj = matrix_inv * ray_target

        # cast the ray
        hit, normal, face_index = obj.ray_cast(ray_origin_obj, ray_target_obj)

        if face_index != -1:
            return hit, normal, face_index
        else:
            return None, None, None


    # cast rays and find the closest object
    best_length_squared = ray_max * ray_max
    best_obj = None

    mifthTools = bpy.context.scene.mifthTools

    for obj, matrix in mft_selected_objects_and_duplis():
        if obj.type == 'MESH':
            hit, normal, face_index = mft_obj_ray_cast(obj, matrix)

            if hit is not None:
                hit_world = matrix * hit

                length_squared = (hit_world - ray_origin).length_squared

                if length_squared < best_length_squared:
                    best_length_squared = length_squared
                    best_obj = obj
                    best_obj_pos = hit_world
                    best_obj_nor = normal.normalized()
                    # scene.cursor_location = hit_world

    # now we have the object under the mouse cursor,
    # we could do lots of stuff but for the example just select.
    if best_obj is not None and mifthTools.drawForClonesObj != "":
        selected_Obj_True = context.selected_objects
        obj_Active_True = context.scene.objects.active
        bpy.ops.object.select_all(action='DESELECT')

        objToClone = bpy.data.objects.get(mifthTools.drawForClonesObj)
        objToClone.select = True
        context.scene.objects.active = objToClone

        bpy.ops.object.duplicate(linked=True, mode='DUMMY')
        newDup = bpy.context.selected_objects[0]
        newDup.location = best_obj_pos

        xyNor = best_obj_nor.copy()
        xyNor.z = 0.0

        if xyNor.length == 0:
            rotatePlaneAngle = math.radians(90.0)
            if best_obj_nor.z > 0:
                bpy.ops.transform.rotate(value=-rotatePlaneAngle, axis=(1.0, 0.0, 0.0))
            else:
                bpy.ops.transform.rotate(value=rotatePlaneAngle, axis=(1.0, 0.0, 0.0))
        else:
            xyNor = xyNor.normalized()

            if mifthTools.drawClonesRadialRotate is True:
                #xyRot = ((best_obj_pos.copy() + xyNor) - best_obj_pos.copy()).normalized()
                xyAngleRotate = mathutils.Vector((0.0, -1.0, 0.0)).angle(xyNor)
                #print(xyAngleRotate)
                if xyNor.x < 0:
                    xyAngleRotate = -xyAngleRotate
                xyRotateAxis = mathutils.Vector((0.0, 0.0, 1.0))
                bpy.ops.transform.rotate(value=xyAngleRotate, axis=(0.0, 0.0, 1.0))

            if mifthTools.drawClonesNormalRotate is True:
                # Other rotate
                
                xRotateAxis = xyNor.cross(best_obj_nor).normalized()
                angleRotate = xyNor.angle(best_obj_nor)
                
                if mifthTools.drawClonesRadialRotate is False:
                    newDupMatrix = newDup.matrix_world
                    #activeObjMatrix = objToClone.matrix_world

                    #newDupZAxisTuple = (newDupMatrix[0][2], newDupMatrix[1][2], newDupMatrix[2][2])
                    #newDupZAxis = mathutils.Vector(newDupZAxisTuple).normalized()

                    newDupYAxisTuple = (newDupMatrix[0][1], newDupMatrix[1][1], newDupMatrix[2][1])
                    newDupYAxis = mathutils.Vector(newDupYAxisTuple).normalized()
                    newDupYAxis.x = -newDupYAxis.x
                    newDupYAxis.y = -newDupYAxis.y
                    newDupYAxis.z = -newDupYAxis.z

                    xRotateAxis = newDupYAxis.cross(best_obj_nor).normalized()
                    angleRotate = newDupYAxis.angle(best_obj_nor)
                    #if newDupZAxis.angle(best_obj_nor) > math.radians(90.0):
                        #angleRotate = -angleRotate

                bpy.ops.transform.rotate(value=angleRotate, axis=( (xRotateAxis.x, xRotateAxis.y, xRotateAxis.z) ))

        global prevClonePos

        if mifthTools.drawClonesDirectionRotate is True and prevClonePos is not None:
            newDirRotLookAtt = (best_obj_pos - prevClonePos).normalized()

            newDupMatrix2 = newDup.matrix_world
            newDupZAxisTuple2 = (newDupMatrix2[0][2], newDupMatrix2[1][2], newDupMatrix2[2][2])
            newDupZAxis2 = (mathutils.Vector(newDupZAxisTuple2)).normalized()

            #newDupXAxisTuple2 = (newDupMatrix2[0][0], newDupMatrix2[1][0], newDupMatrix2[2][0])
            #newDupZAxis2.x = -newDupZAxis2.x
            #newDupZAxis2.y = -newDupZAxis2.y
            #newDupZAxis2.z = -newDupZAxis2.z

            #newDupXAxis2 = (mathutils.Vector(newDupXAxisTuple2)).normalized()

            newDirRotVec2 = ( newDirRotLookAtt.cross(newDupZAxis2) ).normalized()

            newDirRotAngle = newDirRotLookAtt.angle(newDupZAxis2)
            #if newDupXAxis2.angle(newDirRotLookAtt) > math.radians(90.0):
                #newDirRotAngle = -newDirRotAngle

            newDirRotAngle = -newDirRotAngle # As we do it in negative axis

            print(newDirRotLookAtt.angle(newDupZAxis2))

            # Main rotation
            bpy.ops.transform.rotate(value= newDirRotAngle, axis=( (newDirRotVec2.x, newDirRotVec2.y, newDirRotVec2.z) ))

            # Fix Rotation
            newDupMatrix2 = newDup.matrix_world  # Do it Again with new Rotation
            newDupZAxisTuple2 = (newDupMatrix2[0][1], newDupMatrix2[1][1], newDupMatrix2[2][1])
            newDupZAxis2 = (mathutils.Vector(newDupZAxisTuple2)).normalized()
            newDupZAxis2.x = -newDupZAxis2.x
            newDupZAxis2.y = -newDupZAxis2.y
            newDupZAxis2.z = -newDupZAxis2.z

            fixDirRotAngle = newDupZAxis2.angle(best_obj_nor)
            fixDirRotAxis = (newDupZAxis2.cross(best_obj_nor) ).normalized()

            bpy.ops.transform.rotate(value= fixDirRotAngle, axis=( (fixDirRotAxis.x, fixDirRotAxis.y, fixDirRotAxis.z) ))

            # temp fix
            if newDirRotLookAtt.angle(newDupZAxis2) < math.radians(90.0) and newDirRotAngle < math.radians(-90.0):
                bpy.ops.transform.rotate(value= math.radians(-45.0), axis=( (best_obj_nor.x, best_obj_nor.y, best_obj_nor.z) ))

        #print(prevClonePos)
        prevClonePos = best_obj_pos.copy()  # set PreviousClone position
            
        if mifthTools.randNormalClone > 0.0:
            randNorAngle = random.uniform(math.radians(-180.0), math.radians(180.0)) * mifthTools.randNormalClone
            randNorAxis = (best_obj_nor.x, best_obj_nor.y, best_obj_nor.z)
            if mifthTools.drawClonesRadialRotate is False and mifthTools.drawClonesNormalRotate is False:
                randNorAxis = (0.0, 0.0, 1.0)
            bpy.ops.transform.rotate(value=randNorAngle, axis=( randNorAxis ))

        if mifthTools.randScaleClone > 0.0:
            randScaleClone = 1.0 - (random.uniform(0.0, 0.99) * mifthTools.randScaleClone)
            bpy.ops.transform.resize(value=(randScaleClone, randScaleClone, randScaleClone), constraint_axis=(False, False, False), constraint_orientation='GLOBAL')

        bpy.ops.object.select_all(action='DESELECT')

        for obj in selected_Obj_True:
            obj.select = True
        context.scene.objects.active = obj_Active_True

        #best_obj.select = True
        #context.scene.objects.active = best_obj


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
