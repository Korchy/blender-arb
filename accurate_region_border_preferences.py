# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-arb

from bpy.types import AddonPreferences
from bpy.props import BoolProperty
from bpy.utils import register_class, unregister_class


class ACCURATE_REGION_BORDER_Preferences(AddonPreferences):

    bl_idname = __package__

    auto_sync: BoolProperty(
        name='Auto Synchronize',
        default=False
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'auto_sync', icon='FILE_REFRESH')


def register():
    register_class(ACCURATE_REGION_BORDER_Preferences)


def unregister():
    unregister_class(ACCURATE_REGION_BORDER_Preferences)
