import bpy, bmesh
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty

bl_info = {
    "name": "Vertex Weight Presets",
    "author": "Jonas Francisco",
    "version": (0, 0, 1),
    "blender": (2, 7, 8),
    "description": "Add presets for fast assign vertex group weight values",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh"}

class VertexWeightPresetsPreferences(AddonPreferences):
    bl_idname = __name__
    presets = StringProperty(
        name="Presets",
        default="0.25, 0.50, 0.75, 1"
    )
    def draw(self, context):
        layout = self.layout
        layout.label(text="Presets (default '0.25, 0.50, 0.75, 1', without quotes)")
        layout.prop(self, "presets")

class SetVertexGroupWeightOperator(bpy.types.Operator):
    bl_idname = "window.set_vertex_group_weight"
    bl_label = "Set Vertex Group Weight"
    value = bpy.props.FloatProperty()
    def execute(self, context):
        return {'FINISHED'}
    def invoke(self, context, event):
        context.scene.tool_settings.vertex_group_weight = self.value
        bpy.ops.object.vertex_group_assign();
        return self.execute(context)

def test(self,context):
    layout = self.layout
    row = layout.row()
    sub = row.row(align=True)

    def parseFloat(value):
        try:
            return float(value.strip())
        except:
            return 0

    addon_prefs = bpy.context.user_preferences.addons["vertex-weight-preset"].preferences
    presets = map(parseFloat, addon_prefs.presets.split(","))
    for i in presets:
        sub.operator("window.set_vertex_group_weight", text=str(i)).value = i

def register():
    bpy.utils.register_class(VertexWeightPresetsPreferences)
    bpy.utils.register_class(SetVertexGroupWeightOperator)
    bpy.types.DATA_PT_vertex_groups.append(test)

def unregister():
    bpy.utils.unregister_class(SetVertexGroupWeightOperator)
    bpy.utils.unregister_class(VertexWeightPresetsPreferences)
    bpy.types.DATA_PT_vertex_groups.remove(test)

if __name__ == "__main__":
    register()
