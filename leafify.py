# Author: Rojuienx <rojuinex@gmail.com http://github.com/rojuinex>
# Version: 0.0.3
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
	"version":      (0, 0, 3),
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

class OBJECT_OT_leafify(bpy.types.Operator):
	"""Duplicates and flips selected faces to replicate dual-sided mesehs"""

	bl_idname      = "mesh.leafify"
	bl_label       = "Leafify"
	bl_options     = {"REGISTER", "UNDO"}

	leafify_offset = bpy.props.FloatVectorProperty(
		name        = "Transformation Offset",
		default     = (0.0, 0.0, 0.0),
		subtype     = "TRANSLATION",
		description = "Offset between faces.",
		#min         = 0.0,
		soft_min    = 0.0
	)

	leafify_preflip = bpy.props.BoolProperty(
		name        = "Flip Original Normals",
		default     = True,
		description = "Flip original face normals"
	)

	leafify_allow_zero = bpy.props.BoolProperty(
		name        = "Allow Zero",
		default     = False,
		description = "Don't warn about non-zero values."
	)

	@classmethod
	def poll(self, context):
		if context.active_object == None:
			return False

		# TODO: Check to see if faces are selected

		if context.mode == 'EDIT_MESH':
			return True

		return False

	def draw(self, context):
		col = self.layout.column()
		col.label("Plese use a non-zero vector.", icon='NONE')
		col.prop(self, "leafify_preflip")
		col.prop(self, "leafify_offset")
		col.prop(self, "leafify_allow_zero")
	# end of draw

	def action_common(self, context):
		if self.leafify_preflip == True:
			bpy.ops.mesh.flip_normals()

		offset = self.leafify_offset

		bpy.ops.mesh.duplicate_move(
			MESH_OT_duplicate      = {"mode":1}, 
			TRANSFORM_OT_translate = {
				"value":                      offset,
				"constraint_axis":            (False, False, False),
				"constraint_orientation":     "GLOBAL",
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
	# end of action_common

	def execute(self, context):
		self.action_common(context)
		return {"FINISHED"}
	# end of execute

	def invoke(self, context, event):
		self.action_common(context)
		return {"FINISHED"}
	# end of invoke

class LeafifyPanel(bpy.types.Panel):
	"""Options for Leafify"""

	bl_label       = "Leafify"
	bl_idname      = "OBJECT_PT_leafify_props"
	bl_space_type  = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_context     = "mesh_edit"

	def draw(self, context):
		row    = self.layout.row()
		row.operator("mesh.leafify", icon = "UV_VERTEXSEL")

def add_object_manual_map():
	url_manual_prefix  = "https://github.com/Rojuinex/leafify#"
	url_manual_mapping = (
		("bpy.ops.mesh.leafify", "usage"),
		) 
	return url_manual_prefix, url_manual_mapping


def register():
	bpy.utils.register_module(__name__)
	bpy.utils.register_manual_map(add_object_manual_map)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.utils.unregister_manual_map(add_object_manual_map)
	del bpy.types.Scene.leafify_preflip
	del bpy.types.Scene.leafify_normal
	del bpy.types.Scene.leafify_offset

if __name__ == "__main__":
	register()