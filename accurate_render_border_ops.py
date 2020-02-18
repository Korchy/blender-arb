# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-arb

from bpy.props import IntProperty, BoolProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .accurate_region_border import AccurateRegionBorder


class ACCURATE_RENDER_BORDER_OT_sync(Operator):
    bl_idname = 'accurate_region_border.sync'
    bl_label = 'Sync'
    bl_description = 'Sync accurate region border with real border values'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        AccurateRegionBorder.synchronize(
            border_parameters=context.scene.accurate_region_border,
            context=context
        )
        return {'FINISHED'}


class ACCURATE_RENDER_BORDER_OT_main(Operator):
    bl_idname = 'accurate_render_border.main'
    bl_label = 'Set Accurate Border'
    bl_description = 'Accurate Render Border - main operator'
    bl_options = {'REGISTER', 'UNDO'}

    x1: IntProperty(
        name='Left-Top X',
        description='Left X Coordinate',
        subtype='UNSIGNED',
        min=0,
        default=0
    )
    x2: IntProperty(
        name='Right-Bottom X',
        description='Right X Coordinate',
        subtype='UNSIGNED',
        min=0,
        default=0,
    )
    y1: IntProperty(
        name='Left-Top Y',
        description='Top Y Coordinate',
        subtype='UNSIGNED',
        min=0,
        default=0
    )
    y2: IntProperty(
        name='Right-Bottom Y',
        description='Bottom Y Coordinate',
        subtype='UNSIGNED',
        min=0,
        default=0
    )
    xywh: BoolProperty(
        name='Width/Height',
        description='Width-Height instead Right-Bottom coordinates',
        default=False
    )

    def execute(self, context):
        context.scene.render.border_min_x = context.window_manager.accurate_render_border_params.x0 / context.scene.render.resolution_x
        context.scene.render.border_min_y = 1 - context.window_manager.accurate_render_border_params.y0 / context.scene.render.resolution_y
        if context.window_manager.accurate_render_border_params.xywh:
            context.scene.render.border_max_x = (context.window_manager.accurate_render_border_params.x0 + context.window_manager.accurate_render_border_params.x1) / context.scene.render.resolution_x
            context.scene.render.border_max_y = 1 - (context.window_manager.accurate_render_border_params.y0 + context.window_manager.accurate_render_border_params.y1) / context.scene.render.resolution_y
        else:
            context.scene.render.border_max_x = context.window_manager.accurate_render_border_params.x1 / context.scene.render.resolution_x
            context.scene.render.border_max_y = 1 - context.window_manager.accurate_render_border_params.y1 / context.scene.render.resolution_y
        if context.scene.render.border_min_x > context.scene.render.border_max_x:
            context.scene.render.border_max_x, context.scene.render.border_min_x = context.scene.render.border_min_x, context.scene.render.border_max_x
        if context.scene.render.border_min_y > context.scene.render.border_max_y:
            context.scene.render.border_max_y, context.scene.render.border_min_y = context.scene.render.border_min_y, context.scene.render.border_max_y
        context.scene.render.use_border = True
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if not context.window_manager.accurate_render_border_params.xywh \
                and ((context.window_manager.accurate_render_border_params.x0 == context.window_manager.accurate_render_border_params.x1)
                     or (context.window_manager.accurate_render_border_params.y0 == context.window_manager.accurate_render_border_params.y1)
                     ):
            return False
        if context.window_manager.accurate_render_border_params.xywh \
                and ((context.window_manager.accurate_render_border_params.x1 == 0)
                     or (context.window_manager.accurate_render_border_params.y1 == 0)
                     ):
            return False
        return True


def register():
    register_class(ACCURATE_RENDER_BORDER_OT_sync)


def unregister():
    unregister_class(ACCURATE_RENDER_BORDER_OT_sync)
