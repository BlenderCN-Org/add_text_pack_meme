# import bpy
from bpy.types import (
    Menu
)


class VIEW3D_MT_meme_menu(Menu):
    bl_label = 'Meme'
    bl_space_type = 'VIEW_3D'

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator('object.add_texts')
        col.operator('object.pack_meme')
