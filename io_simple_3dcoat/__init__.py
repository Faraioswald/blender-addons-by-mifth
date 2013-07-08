# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Simple 3D-Coat Applink",
    "author": "Kalle-Samuli Riihikoski (haikalle), Paul Geraskin",
    "version": (0, 1, 0),
    "blender": (2, 67, 0),
    "location": "Scene > Simple 3D-Coat Applink",
    "description": "Transfer data between 3D-Coat/Blender",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/" \
        "Scripts/Import-Export/3dcoat_applink",
    "tracker_url": "https://projects.blender.org/tracker/?"\
        "func=detail&aid=24446",
    "category": "Import-Export"}



if "bpy" in locals():
    import imp
    imp.reload(simple_coat)
    #imp.reload(tex)
else:
    from . import simple_coat
    #from . import tex

import bpy
from bpy.props import *

    
def register():
    bpy.simple3Dcoat = dict()
    bpy.simple3Dcoat['active_coat'] = ''
    bpy.simple3Dcoat['status'] = 0
    bpy.simple3Dcoat['kuva'] = 1
    
    class ObjectCoat3D(bpy.types.PropertyGroup):
        objpath = StringProperty(name="Object_Path")
        applink_name = StringProperty(name="Object_Applink_name")
        coatpath = StringProperty(name="Coat_Path")
        objectdir = StringProperty(name="ObjectPath", subtype="FILE_PATH")
        #objecttime = StringProperty(name="ObjectTime", subtype="FILE_PATH")
        #texturefolder = StringProperty(name="Texture folder:", subtype="DIR_PATH")
        path3b = StringProperty(name="3B Path", subtype="FILE_PATH")
        export_on = BoolProperty(name="Export_On", description="Add Modifiers and export",default= False)
        #dime = FloatVectorProperty(name="dime",description="Dimension")
        #loc = FloatVectorProperty(name="Location",description="Location")
        #rot = FloatVectorProperty(name="Rotation",description="Rotation",subtype='EULER')
        #sca = FloatVectorProperty(name="Scale",description="Scale")

    class SimpleSceneCoat3D(bpy.types.PropertyGroup):

        defaultfolder = StringProperty(
            name="FilePath",
            subtype="DIR_PATH",
        )
        cursor_loc = FloatVectorProperty(name="Cursor_loc",description="location")
        
        exchangedir = StringProperty(
            name="FilePath",
            subtype="DIR_PATH"
        )

        exchangefolder = StringProperty(
            name="FilePath",
            subtype="DIR_PATH"
        )

        doApplyModifiers = BoolProperty(
            name="Apply Modifiers",
            description="Apply Modifiers...",
            default= True
        )

        exportMaterials = BoolProperty(
            name="Export Materials",
            description="Export Materials...",
            default= True
        )


        type = EnumProperty( name= "Export Type",
            description= "Different Export Types",
            items=(("ppp",   "Per-Pixel Painting", ""),
                   ("mv",   "Microvertex Painting", ""),
                   ("ptex",   "Ptex Painting", ""),
                   ("uv",   "UV-Mapping", ""),
                   ("ref",  "Reference Mesh", ""),
                   ("retopo",  "Retopo mesh as new layer", ""),
                   ("vox",  "Mesh As Voxel Object", ""),
                   ("alpha",  "Mesh As New Pen Alpha", ""),
                   ("prim",  "Mesh As Voxel Primitive", ""),
                   ("curv", "Mesh As a Curve Profile", ""),
                   ("autopo",  "Mesh For Auto-retopology", ""),
                   ),
            default= "ppp"
        )

    bpy.utils.register_module(__name__)

    bpy.types.Object.simple3Dcoat= PointerProperty(
        name= "Applink Variables",
        type=  ObjectCoat3D,
        description= "Applink variables"
    )

    bpy.types.Scene.simple3Dcoat= PointerProperty(
        name= "Applink Variables",
        type=  SimpleSceneCoat3D,
        description= "Applink variables"
    )


def unregister():
    import bpy

    del bpy.types.Object.simple3Dcoat
    del bpy.types.Scene.simple3Dcoat
    del bpy.simple3Dcoat
    
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()



