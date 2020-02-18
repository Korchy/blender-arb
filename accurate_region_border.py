# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-arb


class AccurateRegionBorder:

    @staticmethod
    def max_x(context):
        # return max available Y region coordinate
        return context.scene.render.resolution_x

    @staticmethod
    def max_y(context):
        # return max available Y region coordinate
        return context.scene.render.resolution_y

    @classmethod
    def synchronize(cls, border_parameters, context):
        # sync values in parameter with real region border values
        border_parameters.x0 = context.scene.render.border_min_x * cls.max_x(context=context)
        border_parameters.y0 = (1 - context.scene.render.border_max_y) * cls.max_y(context=context)
        if border_parameters.mode == 'Top-Bottom':
            border_parameters.x1 = context.scene.render.border_max_x * cls.max_x(context=context)
            border_parameters.y1 = (1 - context.scene.render.border_min_y) * cls.max_y(context=context)
        else:
            border_parameters.x1 = context.scene.render.border_max_x * cls.max_x(context=context) - border_parameters.x0
            border_parameters.y1 = (1 - context.scene.render.border_min_y) * cls.max_y(context=context) - border_parameters.y0


    @classmethod
    def update_region_border_x0(cls, border_parameters, context):
        # update border_min_x
        context.scene.render.border_min_x = border_parameters.x0 / cls.max_x(context=context)

    @classmethod
    def update_region_border_y0(cls, border_parameters, context):
        # update border_max_y
        context.scene.render.border_max_y = 1 - border_parameters.y0 / cls.max_y(context=context)

    @classmethod
    def update_region_border_x1(cls, border_parameters, context):
        # update border_max_x
        if border_parameters.mode == 'Top-Bottom':
            context.scene.render.border_max_x = border_parameters.x1 / cls.max_x(context=context)
        else:
            context.scene.render.border_max_x = (border_parameters.x1 + border_parameters.x0)/ cls.max_x(context=context)

    @classmethod
    def update_region_border_y1(cls, border_parameters, context):
        # update border_min_y
        if border_parameters.mode == 'Top-Bottom':
            context.scene.render.border_min_y = 1 - border_parameters.y1 / cls.max_y(context=context)
        else:
            context.scene.render.border_min_y = 1 - (border_parameters.y1 + border_parameters.y0) / cls.max_y(context=context)
