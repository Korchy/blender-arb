# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-arb

import bpy


class ACCURATE_REGION_BORDER_KeyMap:

    _keymaps = []

    @classmethod
    def register(cls, context):
        if context.window_manager.keyconfigs.addon:
            keymap = context.window_manager.keyconfigs.addon.keymaps.new(name='Screen', space_type='EMPTY')
            # add keys
            keymap_item = keymap.keymap_items.new('accurate_region_border.cancel_render_sequence', 'ESC', 'PRESS')
            cls._keymaps.append((keymap, keymap_item))

    @classmethod
    def unregister(cls):
        # clear keys
        for keymap, keymap_item in cls._keymaps:
            keymap.keymap_items.remove(keymap_item)
        cls._keymaps.clear()


def register():
    ACCURATE_REGION_BORDER_KeyMap.register(context=bpy.context)


def unregister():
    ACCURATE_REGION_BORDER_KeyMap.unregister()
