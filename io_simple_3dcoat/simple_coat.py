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
import os
import shutil


bpy.simple3Dcoat = dict()
bpy.simple3Dcoat['active_coat'] = ''
bpy.simple3Dcoat['status'] = 0


class MainPanel3DCoat(bpy.types.Panel):
    bl_label = "Simple3DCoat Applink"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        me = context.scene.objects
        mat_list = []
        import_no = 0
        coat = bpy.simple3Dcoat
        simple3Dcoat = bpy.context.scene.simple3Dcoat

        # GUI
        row = layout.row()
        row.label(text="Import/Export Objects")
        row = layout.row()
        row.prop(simple3Dcoat, "type", text="")
        row = layout.row()

        colL = row.column()
        colR = row.column()

        colR.operator("export_applink.simple_3d_coat", text="ExportObjects")
        colL.operator("import_applink.simple_3d_coat", text="ImportObjects")

        row = layout.row()
        row.prop(simple3Dcoat, "doApplyModifiers", text="Apply Modifiers")
        row = layout.row()
        row.prop(simple3Dcoat, "exportMaterials", text="Export Materials")
        row = layout.row()
        row = layout.row()
        row.label(text="Copy Textures")
        row = layout.row()
        row.prop(simple3Dcoat, "copyTexturesPath", text="")
        #row = layout.row()
        #row.operator("copytextures.simple_3d_coat", text="Copy Textures to a Path")
        row = layout.row()
        row = layout.row()
        row.operator("clearexchange.simple_3d_coat", text="Clear Exchange Folder")


class Coat3DAddonPreferences(AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    # bl_idname = __name__
    bl_idname = __package__

    exchangedir = StringProperty(
        name="ExchangeFolder",
        subtype="DIR_PATH",
        default="",
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Please, set Exchanges Folder and save Preferences")
        row = layout.row()
        row.prop(self, "exchangedir")


class ExportScene3DCoat(bpy.types.Operator):
    bl_idname = "export_applink.simple_3d_coat"
    bl_label = "Export your custom property"
    bl_description = "Export your custom property"
    bl_options = {'UNDO'}

    def invoke(self, context, event):
        # Addon Preferences
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__package__].preferences

        #checkname = ''
        simple3Dcoat = bpy.context.scene.simple3Dcoat
        #scene = context.scene

        if len(bpy.context.selected_objects) > 0 and os.path.isdir(addon_prefs.exchangedir):
            importfile = addon_prefs.exchangedir
            importfile += ('%simport.txt' % (os.sep))

            # Paths for export/import
            blenderExportName = "export"
            blenderImportName = "import"

            # create Simple3DCoat directory
            simple3DCoatDir = addon_prefs.exchangedir + "BlenderSimple3DCoat" + os.sep
            if not(os.path.isdir(simple3DCoatDir)):
                os.makedirs(simple3DCoatDir)

            # Export to Obj
            bpy.ops.export_scene.obj(
                filepath=simple3DCoatDir + blenderExportName + '.obj', use_selection=True, use_mesh_modifiers=simple3Dcoat.doApplyModifiers,
                use_blen_objects=True, use_normals=True, use_materials=simple3Dcoat.exportMaterials, keep_vertex_order=True, axis_forward='-Z', axis_up='Y')

            # Save import file
            file = open(importfile, "w")
            file.write("%s" %
                       (simple3DCoatDir + blenderExportName + '.obj'))
            file.write("\n%s" %
                       (simple3DCoatDir + blenderImportName + '.obj'))
            file.write("\n[%s]" % (simple3Dcoat.type))

            # Copy textures to a custom path
            copyToFolder = simple3Dcoat.copyTexturesPath
            if os.path.isdir(copyToFolder):
                file.write("\n[TexOutput:%s]"%(copyToFolder))

            file.close()

        else:
            self.report(
                {'INFO'}, "No Selected Objects or Bad Exchange Folder!!!")

        return {'FINISHED'}


class ImportScene3DCoat(bpy.types.Operator):
    bl_idname = "import_applink.simple_3d_coat"
    bl_label = "import your custom property"
    bl_description = "import your custom property"
    bl_options = {'UNDO'}

    def invoke(self, context, event):
        # Addon Preferences
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__package__].preferences

        #scene = context.scene
        simple3Dcoat = bpy.context.scene.simple3Dcoat
        #coat = bpy.simple3Dcoat

        exchangeFile = addon_prefs.exchangedir
        exchangeFile += ('%sexport.txt' % (os.sep))
        simple3DCoatDir = addon_prefs.exchangedir + "BlenderSimple3DCoat" + os.sep
        new_applink_name = None

        if(os.path.isfile(exchangeFile) and os.path.isdir(simple3DCoatDir)):
            obj_pathh = open(exchangeFile)

            for line in obj_pathh:
                new_applink_name = line
                if os.path.isfile(new_applink_name):
                    bpy.ops.import_scene.obj(filepath=new_applink_name, axis_forward='-Z', axis_up='Y', use_image_search=False)
                else:
                    self.report({'INFO'}, "No Imported Objects!!!")
                break
            obj_pathh.close()
        else:
            self.report({'INFO'}, "No Imported Objects or Bad Exchange Folder!!!")

        return {'FINISHED'}


#class CopyTextures3DCoat(bpy.types.Operator):
    #bl_idname = "copytextures.simple_3d_coat"
    #bl_label = "Copy Textures"
    #bl_description = "Copy Textures To a Custom Folder"

    #def invoke(self, context, event):
        ## Addon Preferences
        #user_preferences = context.user_preferences
        #addon_prefs = user_preferences.addons[__package__].preferences

        #simple3Dcoat = bpy.context.scene.simple3Dcoat
        #texturesFile = addon_prefs.exchangedir
        #texturesFile += ('%stextures.txt' % (os.sep))
        #simple3DCoatDir = addon_prefs.exchangedir + "BlenderSimple3DCoat" + os.sep
        #copyToFolder = simple3Dcoat.copyTexturesPath

        #if os.path.isdir(copyToFolder) and os.path.isfile(texturesFile) and os.path.isdir(simple3DCoatDir):
            #tex_file = open(texturesFile)
            #for line in tex_file:
                #if line.find(addon_prefs.exchangedir) >= 0:
                    #lineFixed = line.replace("\n", "");
                    #if os.path.isfile(lineFixed):
                        #shutil.copy2(lineFixed, copyToFolder)
                    #else:
                        #self.report({'INFO'}, "Texture does not exist!!")

            #tex_file.close()
        #else:
            #self.report({'INFO'}, "Folder does not exist!!")

        #return {'FINISHED'}


class ClearExchangeFolder(bpy.types.Operator):
    bl_idname = "clearexchange.simple_3d_coat"
    bl_label = "Clear Exchange Folder"
    bl_description = "Clear Exchange Folder.."

    def invoke(self, context, event):
        # Addon Preferences
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__package__].preferences
        simple3DCoatDir = addon_prefs.exchangedir + "BlenderSimple3DCoat" + os.sep

        # Remove BlenderSimple3DCoat Folder
        if os.path.isdir(simple3DCoatDir):
            shutil.rmtree(simple3DCoatDir)

        return {'FINISHED'}

    
def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
