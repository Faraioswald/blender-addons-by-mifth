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
        
#def set_working_folders():
    #platform = os.sys.platform
    #simple3Dcoat = bpy.context.scene.simple3Dcoat
    #if(platform == 'win32'):
        #folder_objects = os.path.expanduser("~") + os.sep + 'Documents' + os.sep + '3DC2Blender' + os.sep + 'Objects'
        #folder_textures = os.path.expanduser("~") + os.sep + 'Documents' + os.sep + '3DC2Blender' + os.sep + 'Textures' + os.sep
        #if(not(os.path.isdir(folder_objects))):
            #os.makedirs(folder_objects)
        #if(not(os.path.isdir(folder_textures))):
            #os.makedirs(folder_textures)       
    #else:
        #folder_objects = os.path.expanduser("~") + os.sep + '3DC2Blender' + os.sep + 'Objects'
        #folder_textures = os.path.expanduser("~") + os.sep + '3DC2Blender' + os.sep + 'Textures' + os.sep
        #if(not(os.path.isdir(folder_objects))):
            #os.makedirs(folder_objects)
        #if(not(os.path.isdir(folder_textures))):
            #os.makedirs(folder_textures)
            
                
    #return folder_objects,folder_textures

#class SimpleCoatPanel():
    #bl_space_type = 'PROPERTIES'
    #bl_region_type = 'WINDOW'
    #bl_context = "object"

class MainPanel(bpy.types.Panel):
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

        colR.operator("export_applink.simple_3d_coat", text="Transfer")
        colL.operator("import_applink.simple_3d_coat", text="Update")

        row = layout.row()
        row.prop(simple3Dcoat,"exchangedir",text="ExchangeFolder")
            

           

                    
            
            
              



class ExportScene(bpy.types.Operator):
    bl_idname = "export_applink.simple_3d_coat"
    bl_label = "Export your custom property"
    bl_description = "Export your custom property"
    bl_options = {'UNDO'}

    def invoke(self, context, event):
        checkname = ''
        simple3Dcoat = bpy.context.scene.simple3Dcoat
        scene = context.scene
        activeobj = bpy.context.active_object.name
        obj = scene.objects[activeobj]
        #coa = bpy.context.scene.objects.active.simple3Dcoat
        #simple3Dcoat.exchangedir = set_exchange_folder()
        export_ok = False

        #folder_objects,folder_textures = set_working_folders()

        #if(simple3Dcoat.exchange_found == False):
            #return {'FINISHED'}

        #if(bpy.context.selected_objects == []):
            #return {'FINISHED'}
        #else:
            #for objec in bpy.context.selected_objects:
                #if objec.type == 'MESH':
                    #export_ok = True
            #if(export_ok == False):
                #return {'FINISHED'}

        importfile = simple3Dcoat.exchangedir
        #texturefile = simple3Dcoat.exchangedir
        importfile += ('%simport.txt'%(os.sep))
        #texturefile += ('%stextures.txt'%(os.sep))

        #looking = True
        #object_index = 0
        #if(coa.applink_name and os.path.isfile(coa.applink_name)):
            #checkname = coa.applink_name
           
        #else:
            #while(looking == True):
                #checkname = folder_objects + os.sep + activeobj
                #checkname = ("%s%.2d.obj"%(checkname,object_index))
                #if(os.path.isfile(checkname)):
                    #object_index += 1
                #else:
                    #looking = False
                    #coa.applink_name = checkname


        #simple3Dcoat.cursor_loc = obj.location
        #simple3Dcoat.cursor_orginal = bpy.context.scene.cursor_location

        

        #coa.loc = obj.location
        #coa.rot = obj.rotation_euler
        #coa.sca = obj.scale
        #coa.dime = obj.dimensions

        #obj.location = (0,0,0)
        #obj.rotation_euler = (0,0,0)
        #bpy.ops.object.transform_apply(scale=True)
        
        bpy.ops.export_scene.obj(filepath=simple3Dcoat.exchangedir + activeobj + '.obj', use_selection=True,
        use_mesh_modifiers=False,use_blen_objects=True, use_materials = True,
        keep_vertex_order = True,axis_forward='-Z',axis_up='Y')
        
        #obj.location = coa.loc
        #obj.rotation_euler = coa.rot
        

        #bpy.context.scene.cursor_location = simple3Dcoat.cursor_loc
        #bpy.context.scene.cursor_location = simple3Dcoat.cursor_orginal
        
        file = open(importfile, "w")
        file.write("%s"%(simple3Dcoat.exchangedir + activeobj + '.obj'))
        file.write("\n%s"%(simple3Dcoat.exchangedir + activeobj + '.obj'))
        file.write("\n[%s]"%(simple3Dcoat.type))
        #file.write("\n[TexOutput:%s]"%(folder_textures))
        file.close()

        #coa.objecttime = str(os.path.getmtime(coa.applink_name))
        
        
               
        return {'FINISHED'}

class ImportScene(bpy.types.Operator):
    bl_idname = "import_applink.simple_3d_coat"
    bl_label = "import your custom property"
    bl_description = "import your custom property"
    bl_options = {'UNDO'}
    
    def invoke(self, context, event):
        scene = context.scene
        simple3Dcoat = bpy.context.scene.simple3Dcoat
        coat = bpy.simple3Dcoat
        #test = bpy.context.selected_objects
        #act_first = bpy.context.scene.objects.active
        #bpy.context.scene.game_settings.material_mode = 'GLSL'
        #simple3Dcoat.exchangedir = set_exchange_folder()

        #folder_objects,folder_textures = set_working_folders()

        #Blender_folder = ("%s%sBlender"%(simple3Dcoat.exchangedir,os.sep))
        exchangeFolder = simple3Dcoat.exchangedir
        #path3b_now = simple3Dcoat.exchangedir
        #path3b_now += ('last_saved_3b_file.txt')
        exchangeFolder += ('%sexport.txt'%(os.sep))
        new_applink_name = None
        #new_object = False
        if(os.path.isfile(exchangeFolder)):
            obj_pathh = open(exchangeFolder)
            #new_object = True
            for line in obj_pathh:
                new_applink_name = line
                break
            obj_pathh.close()

            #for scene_objects in bpy.context.scene.objects:
                #if(scene_objects.type == 'MESH'):
                    #if(scene_objects.simple3Dcoat.applink_name == new_applink_name):
                        #new_object = False

        #for act_name in test:
            #coa = act_name.simple3Dcoat
            #path_object = coa.applink_name
            #if act_name.type == 'MESH' and os.path.isfile(path_object):
                #multires_on = False
                #activeobj = act_name.name
                #mat_list = []
                #scene.objects[activeobj].select = True
                #objekti = scene.objects[activeobj]
                #simple3Dcoat.loca = objekti.location
                #simple3Dcoat.rota = objekti.rotation_euler
                #simple3Dcoat.dime = objekti.scale
                

                
                ##See if there is multres modifier. 
                #for modifiers in objekti.modifiers:
                    #if modifiers.type == 'MULTIRES' and (modifiers.total_levels > 0):
                        #if(not(simple3Dcoat.importlevel)):
                            #bpy.ops.object.multires_external_pack()
                            #multires = simple3Dcoat.exchangedir
                            #multires += ('%stemp.btx'%(os.sep))
                            #bpy.ops.object.multires_external_save(filepath=multires)
                            ##bpy.ops.object.multires_external_pack()
                        #multires_on = True
                        #multires_name = modifiers.name
                        #break
                        
                #exportfile = simple3Dcoat.exchangedir
                #path3b_n = simple3Dcoat.exchangedir
                #path3b_n += ('last_saved_3b_file.txt')
                #exportfile += ('%sexport.txt'%(os.sep))
                #if(os.path.isfile(exportfile)):
                    #export_file = open(exportfile)
                    #for line in export_file:
                        #if line.rfind('.3b'):
                            #objekti.simple3Dcoat.coatpath = line
                            #coat['active_coat'] = line
                    #export_file.close()
                    #os.remove(exportfile)

                #if(len(objekti.material_slots) == 0):
                    #delete_material = False
                #else:
                    #delete_material = True
                    
               
                #if(not(objekti.active_material) and objekti.material_slots):
                    #act_mat_index = objekti.active_material_index
                    #materials_old = bpy.data.materials.keys()
                    #bpy.ops.material.new()
                    #materials_new = bpy.data.materials.keys()
                    #new_ma = list(set(materials_new).difference(set(materials_old)))
                    #new_mat = new_ma[0]
                    #ki = bpy.data.materials[new_mat]
                    #objekti.material_slots[act_mat_index].material = ki
                 

                 
                #if(os.path.isfile(path_object) and (coa.objecttime != str(os.path.getmtime(path_object)))):

                    #if(objekti.material_slots):
                        #act_mat_index = objekti.active_material_index
                        #for obj_mat in objekti.material_slots:
                            #mat_list.append(obj_mat.material)
                            
                    #coa.dime = objekti.dimensions
                    #coa.objecttime = str(os.path.getmtime(path_object))
                    #mtl = coa.applink_name
                    #mtl = mtl.replace('.obj','.mtl')
                    #if(os.path.isfile(mtl)):
                        #os.remove(mtl)
                   
        bpy.ops.import_scene.obj(filepath=new_applink_name, axis_forward='-Z',axis_up='Y',use_image_search=False)
        obj_proxy = scene.objects[0]
        bpy.ops.object.select_all(action='TOGGLE')
        obj_proxy.select = True
            
                        
                    #bpy.ops.object.transform_apply(rotation=True)
                    #proxy_mat = obj_proxy.material_slots[0].material
                    #if(delete_material):
                        #while(list(obj_proxy.data.materials) != []):
                            #proxy_mat = obj_proxy.material_slots[0].material
                            #obj_proxy.data.materials.pop(0,1)
                            #proxy_mat.user_clear()
                            #bpy.data.materials.remove(proxy_mat)
                    #bpy.ops.object.select_all(action='TOGGLE')

                    #if(simple3Dcoat.importlevel):
                        #obj_proxy.select = True
                        #obj_proxy.modifiers.new(name='temp',type='MULTIRES')
                        #objekti.select = True
                        #bpy.ops.object.multires_reshape(modifier=multires_name)
                        #bpy.ops.object.select_all(action='TOGGLE')
                        #multires_on = False
                    #else:
                    
                        #scene.objects.active = obj_proxy
                    
                        #obj_data = objekti.data.id_data
                        #objekti.data = obj_proxy.data.id_data
                        #if(bpy.data.meshes[obj_data.name].users == 0):
                            #objekti.data.id_data.name = obj_data.name
                            #bpy.data.meshes.remove(obj_data)
                            

                    #obj_proxy.select = True
                    #bpy.ops.object.delete()
                    #objekti.select = True
                    #objekti.scale = simple3Dcoat.dime
                    
                    #bpy.context.scene.objects.active = objekti

                #if(os.path.isfile(path3b_n)):
                    #path3b_fil = open(path3b_n)
                    #for lin in path3b_fil:
                        #objekti.simple3Dcoat.path3b = lin
                    #path3b_fil.close()
                    #os.remove(path3b_n)
                        
                #if(simple3Dcoat.importmesh and not(os.path.isfile(path_object))):
                    #simple3Dcoat.importmesh = False

                #if(mat_list and simple3Dcoat.importmesh):
                    #for mat_one in mat_list:
                        #objekti.data.materials.append(mat_one)
                    #objekti.active_material_index = act_mat_index
                    
                #if(mat_list):
                    #for obj_mate in objekti.material_slots:
                        #if(hasattr(obj_mate.material,'texture_slots')):
                            #for tex_slot in obj_mate.material.texture_slots:
                                #if(hasattr(tex_slot,'texture')):
                                    #if(tex_slot.texture.type == 'IMAGE'):
                                        #if tex_slot.texture.image is not None:
                                            #tex_slot.texture.image.reload()
                                                                
                        
                #if(simple3Dcoat.importtextures):
                    #export = ''
                    #tex.gettex(mat_list,objekti,scene,export)

                #if(multires_on):
                    #temp_file = simple3Dcoat.exchangedir
                    #temp_file += ('%stemp2.btx'%(os.sep))
                    #if(objekti.modifiers[multires_name].levels == 0):
                        #objekti.modifiers[multires_name].levels = 1
                        #bpy.ops.object.multires_external_save(filepath=temp_file)
                        #objekti.modifiers[multires_name].filepath = multires
                        #objekti.modifiers[multires_name].levels = 0

                    #else:
                        #bpy.ops.object.multires_external_save(filepath=temp_file)
                        #objekti.modifiers[multires_name].filepath = multires
                    ##bpy.ops.object.multires_external_pack()
                #bpy.ops.object.shade_smooth()
                
              
        #for act_name in test:
            #act_name.select = True
        #bpy.context.scene.objects.active = act_first

        #if(new_object == True):
            #simple3Dcoat = bpy.context.scene.simple3Dcoat
            #scene = context.scene
            
            #Blender_folder = ("%s%sBlender"%(simple3Dcoat.exchangedir,os.sep))
            #Blender_export = Blender_folder
            #path3b_now = simple3Dcoat.exchangedir
            #path3b_now += ('last_saved_3b_file.txt')
            #Blender_export += ('%sexport.txt'%(os.sep))

       
            #mat_list = []
            #obj_path =''

         
            #export = new_applink_name
            #mod_time = os.path.getmtime(new_applink_name)
            #mtl_list = new_applink_name.replace('.obj','.mtl')
            #if(os.path.isfile(mtl_list)):
                #os.remove(mtl_list)
                
            #bpy.ops.import_scene.obj(filepath=new_applink_name,axis_forward='-Z',axis_up='Y')
            #bpy.ops.object.transform_apply(rotation=True)
            #new_obj = scene.objects[0]
            #new_obj.simple3Dcoat.applink_name = obj_path
            #scene.objects[0].simple3Dcoat.applink_name = export #objectdir muutettava
                
            #os.remove(Blender_export)
            
            #bpy.context.scene.objects.active = new_obj

            #bpy.ops.object.shade_smooth()
           
            #Blender_tex = ("%s%stextures.txt"%(simple3Dcoat.exchangedir,os.sep))
            #mat_list.append(new_obj.material_slots[0].material)
            #tex.gettex(mat_list, new_obj, scene,export)

        return {'FINISHED'}



#from bpy import *
#from mathutils import Vector, Matrix

## 3D-Coat Dynamic Menu
#class VIEW3D_MT_Coat_Dynamic_Menu(bpy.types.Menu):
    #bl_label = "3D-Coat Applink Menu"

    #def draw(self, context):
        #layout = self.layout
        #settings = context.tool_settings
        #layout.operator_context = 'INVOKE_REGION_WIN'
        #simple3Dcoat = bpy.context.scene.simple3Dcoat
        #Blender_folder = ("%s%sBlender"%(simple3Dcoat.exchangedir,os.sep))
        #Blender_export = Blender_folder
        #Blender_export += ('%sexport.txt'%(os.sep))

        #ob = context
        #if ob.mode == 'OBJECT':
            #if(bpy.context.selected_objects):
                #for ind_obj in bpy.context.selected_objects:
                    #if(ind_obj.type == 'MESH'):
                        #layout.active = True
                        #break
                    #layout.active = False

                #if(layout.active == True):

                    #layout.operator("import_applink.simple_3d_coat", text="Import")
                    #layout.separator()

                    #layout.operator("export_applink.simple_3d_coat", text="Export")
                    #layout.separator()

                    #layout.menu("VIEW3D_MT_ImportMenu")
                    #layout.separator()

                    #layout.menu("VIEW3D_MT_ExportMenu")
                    #layout.separator()

                    #layout.menu("VIEW3D_MT_ExtraMenu")
                    #layout.separator()

                    #if(len(bpy.context.selected_objects) == 1):
                        #if(os.path.isfile(bpy.context.selected_objects[0].simple3Dcoat.path3b)):
                            #layout.operator("import_applink.simple_3d_coat_3b", text="Load 3b")
                            #layout.separator()

                    #if(os.path.isfile(Blender_export)):

                        #layout.operator("import3b_applink.simple_3d_coat", text="Bring from 3D-Coat")
                        #layout.separator()
                #else:
                    #if(os.path.isfile(Blender_export)):
                        #layout.active = True

                        #layout.operator("import3b_applink.simple_3d_coat", text="Bring from 3D-Coat")
                        #layout.separator()
            #else:
                 #if(os.path.isfile(Blender_export)):
                    

                    #layout.operator("import3b_applink.simple_3d_coat", text="Bring from 3D-Coat")
                    #layout.separator()
                
#class VIEW3D_MT_ImportMenu(bpy.types.Menu):
    #bl_label = "Import Settings"

    #def draw(self, context):
        #layout = self.layout
        #simple3Dcoat = bpy.context.scene.simple3Dcoat
        #settings = context.tool_settings
        #layout.operator_context = 'INVOKE_REGION_WIN'
        #layout.prop(simple3Dcoat,"importmesh")
        #layout.prop(simple3Dcoat,"importmod")
        #layout.prop(simple3Dcoat,"smooth_on")
        #layout.prop(simple3Dcoat,"importtextures")
        
#class VIEW3D_MT_ExportMenu(bpy.types.Menu):
    #bl_label = "Export Settings"

    #def draw(self, context):
        #layout = self.layout
        #simple3Dcoat = bpy.context.scene.simple3Dcoat
        #settings = context.tool_settings
        #layout.operator_context = 'INVOKE_REGION_WIN'
        #layout.prop(simple3Dcoat,"exportover")
        #if(simple3Dcoat.exportover):
           #layout.prop(simple3Dcoat,"exportmod")

#class VIEW3D_MT_ExtraMenu(bpy.types.Menu):
    #bl_label = "Extra"

    #def draw(self, context):
        #layout = self.layout
        #simple3Dcoat = bpy.context.scene.simple3Dcoat
        #settings = context.tool_settings
        #layout.operator_context = 'INVOKE_REGION_WIN'

        #layout.operator("import_applink.pilgway_3d_deltex",text="Delete all Textures")
        #layout.separator()

def register():
    bpy.utils.register_module(__name__)

    wm = bpy.context.window_manager
    #km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    #kmi = km.keymap_items.new('wm.call_menu2', 'Q', 'PRESS')
    #kmi.properties.name = "VIEW3D_MT_Coat_Dynamic_Menu"

def unregister():
    bpy.utils.unregister_module(__name__)

    wm = bpy.context.window_manager
    #km = wm.keyconfigs.addon.keymaps['3D View']
    #for kmi in km.keymap_items:
        #if kmi.idname == '':
            #if kmi.properties.name == "VIEW3D_MT_Coat_Dynamic_Menu":
                #km.keymap_items.remove(kmi)
                #break


if __name__ == "__main__":
    register()
