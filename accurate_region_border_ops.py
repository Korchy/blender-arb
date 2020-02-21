# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-arb

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .accurate_region_border import AccurateRegionBorder


class ACCURATE_REGION_BORDER_OT_sync(Operator):
    bl_idname = 'accurate_region_border.sync'
    bl_label = 'Sync'
    bl_description = 'Sync accurate region border with real border values'
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


def register():
    register_class(ACCURATE_REGION_BORDER_OT_sync)


def unregister():
    unregister_class(ACCURATE_REGION_BORDER_OT_sync)
