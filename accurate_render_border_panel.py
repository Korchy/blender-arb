# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-arb

from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class ACCURATE_RENDER_BORDER_PT_panel(Panel):
    bl_idname = 'ACCURATE_RENDER_BORDER_PT_panel'
    bl_label = 'ARB'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ARB'

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.accurate_region_border, 'x0')
        layout.prop(context.scene.accurate_region_border, 'y0')
        layout.prop(context.scene.accurate_region_border, 'x1')
        layout.prop(context.scene.accurate_region_border, 'y1')
        split = layout.split(factor=0.9)
        col = split.column()
        col = split.column()
        col.operator('accurate_region_border.sync', icon='FILE_REFRESH', text='')

        # self.layout.prop(context.window_manager.accurate_render_border_params, 'x0')
        # self.layout.prop(context.window_manager.accurate_render_border_params, 'y0')
        # self.layout.prop(context.window_manager.accurate_render_border_params, 'x1')
        # self.layout.prop(context.window_manager.accurate_render_border_params, 'y1')
        # self.layout.prop(context.window_manager.accurate_render_border_params, 'xywh')
        # operator = self.layout.operator('accurate_render_border.main', icon='OBJECT_HIDDEN')
        # operator.x1 = context.window_manager.accurate_render_border_params.x0
        # operator.y1 = context.window_manager.accurate_render_border_params.y0
        # operator.x2 = context.window_manager.accurate_render_border_params.x1
        # operator.y2 = context.window_manager.accurate_render_border_params.y1
        # operator.xywh = context.window_manager.accurate_render_border_params.xywh


def register():
    register_class(ACCURATE_RENDER_BORDER_PT_panel)


def unregister():
    unregister_class(ACCURATE_RENDER_BORDER_PT_panel)
