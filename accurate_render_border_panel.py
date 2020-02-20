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
        # print(dir(context.area)) # width - height, x-y
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
            col = split.column()
            col.operator('accurate_region_border.sync', icon='FILE_REFRESH', text='')
        else:
            layout.prop(context.space_data, 'use_render_border', icon='SELECT_SET')



def register():
    register_class(ACCURATE_RENDER_BORDER_PT_panel)


def unregister():
    unregister_class(ACCURATE_RENDER_BORDER_PT_panel)
