# Author: Rojuienx <rojuinex@gmail.com http://github.com/rojuinex>
# Version: 0.0.1
# Date Created: December 28th, 2012
# Copyright (c) 2012, Rojuinex (See license agreement)

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# Created using Sam Hocevar's <sam@hocevar.net> Leafify Script as a refrence. #
# Original script contributed by FergusL and Aiena                            #
# contactable at #blenderpython @ irc.freenode.net                            #
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

bl_info = { 
	"name":         "Leafify", 
	"author":       "Rojuienx <rojuinex@gmail.com>",
	"version":      (0, 0, 1),
	"blender":      (2, 6, 5),
	"location":     "View3D > Tools",
	"description":  "Creates double sided faces.  Located in toolshelf and spacebar leafify",
	"warning":      "Currently in Beta",
	"wiki_url":     "https://github.com/Rojuinex/leafify",
	"tracker_url":  "https://github.com/Rojuinex/leafify/issues",
	"category":     "Mesh"
} 

import bpy
import bmesh
from mathutils import Vector

def leafify(self, context):

	if context.scene.leafify_preflip == True:
		bpy.ops.mesh.flip_normals()

	offset = context.scene.leafify_offset

	orientation = "GLOBAL"

	if context.scene.leafify_normal == True:
		orientation = "NORMAL"

	bpy.ops.mesh.duplicate_move(
		MESH_OT_duplicate      = {"mode":1}, 
		TRANSFORM_OT_translate = {
			"value":                      offset,
			"constraint_axis":            (False, False, False),
			"constraint_orientation":     orientation,
			"mirror":                     False,
			"proportional":               "DISABLED",
			"proportional_edit_falloff":  "SMOOTH",
			"proportional_size":          1, 
			"snap":                       False,
			"snap_target":                "CLOSEST",
			"snap_point":                 (0, 0, 0),
			"snap_align":                 False,
			"snap_normal":                (0, 0, 0),
			"texture_space":              False,
			"release_confirm":            False
			}
	)

	bpy.ops.mesh.flip_normals()

class OBJECT_OT_leafify(bpy.types.Operator):
	"""Duplicates and flips selected faces to replicate dual-sided mesehs"""

	bl_idname  = "mesh.leafify"
	bl_label   = "Leafify"
	bl_options = {"REGISTER", "UNDO"}

	def execute(self, context):

		if context.scene.leafify_offset == Vector((0.0, 0.0, 0.0)) :
			self.report({"ERROR"}, "Please use non-zero values.")
			return {"FINISHED"}
		else :
			leafify(self, context)
			return {"FINISHED"}

class LeafifyPanel(bpy.types.Panel):
	"""Options for Leafify"""

	bl_label       = "Leafify options"
	bl_idname      = "OBJECT_PT_leafify_props"
	bl_space_type  = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_context     = "mesh_edit"

	def draw(self, context):
		layout = self.layout
		col    = layout.column()
		col.prop(context.scene, "leafify_preflip")
		col.prop(context.scene, "leafify_offset")
		#col.prop(context.scene, "leafify_normal")
		row    = layout.row()
		row.operator("mesh.leafify", icon = "UV_VERTEXSEL")

def add_object_manual_map():
	url_manual_prefix = "https://github.com/Rojuinex/leafify#"
	url_manual_mapping = (
		("bpy.ops.mesh.leafify", "usage"),
		) 
	return url_manual_prefix, url_manual_mapping

def register():
	bpy.utils.register_module(__name__)
	bpy.utils.register_manual_map(add_object_manual_map)

	bpy.types.Scene.leafify_offset = bpy.props.FloatVectorProperty(
		name        = "Transformation Offset",
		default     = (0.0, 0.0, 0.0),
		subtype     = "TRANSLATION",
		description = "Offset between faces.",
		min         = 0.0,
		soft_min    = 0.0
	)

	bpy.types.Scene.leafify_normal = bpy.props.BoolProperty(
		name        = "Respect Normals",
		default     = False,
		description = "Transform with respect to face normals."
	)

	bpy.types.Scene.leafify_preflip = bpy.props.BoolProperty(
		name        = "Preflip Normals",
		default     = True,
		description = "Flip original face normals before running leafify."
	)


def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.utils.unregister_manual_map(add_object_manual_map)

if __name__ == "__main__":
	register()