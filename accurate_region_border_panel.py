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
            # camera
            row = layout.row()
            row.prop(context.scene.render, 'use_border', icon='SELECT_SET')
            row.prop(context.scene.render, 'use_crop_to_border', icon_only=True, icon='OBJECT_HIDDEN')
            row.operator('accurate_region_border.render_sequence', icon='RENDER_ANIMATION', text='')
            if context.scene.accurate_region_border.mode == 'Top-Bottom':
                layout.prop(context.scene.accurate_region_border, 'x0', text='Left')
                layout.prop(context.scene.accurate_region_border, 'x1', text='Right')
                layout.prop(context.scene.accurate_region_border, 'y1', text='Up')
                layout.prop(context.scene.accurate_region_border, 'y0', text='Down')
            else:
                layout.prop(context.scene.accurate_region_border, 'x0', text='Left')
                layout.prop(context.scene.accurate_region_border, 'y0', text='Up')
                layout.prop(context.scene.accurate_region_border, 'x1', text='Width')
                layout.prop(context.scene.accurate_region_border, 'y1', text='Height')
            split = layout.split(factor=0.8)
            col = split.column()
            row = col.row()
            row.prop(context.scene.accurate_region_border, 'mode', expand=True)
        else:
            # viewport
            layout.prop(context.space_data, 'use_render_border', icon='SELECT_SET')
            area_index = context.screen.areas[:].index(context.area)
            while area_index >= len(context.window_manager.accurate_region_border):
                context.window_manager.accurate_region_border.add()
            area_accurate_region_border_parameters = context.window_manager.accurate_region_border[area_index]
            if area_accurate_region_border_parameters.mode == 'Top-Bottom':
                layout.prop(area_accurate_region_border_parameters, 'x0', text='Left')
                layout.prop(area_accurate_region_border_parameters, 'x1', text='Right')
                layout.prop(area_accurate_region_border_parameters, 'y1', text='Up')
                layout.prop(area_accurate_region_border_parameters, 'y0', text='Down')
            else:
                layout.prop(area_accurate_region_border_parameters, 'x0', text='Left')
                layout.prop(area_accurate_region_border_parameters, 'y0', text='Up')
                layout.prop(area_accurate_region_border_parameters, 'x1', text='Width')
                layout.prop(area_accurate_region_border_parameters, 'y1', text='Height')
            split = layout.split(factor=0.8)
            col = split.column()
            row = col.row()
            row.prop(area_accurate_region_border_parameters, 'mode', expand=True)
        col = split.column()
        row = col.row()
        row.operator('accurate_region_border.sync', icon='FILE_REFRESH', text='')
        row.operator('accurate_region_border.to_all_scenes', icon='CON_LOCLIKE', text='')


def register():
    register_class(ACCURATE_REGION_BORDER_PT_panel)


def unregister():
    unregister_class(ACCURATE_REGION_BORDER_PT_panel)
