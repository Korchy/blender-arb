import bpy

bl_info = {
    'name': 'Accurate Render Border',
    'category': 'Render',
    'author': 'Nikita Akimov',
    'version': (0, 0, 1),
    'blender': (2, 78, 0),
    'location': 'T-Bar > ARB tab',
    'wiki_url': 'http://b3d.interplanety.ru/add-on-accurate-render-border/',
    'tracker_url': 'http://b3d.interplanety.ru/add-on-accurate-render-border/',
    'description': 'Allows to set render border with accurate values'
}


class SetAccurateBorder(bpy.types.Operator):
    bl_idname = "render.set_accurate_border"
    bl_label = "Set Accurate Border"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(self, context):
        if (bpy.context.scene.accurate_border_scope.x1 == bpy.context.scene.accurate_border_scope.x2) or (bpy.context.scene.accurate_border_scope.y1 == bpy.context.scene.accurate_border_scope.y2):
            return False
        else:
            return True

    def execute(self, context):
        bpy.context.scene.render.border_min_x = bpy.context.scene.accurate_border_scope.x1/bpy.context.scene.render.resolution_x
        bpy.context.scene.render.border_max_x = bpy.context.scene.accurate_border_scope.x2/bpy.context.scene.render.resolution_x
        bpy.context.scene.render.border_min_y = 1-bpy.context.scene.accurate_border_scope.y1/bpy.context.scene.render.resolution_y
        bpy.context.scene.render.border_max_y = 1-bpy.context.scene.accurate_border_scope.y2/bpy.context.scene.render.resolution_y
        if bpy.context.scene.render.border_min_x > bpy.context.scene.render.border_max_x:
            bpy.context.scene.render.border_max_x, bpy.context.scene.render.border_min_x = bpy.context.scene.render.border_min_x, bpy.context.scene.render.border_max_x
        if bpy.context.scene.render.border_min_y > bpy.context.scene.render.border_max_y:
            bpy.context.scene.render.border_max_y, bpy.context.scene.render.border_min_y = bpy.context.scene.render.border_min_y, bpy.context.scene.render.border_max_y
        bpy.context.scene.render.use_border = True
        return {'FINISHED'}


class AccurateBorderScope(bpy.types.PropertyGroup):
    x1 = bpy.props.IntProperty(
        name = "Left Top X",
        description="Left X Coordinate",
        default = 0
    )
    x2 = bpy.props.IntProperty(
        name = "Right Bottom X",
        description = "Right X Coordinate",
        default = 0
    )
    y1 = bpy.props.IntProperty(
        name = "Left Top Y",
        description = "Top Y Coordinate",
        default = 0
    )
    y2 = bpy.props.IntProperty(
        name = "Right Bottom Y",
        description = "Bottom Y Coordinate",
        default = 0
    )


class AccurateBorderPanel(bpy.types.Panel):
    bl_idname = "panel.accurate_border_panel"
    bl_label = "Accurate Render Border"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "ARB"

    def draw(self, context):
        self.layout.prop(bpy.context.scene.accurate_border_scope, 'x1')
        self.layout.prop(bpy.context.scene.accurate_border_scope, 'y1')
        self.layout.prop(bpy.context.scene.accurate_border_scope, 'x2')
        self.layout.prop(bpy.context.scene.accurate_border_scope, 'y2')
        self.layout.operator("render.set_accurate_border", icon = 'BORDER_RECT', text = "Set Accurate Render Border")


def register():
    bpy.utils.register_class(SetAccurateBorder)
    bpy.utils.register_class(AccurateBorderScope)
    bpy.utils.register_class(AccurateBorderPanel)
    bpy.types.Scene.accurate_border_scope = bpy.props.PointerProperty(type=AccurateBorderScope)


def unregister():
    del bpy.types.Scene.accurate_border_scope
    bpy.utils.unregister_class(AccurateBorderPanel)
    bpy.utils.unregister_class(AccurateBorderScope)
    bpy.utils.unregister_class(SetAccurateBorder)

if __name__ == "__main__":
    register()
