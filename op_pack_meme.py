import bpy
from bpy.types import (
    Operator,
)
from bpy.props import (
    IntProperty,
    FloatProperty,
)
from pprint import pprint


def create_texts(self, context, words):
    # create collection
    coll = bpy.data.collections.new('meme')
    # link collection
    context.scene.collection.children.link(coll)
    obs = []
    for i, word in enumerate(words):
        name = f'{i:02}' + ' ' + word
        text_data = bpy.data.curves.new(name, 'FONT')
        text_data.body = word
        ob = bpy.data.objects.new(name, text_data)
        coll.objects.link(ob)
        obs.append(ob)


def pack_meme(self, context, line):
    words = line.split(' ')
    obs = create_texts(self, context, words)


class OBJECT_OT_pack_meme(Operator):
    bl_idname = 'object.pack_meme'
    bl_label = 'Pack Meme'
    bl_description = 'Pack Meme'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        pprint(self.lines)
        pack_meme(self, context, self.lines[0])
        return {'FINISHED'}

    def invoke(self, context, event):
        self.text = bpy.data.texts['memes']
        self.lines = self.text.as_string().split('\n')
        self.execute(context)
        return {'FINISHED'}
