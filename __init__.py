# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-arb

from . import accurate_region_border_parameters
from . import accurate_region_border_ops
from . import accurate_region_border_panel
from .addon import Addon


bl_info = {
    'name': 'accurate_region_border',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 1, 0),
    'blender': (2, 82, 0),
    'location': 'N-Panel > ARB',
    'wiki_url': 'https://b3d.interplanety.org/en/blender-add-on-accurate-region-border/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-add-on-accurate-region-border/',
    'description': 'Allows to set render region border with accurate values'
}


def register():
    if not Addon.dev_mode():
        accurate_region_border_parameters.register()
        accurate_region_border_ops.register()
        accurate_region_border_panel.register()
    else:
        print('It seems you are trying to use the dev version of the ' + bl_info['name'] + ' add-on. It may work not properly. Please download and use the release version!')


def unregister():
    if not Addon.dev_mode():
        accurate_region_border_panel.unregister()
        accurate_region_border_ops.unregister()
        accurate_region_border_parameters.unregister()


if __name__ == '__main__':
    register()
