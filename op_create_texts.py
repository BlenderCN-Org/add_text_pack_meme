import bpy
from bpy.types import (
    Operator,
    )
# from bpy.props import (
#     IntProperty,
#     FloatProperty,
#     )
from pprint import pprint

from .utils import (
    active,
    deselect_all,
    delete_collection_and_objects,
)


def create_texts(self, context, line):
    delete_collection_and_objects(context, line)
    deselect_all(context)

    words = line.split(' ')

    collection = bpy.data.collections.new(line)
    context.scene.collection.children.link(collection)
    # context.view_layer.collections.active = collection # TODO Does not work

    obs = []
    for i, word in enumerate(words):
        name = f'{i:02}' + ' ' + word

        # Check if object exists and can be reused
        ob = None
        for existing in bpy.data.objects:
            if existing.type == 'FONT':
                if existing.data.body == word and existing.name == name:
                    ob = existing

        # Create new Text Object
        if not ob:
            text_data = bpy.data.curves.new(name, 'FONT')
            text_data.body = word
            ob = bpy.data.objects.new(name, text_data)

        # Link into Collection
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


def copy_as_mesh(self, context):
    coll_font = context.view_layer.collections.active.collection
    deselect_all(context)
    coll_name = coll_font.name + ' - mesh'
    delete_collection_and_objects(context, coll_name)
    coll_mesh = bpy.data.collections.new(coll_name)
    context.scene.collection.children.link(coll_mesh)
    # Copy objects
    for orig in coll_font.objects:
        # Copy opbjects and data
        new_ob = bpy.data.objects[orig.name].copy()
        new_ob.data = new_ob.data.copy()
        new_ob.name = orig.name + ' - mesh'
        print('Made Copy: ', new_ob.name)

        # Add new objects into new collection
        coll_mesh.objects.link(new_ob)

        # Convert new objects to mesh
        active(context, new_ob)
        new_ob.select_set('SELECT')
        # orig.select_set('DESELECT')
        bpy.ops.object.convert(target='MESH', keep_original=False)

    coll_font.hide_viewport = True
    coll_font.hide_render = True
    return coll_mesh


class OBJECT_OT_copy_as_mesh(Operator):
    bl_idname = 'object.copy_as_mesh'
    bl_label = 'MEME: Copy as Mesh'
    bl_description = 'Copy Collection of Fonts as Meshes'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        copy_as_mesh(self, context)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.execute(context)
        return {'FINISHED'}
