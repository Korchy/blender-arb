# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-arb

import bpy
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .accurate_region_border import AccurateRegionBorder
from .accurate_region_border_render_sequence import RenderSequence


class ACCURATE_REGION_BORDER_OT_sync(Operator):
    bl_idname = 'accurate_region_border.sync'
    bl_label = 'Sync'
    bl_description = 'Get values from scene'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.area.spaces[0].region_3d.view_perspective == 'CAMERA':
            parameter = context.scene.accurate_region_border
        else:
            # viewport
            area_index = context.screen.areas[:].index(context.area)
            parameter = context.window_manager.accurate_region_border[area_index]
        AccurateRegionBorder.synchronize(
            border_parameters=parameter,
            context=context
        )
        return {'FINISHED'}


class ACCURATE_REGION_BORDER_OT_render_sequence(Operator):
    bl_idname = 'accurate_region_border.render_sequence'
    bl_label = 'Render Animation'
    bl_description = 'Render TimeLine animation with region border'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        RenderSequence.render(context=context)
        return {'FINISHED'}


class ACCURATE_REGION_BORDER_OT_cancel_render_sequence(Operator):
    bl_idname = 'accurate_region_border.cancel_render_sequence'
    bl_label = 'Cancel Render Animation'
    bl_description = 'Cancel render TimeLine animation with region border'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        RenderSequence.cancel_render()
        return {'FINISHED'}


class ACCURATE_REGION_BORDER_OT_to_all_scenes(Operator):
    bl_idname = 'accurate_region_border.to_all_scenes'
    bl_label = 'To All Scenes'
    bl_description = 'Translate current region border to all scenes'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        AccurateRegionBorder.to_all_scenes(
            src_scene=context.scene,
            scenes=bpy.data.scenes
        )
        return {'FINISHED'}


def register():
    register_class(ACCURATE_REGION_BORDER_OT_sync)
    register_class(ACCURATE_REGION_BORDER_OT_render_sequence)
    register_class(ACCURATE_REGION_BORDER_OT_cancel_render_sequence)
    register_class(ACCURATE_REGION_BORDER_OT_to_all_scenes)


def unregister():
    unregister_class(ACCURATE_REGION_BORDER_OT_to_all_scenes)
    unregister_class(ACCURATE_REGION_BORDER_OT_cancel_render_sequence)
    unregister_class(ACCURATE_REGION_BORDER_OT_render_sequence)
    unregister_class(ACCURATE_REGION_BORDER_OT_sync)
