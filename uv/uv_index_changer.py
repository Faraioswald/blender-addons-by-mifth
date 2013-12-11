# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2
#  of the License.
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
    "name": "UV Index Changer",
    "author": "Paul Geraskin",
    "version": (0,1),
    "blender": (2, 69, 0),
    "location": "View3D > ToolBar",
    "description": "Change Index Of UVMap.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "UV"}


import bpy
from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       )
from bpy.props import *


class UV_IC_Panel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'


class UV_IC_TexIndex(PropertyGroup):
    bpy.types.Scene.UVTexIndex = IntProperty(
             name = "UVIndex", 
             description = "set new UVIndex to selected objects",
             min = 1,
             max = 8,
             default = 1)

class UV_IC_Main(UV_IC_Panel, Panel):
    bl_context = "objectmode"
    bl_label = "UV Indexer"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):

        layout = self.layout

        scn = context.scene
        ob = context.object

        col = layout.column(align=True)

        row = layout.row(align=True)
        row.operator("uv.change_index", text="Change UV Index")

        col = layout.column()
        col.prop(scn, "UVTexIndex")


class UV_IC_ChangeIndex(UV_IC_Panel, Operator):
    bl_idname = "uv.change_index"
    bl_label = "Change Index"

    def execute(self, context):
        scene = context.scene

        for theObj in context.selected_objects:
            meshData = theObj.data

            #meshData.uv_textures.active_index = 0
            tmpuvmap = meshData.uv_textures.active
            tmpuvmap_name = tmpuvmap.name

            newuvmap = meshData.uv_textures.new()
            meshData.uv_textures.remove(tmpuvmap)
            meshData.uv_textures[len(meshData.uv_textures) - 1].name = tmpuvmap_name

        return{'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
    
    

