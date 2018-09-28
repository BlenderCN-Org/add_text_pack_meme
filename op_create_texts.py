import bpy
from bpy.types import (
    Operator,
    )
# from bpy.props import (
#     IntProperty,
#     FloatProperty,
#     )
from pprint import pprint


def del_collandobs(context, coll_name):
    if coll_name in context.scene.collection.children:
        coll = bpy.data.collections[coll_name]
        for ob in coll.objects:
            coll.objects.unlink(ob)
        bpy.data.collections.remove(coll)


def create_texts(self, context, line):
    del_collandobs(context, line)
    words = line.split(' ')
    collection = bpy.data.collections.new(line)
    context.scene.collection.children.link(collection)
    obs = []
    for i, word in enumerate(words):
        name = f'{i:02}' + ' ' + word
        text_data = bpy.data.curves.new(name, 'FONT')
        text_data.body = word
        ob = bpy.data.objects.new(name, text_data)
        collection.objects.link(ob)
        ob.select_set(action='SELECT')
        obs.append(ob)


class OBJECT_OT_add_texts(Operator):
    bl_idname = 'object.add_texts'
    bl_label = 'MEME: Add Texts'
    bl_description = 'Pack Meme'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        self.text = bpy.data.texts['memes']
        self.lines = self.text.as_string().split('\n')
        pprint(self.lines)
        create_texts(self, context, self.lines[0])
        return {'FINISHED'}

    def invoke(self, context, event):
        self.execute(context)
        return {'FINISHED'}
