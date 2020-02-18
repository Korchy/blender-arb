# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-arb

import bpy
from bpy.props import IntProperty, PointerProperty, BoolProperty
from bpy.types import PropertyGroup
from bpy.utils import register_class, unregister_class
from .accurate_region_border import AccurateRegionBorder


class ACCURATE_RENDER_BORDER_Parameters(PropertyGroup):

    def max_x0(self, context):
        return context.scene.render.resolution_x

    x0: IntProperty(
        name='Left-Top X',
        description='Left X Coordinate',
        subtype='UNSIGNED',
        min=0,
        default=0,
        get=lambda self: self._x0_get(self),
        set=lambda self, value: self._x0_set(self, value)
    )
    y0: IntProperty(
        name='Left-Top Y',
        description='Top Y Coordinate',
        subtype='UNSIGNED',
        min=0,
        default=0,
        get=lambda self: self._y0_get(self),
        set=lambda self, value: self._y0_set(self, value)
    )
    x1: IntProperty(
        name='Right-Bottom X',
        description='Right X Coordinate',
        subtype='UNSIGNED',
        min=0,
        default=0,
        get=lambda self: self._x1_get(self),
        set=lambda self, value: self._x1_set(self, value)
    )
    y1: IntProperty(
        name='Right-Bottom Y',
        description='Bottom Y Coordinate',
        subtype='UNSIGNED',
        min=0,
        default=0,
        get=lambda self: self._y1_get(self),
        set=lambda self, value: self._y1_set(self, value)
    )
    xywh: BoolProperty(
        name='Width/Height',
        description='Width-Height instead Right-Bottom coordinates',
        default=False
    )

    @staticmethod
    def _x0_get(parameter):
        return parameter.get('x0', 0)

    @staticmethod
    def _x0_set(parameter, new_value):
        if new_value >= parameter.x1 > 0:
            new_value = parameter.x1
        elif new_value >= AccurateRegionBorder.max_x(context=bpy.context):
            new_value = AccurateRegionBorder.max_x(context=bpy.context)
        parameter['x0'] = new_value
        AccurateRegionBorder.update_region_border_x0(
            border_parameters=parameter,
            context=bpy.context
        )

    @staticmethod
    def _y0_get(parameter):
        return parameter.get('y0', 0)

    @staticmethod
    def _y0_set(parameter, new_value):
        if new_value >= parameter.y1 > 0:
            new_value = parameter.y1
        elif new_value >= AccurateRegionBorder.max_y(context=bpy.context):
            new_value = AccurateRegionBorder.max_y(context=bpy.context)
        parameter['y0'] = new_value
        AccurateRegionBorder.update_region_border_y0(
            border_parameters=parameter,
            context=bpy.context
        )

    @staticmethod
    def _x1_get(parameter):
        return parameter.get('x1', 0)

    @staticmethod
    def _x1_set(parameter, new_value):
        if new_value <= parameter.x0 > 0:
            new_value = parameter.x0
        elif new_value >= AccurateRegionBorder.max_x(context=bpy.context):
            new_value = AccurateRegionBorder.max_x(context=bpy.context)
        parameter['x1'] = new_value
        AccurateRegionBorder.update_region_border_x1(
            border_parameters=parameter,
            context=bpy.context
        )

    @staticmethod
    def _y1_get(parameter):
        return parameter.get('y1', 0)

    @staticmethod
    def _y1_set(parameter, new_value):
        if new_value <= parameter.y0 > 0:
            new_value = parameter.y0
        elif new_value >= AccurateRegionBorder.max_y(context=bpy.context):
            new_value = AccurateRegionBorder.max_y(context=bpy.context)
        parameter['y1'] = new_value
        AccurateRegionBorder.update_region_border_y1(
            border_parameters=parameter,
            context=bpy.context
        )


def register():
    register_class(ACCURATE_RENDER_BORDER_Parameters)
    bpy.types.Scene.accurate_region_border = PointerProperty(type=ACCURATE_RENDER_BORDER_Parameters)


def unregister():
    del bpy.types.Scene.accurate_region_border
    unregister_class(ACCURATE_RENDER_BORDER_Parameters)
