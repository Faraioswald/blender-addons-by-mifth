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
#from io_simple3Dcoat import tex
import os


bpy.simple3Dcoat = dict()
bpy.simple3Dcoat['active_coat'] = ''
bpy.simple3Dcoat['status'] = 0
#def set_exchange_folder():
    #platform = os.sys.platform
    #simple3Dcoat = bpy.context.scene.simple3Dcoat
    #Blender_export = ""


    #if(platform == 'win32'):
        #exchange = os.path.expanduser("~") + os.sep + 'Documents' + os.sep + '3D-CoatV4' + os.sep +'Exchange'
        #if not(os.path.isdir(exchange)):
            #exchange = os.path.expanduser("~") + os.sep + 'Documents' + os.sep + '3D-CoatV3' + os.sep +'Exchange'
    #else:
        #exchange = os.path.expanduser("~") + os.sep + '3D-CoatV4' + os.sep + 'Exchange'
        #if not(os.path.isdir(exchange)):
            #exchange = os.path.expanduser("~") + os.sep + '3D-CoatV3' + os.sep + 'Exchange'          
    #if(not(os.path.isdir(exchange))):
        #exchange = simple3Dcoat.exchangedir 

    #if(os.path.isdir(exchange)):
        #bpy.simple3Dcoat['status'] = 1
        #if(platform == 'win32'):
            #exchange_path = os.path.expanduser("~") + os.sep + 'Documents' + os.sep + '3DC2Blender' + os.sep + 'Exchange_folder.txt'
            #applink_folder = os.path.expanduser("~") + os.sep + 'Documents' + os.sep + '3DC2Blender'
            #if(not(os.path.isdir(applink_folder))):
                #os.makedirs(applink_folder)
        #else:
            #exchange_path = os.path.expanduser("~") + os.sep + 'Documents' + os.sep + '3DC2Blender' + os.sep + 'Exchange_folder.txt'
            #applink_folder = os.path.expanduser("~") + os.sep + 'Documents' + os.sep + '3DC2Blender'
            #if(not(os.path.isdir(applink_folder))):
                #os.makedirs(applink_folder)
        #file = open(exchange_path, "w")
        #file.write("%s"%(simple3Dcoat.exchangedir))
        #file.close()
        
    #else:
        #if(platform == 'win32'):
            #exchange_path = os.path.expanduser("~") + os.sep + 'Documents' + os.sep + '3DC2Blender' + os.sep + 'Exchange_folder.txt'
        #else:
            #exchange_path = os.path.expanduser("~") + os.sep + '3DC2Blender' + os.sep + 'Exchange_folder.txt'
        #if(os.path.isfile(exchange_path)):
            #ex_path =''

            #ex_pathh = open(exchange_path)
            #for line in ex_pathh:
                #ex_path = line
                #break
            #ex_pathh.close()

            #if(os.path.isdir(ex_path) and ex_path.rfind('Exchange') >= 0):
                #exchange = ex_path
                #bpy.simple3Dcoat['status'] = 1
            #else:
                #bpy.simple3Dcoat['status'] = 0
        #else:
            #bpy.simple3Dcoat['status'] = 0
    #if(bpy.simple3Dcoat['status'] == 1):
        #Blender_folder = ("%s%sBlender"%(exchange,os.sep))
        #Blender_export = Blender_folder
        #path3b_now = exchange
        #path3b_now += ('last_saved_3b_file.txt')
        #Blender_export += ('%sexport.txt'%(os.sep))

        #if(not(os.path.isdir(Blender_folder))):
            #os.makedirs(Blender_folder)
            #Blender_folder = os.path.join(Blender_folder,"run.txt")
            #file = open(Blender_folder, "w")
            #file.close()
    #return exchange


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
        
        #if(bpy.context.scene.objects.active):
            #coa = bpy.context.scene.objects.active.simple3Dcoat

            
        #if(bpy.simple3Dcoat['status'] == 0 and not(os.path.isdir(simple3Dcoat.exchangedir))):
            #bpy.simple3Dcoat['active_coat'] = set_exchange_folder()
            #row = layout.row()
            #row.label(text="Applink didn't find your 3d-Coat/Excahnge folder.")
            #row = layout.row()
            #row.label("Please select it before using Applink.")
            #row = layout.row()
            #row.prop(simple3Dcoat,"exchangedir",text="")
        
        #else:
       
        
        #Here you add your GUI 
        row = layout.row()
        row.prop(simple3Dcoat,"type",text = "")
        row = layout.row()

        colL = row.column()
        colR = row.column()

        colR.operator("export_applink.simple_3d_coat", text="ExportObjects")
        colL.operator("import_applink.simple_3d_coat", text="ImportScene")

        row = layout.row()
        row.prop(simple3Dcoat,"exchangedir",text="ExchangeDir")

        row = layout.row()
        row.prop(simple3Dcoat,"doApplyModifiers",text="Apply Modifiers")


class ExportScene3DCoat(bpy.types.Operator):
    bl_idname = "export_applink.simple_3d_coat"
    bl_label = "Export your custom property"
    bl_description = "Export your custom property"
    bl_options = {'UNDO'}

    def invoke(self, context, event):
        checkname = ''
        simple3Dcoat = bpy.context.scene.simple3Dcoat
        scene = context.scene

        if len(bpy.context.selected_objects) > 0 and os.path.isdir(simple3Dcoat.exchangedir):
            activeobj = bpy.context.active_object.name
            obj = scene.objects[activeobj]

            importfile = simple3Dcoat.exchangedir
            importfile += ('%simport.txt'%(os.sep))

        
            bpy.ops.export_scene.obj(filepath=simple3Dcoat.exchangedir + activeobj + '.obj', use_selection=True,
            use_mesh_modifiers=simple3Dcoat.doApplyModifiers, use_blen_objects=True, use_materials = True,
            keep_vertex_order = True,axis_forward='-Z',axis_up='Y')

            file = open(importfile, "w")
            file.write("%s"%(simple3Dcoat.exchangedir + activeobj + '.obj'))
            file.write("\n%s"%(simple3Dcoat.exchangedir + activeobj + '.obj'))
            file.write("\n[%s]"%(simple3Dcoat.type))
            file.close()

        else:
            self.report({'INFO'}, "No Selected Objects or Bad Exchange Folder!!!")

        return {'FINISHED'}


class ImportScene3DCoat(bpy.types.Operator):
    bl_idname = "import_applink.simple_3d_coat"
    bl_label = "import your custom property"
    bl_description = "import your custom property"
    bl_options = {'UNDO'}
    
    def invoke(self, context, event):
        scene = context.scene
        simple3Dcoat = bpy.context.scene.simple3Dcoat
        coat = bpy.simple3Dcoat

        exchangeFolder = simple3Dcoat.exchangedir
        exchangeFolder += ('%sexport.txt'%(os.sep))
        new_applink_name = None

        if(os.path.isfile(exchangeFolder)):
            obj_pathh = open(exchangeFolder)

            for line in obj_pathh:
                new_applink_name = line
                bpy.ops.import_scene.obj(filepath=new_applink_name, axis_forward='-Z',axis_up='Y',use_image_search=False)
                break
            obj_pathh.close()
        else:
            self.report({'INFO'}, "No Imported Objects or Bad Exchange Folder!!!")

        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
