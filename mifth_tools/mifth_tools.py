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


bpy.mifthTools = dict()


class MFTPanel(bpy.types.Panel):
    bl_label = "Base"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_category = 'Mifth'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        allObjects = context.scene.objects
        mifthTools = bpy.context.scene.mifthTools

        # GUI
        row = layout.row()
        #row.label(text="Import/Export Objects")
        #row = layout.row()
        #row.prop(mifthTools, "type", text="")
        #row = layout.row()

        row.operator("mft.clonetoselected", text="CloneToSelected")



#class MFTPreferences(AddonPreferences):
    ## this must match the addon name, use '__package__'
    ## when defining this in a submodule of a python package.
    ## bl_idname = __name__
    #bl_idname = __package__

    #exchangedir = StringProperty(
        #name="ExchangeFolder",
        #subtype="DIR_PATH",
        #default="",
    #)

    #def draw(self, context):
        #layout = self.layout
        #row = layout.row()
        #row.label(text="Please, set Exchanges Folder and save Preferences")
        #row = layout.row()
        #row.prop(self, "exchangedir")


class MFTCloneToSelected(bpy.types.Operator):
    bl_idname = "mft.clonetoselected"
    bl_label = "Clone To Selected"
    bl_description = "Clone To Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):

        dubOrig = bpy.context.scene.objects.active
        objectsToClone = []

        for obj1 in bpy.context.selected_objects:
            objectsToClone.append(obj1)

        for obj2 in objectsToClone:
            bpy.ops.object.select_all(action='DESELECT')
            dubOrig.select = True

            bpy.ops.object.duplicate(linked=True, mode='DUMMY')
            newDup = bpy.context.selected_objects[0]
            print(newDup)
            newDup.location = obj2.location
            newDup.rotation_euler = obj2.rotation_euler
            newDup.scale = obj2.scale

        bpy.ops.object.select_all(action='DESELECT')
        for obj3 in objectsToClone:
            obj3.select = True
        bpy.ops.object.delete(use_global=False)
        
        objectsToClone = None

        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
