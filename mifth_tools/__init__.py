# BEGIN GPL LICENSE BLOCK #####
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
# END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Mifth Tools",
    "author": "Paul Geraskin",
    "version": (0, 1, 0),
    "blender": (2, 71, 0),
    "location": "3D Viewport",
    "description": "Mifth Tools",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Tools"}


if "bpy" in locals():
    import imp
    imp.reload(mifth_tools)
else:
    from . import mifth_tools

import bpy
from bpy.props import *


def register():
    bpy.mifthTools = dict()

    class MFTProperties(bpy.types.PropertyGroup):

        exportModelType = EnumProperty(
            name = "Export Type",
            items = (('OBJ', 'OBJ', ''),
                   ('FBX', 'FBX', ''),
                   ('DAE', 'DAE', ''),
                   ),
            default = 'OBJ'
        )

        doApplyModifiers = BoolProperty(
            name="Apply Modifiers",
            description="Apply Modifiers...",
            default=True
        )

        exportMaterials = BoolProperty(
            name="Export Materials",
            description="Export Materials...",
            default=True
        )

        copyTexturesPath = StringProperty(
            name="Copy Textures Path",
            subtype="DIR_PATH",
            default="",
        )

        type = EnumProperty(name="Export Type",
                            description="Different Export Types",
                            items=(("ppp", "Per-Pixel Painting", ""),
                           ("mv", "Microvertex Painting", ""),
                                ("ptex", "Ptex Painting", ""),
                                ("uv", "UV-Mapping", ""),
                                ("ref", "Reference Mesh", ""),
                                ("retopo", "Retopo mesh as new layer", ""),
                                ("vox", "Mesh As Voxel Object", ""),
                                ("voxcombine", "Mesh As single Voxel Object", ""),
                                ("alpha", "Mesh As New Pen Alpha", ""),
                                ("prim", "Mesh As Voxel Primitive", ""),
                                ("curv", "Mesh As a Curve Profile", ""),
                                ("autopo", "Mesh For Auto-retopology", ""),
                            ),
                            default= "ppp"
                            )

    bpy.utils.register_module(__name__)

    bpy.types.Scene.mifthTools = PointerProperty(
        name="Mifth Tools Variables",
        type=MFTProperties,
        description="Mifth Tools Properties"
    )


def unregister():
    import bpy

    del bpy.types.Scene.mifthTools
    del bpy.mifthTools
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
