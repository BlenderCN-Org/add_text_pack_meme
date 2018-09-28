import bpy
from bpy.types import (
    Operator,
    )
# from bpy.props import (
#     IntProperty,
#     FloatProperty,
#     )


def pack_meme(self, context):
    pass


class OBJECT_OT_pack_meme(Operator):
    bl_idname = 'object.pack_meme'
    bl_label = 'MEME: Pack Meme'
    bl_description = 'Pack Meme'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        pack_meme(self, context)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.execute(context)
        return {'FINISHED'}
