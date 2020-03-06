# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-arb


class AccurateRegionBorder:

    @classmethod
    def max_x(cls, context):
        # return max available Y region coordinate
        if cls.area_mode(context=context) == 'CAMERA':
            return context.scene.render.resolution_x
        else:
            # viewport
            return context.area.width

    @classmethod
    def max_y(cls, context):
        # return max available Y region coordinate
        if cls.area_mode(context=context) == 'CAMERA':
            return context.scene.render.resolution_y
        else:
            # viewport
            return context.area.height

    @classmethod
    def synchronize(cls, border_parameters, context):
        # sync values in parameter with real region border values
        real_coords = cls.border_coordinates(context=context)
        border_parameters.x0 = real_coords['x0']
        border_parameters.y0 = real_coords['y0']
        if border_parameters.mode == 'Top-Bottom':
            border_parameters.x1 = real_coords['x1']
            border_parameters.y1 = real_coords['y1']
        else:
            border_parameters.x1 = real_coords['x1'] - real_coords['x0']
            border_parameters.y1 = real_coords['y1'] - real_coords['y0']

    @classmethod
    def to_all_scenes(cls, src_scene, scenes):
        # translate border parameters from src_scene to all scenes
        # for camera
        for scene in scenes:
            if scene != src_scene:
                scene.render.use_border = src_scene.render.use_border
                scene.accurate_region_border.mode = src_scene.accurate_region_border.mode
                scene.accurate_region_border.x0 = src_scene.accurate_region_border.x0
                scene.accurate_region_border.y0 = src_scene.accurate_region_border.y0
                scene.accurate_region_border.x1 = src_scene.accurate_region_border.x1
                scene.accurate_region_border.y1 = src_scene.accurate_region_border.y1
                scene.render.border_min_x = src_scene.accurate_region_border.x0 / scene.render.resolution_x
                scene.render.border_max_y = 1 - src_scene.accurate_region_border.y0 / scene.render.resolution_y
                if src_scene.accurate_region_border.mode == 'Top-Bottom':
                    scene.render.border_max_x = src_scene.accurate_region_border.x1 / scene.render.resolution_x
                    scene.render.border_min_y = 1 - src_scene.accurate_region_border.y0 / scene.render.resolution_y
                elif src_scene.accurate_region_border.mode == 'Width-Height':
                    scene.render.border_max_x = (src_scene.accurate_region_border.x0 + src_scene.accurate_region_border.x1) / scene.render.resolution_x
                    scene.render.border_min_y = 1 - (src_scene.accurate_region_border.y0 + src_scene.accurate_region_border.y1) / scene.render.resolution_y

    @classmethod
    def update_region_border_x0(cls, border_parameters, context):
        # update border_min_x
        if cls.area_mode(context=context) == 'CAMERA':
            context.scene.render.border_min_x = border_parameters.x0 / cls.max_x(context=context)
        else:
            # viewport
            context.space_data.render_border_min_x = border_parameters.x0 / cls.max_x(context=context)
        if border_parameters.mode == 'Top-Bottom':
            if border_parameters.x1 < border_parameters.x0:
                border_parameters.x1 = border_parameters.x0
        elif border_parameters.mode == 'Width-Height':
            border_parameters.x1 = border_parameters.x1

    @classmethod
    def update_region_border_y0(cls, border_parameters, context):
        # update border_max_y
        if cls.area_mode(context=context) == 'CAMERA':
            context.scene.render.border_max_y = 1 - border_parameters.y0 / cls.max_y(context=context)
        else:
            # viewport
            context.space_data.render_border_max_y = 1 - border_parameters.y0 / cls.max_y(context=context)
        if border_parameters.mode == 'Top-Bottom':
            if border_parameters.y1 < border_parameters.y0:
                border_parameters.y1 = border_parameters.y0
        elif border_parameters.mode == 'Width-Height':
            border_parameters.y1 = border_parameters.y1

    @classmethod
    def update_region_border_x1(cls, border_parameters, context):
        # update border_max_x
        if cls.area_mode(context=context) == 'CAMERA':
            if border_parameters.mode == 'Top-Bottom':
                context.scene.render.border_max_x = border_parameters.x1 / cls.max_x(context=context)
            elif border_parameters.mode == 'Width-Height':
                context.scene.render.border_max_x = (border_parameters.x1 + border_parameters.x0) / cls.max_x(context=context)
        else:
            # viewport
            if border_parameters.mode == 'Top-Bottom':
                context.space_data.render_border_max_x = border_parameters.x1 / cls.max_x(context=context)
            elif border_parameters.mode == 'Width-Height':
                context.space_data.render_border_max_x = (border_parameters.x1 + border_parameters.x0) / cls.max_x(context=context)

    @classmethod
    def update_region_border_y1(cls, border_parameters, context):
        # update border_min_y
        if cls.area_mode(context=context) == 'CAMERA':
            if border_parameters.mode == 'Top-Bottom':
                context.scene.render.border_min_y = 1 - border_parameters.y1 / cls.max_y(context=context)
            elif border_parameters.mode == 'Width-Height':
                context.scene.render.border_min_y = 1 - (border_parameters.y1 + border_parameters.y0) / cls.max_y(context=context)
        else:
            # viewport
            if border_parameters.mode == 'Top-Bottom':
                context.space_data.render_border_min_y = 1 - border_parameters.y1 / cls.max_y(context=context)
            elif border_parameters.mode == 'Width-Height':
                context.space_data.render_border_min_y = 1 - (border_parameters.y1 + border_parameters.y0) / cls.max_y(context=context)

    @staticmethod
    def area_mode(context):
        # area mode
        if not context.area or not hasattr(context.area.spaces[0], 'region_3d'):
            # for animation from timeline - only for camera
            return 'CAMERA'
        else:
            return context.area.spaces[0].region_3d.view_perspective

    @classmethod
    def border_coordinates(cls, context):
        # get real border coordinates (x0, y0, x1, y1)
        if cls.area_mode(context=context) == 'CAMERA':
            return {
                'x0': round(context.scene.render.border_min_x * cls.max_x(context=context)),
                'y0': round((1 - context.scene.render.border_max_y) * cls.max_y(context=context)),
                'x1': round(context.scene.render.border_max_x * cls.max_x(context=context)),
                'y1': round((1 - context.scene.render.border_min_y) * cls.max_y(context=context))
            }
        else:
            # viewport
            return {
                'x0': round(context.space_data.render_border_min_x * cls.max_x(context=context)),
                'y0': round((1 - context.space_data.render_border_max_y) * cls.max_y(context=context)),
                'x1': round(context.space_data.render_border_max_x * cls.max_x(context=context)),
                'y1': round((1 - context.space_data.render_border_min_y) * cls.max_y(context=context))
            }
