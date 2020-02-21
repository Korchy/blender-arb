# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-arb

from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class ACCURATE_REGION_BORDER_PT_panel(Panel):
    bl_idname = 'ACCURATE_REGION_BORDER_PT_panel'
    bl_label = 'ARB'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ARB'

    def draw(self, context):
        layout = self.layout
        if context.area.spaces[0].region_3d.view_perspective == 'CAMERA':
            layout.prop(context.scene.render, 'use_border', icon='SELECT_SET')
            layout.prop(context.scene.accurate_region_border, 'x0')
            layout.prop(context.scene.accurate_region_border, 'y0')
            if context.scene.accurate_region_border.mode == 'Top-Bottom':
                layout.prop(context.scene.accurate_region_border, 'x1')
                layout.prop(context.scene.accurate_region_border, 'y1')
            else:
                layout.prop(context.scene.accurate_region_border, 'x1', text='Width')
                layout.prop(context.scene.accurate_region_border, 'y1', text='Height')
            split = layout.split(factor=0.9)
            col = split.column()
            row = col.row()
            row.prop(context.scene.accurate_region_border, 'mode', expand=True)
        else:
            layout.prop(context.space_data, 'use_render_border', icon='SELECT_SET')
            area_index = context.screen.areas[:].index(context.area)
            while area_index >= len(context.window_manager.accurate_region_border):
                context.window_manager.accurate_region_border.add()
            area_accurate_region_border_parameters = context.window_manager.accurate_region_border[area_index]
            layout.prop(area_accurate_region_border_parameters, 'x0')
            layout.prop(area_accurate_region_border_parameters, 'y0')
            if area_accurate_region_border_parameters.mode == 'Top-Bottom':
                layout.prop(area_accurate_region_border_parameters, 'x1')
                layout.prop(area_accurate_region_border_parameters, 'y1')
            else:
                layout.prop(area_accurate_region_border_parameters, 'x1', text='Width')
                layout.prop(area_accurate_region_border_parameters, 'y1', text='Height')
            split = layout.split(factor=0.9)
            col = split.column()
            row = col.row()
            row.prop(area_accurate_region_border_parameters, 'mode', expand=True)
        col = split.column()
        col.operator('accurate_region_border.sync', icon='FILE_REFRESH', text='')


def register():
    register_class(ACCURATE_REGION_BORDER_PT_panel)


def unregister():
    unregister_class(ACCURATE_REGION_BORDER_PT_panel)
