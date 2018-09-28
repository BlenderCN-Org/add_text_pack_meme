import bpy
from bpy.types import (
    Operator,
    )
# from bpy.props import (
#     IntProperty,
#     FloatProperty,
#     )
from .utils import (
    active,
    deselect_all,
    delete_collection_and_objects,
)


def copy_as_mesh(context, coll_font):
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
    return coll_mesh


def pack_meme(self, context):
    coll_font = context.view_layer.collections.active.collection
    # obs = coll_font.objects
    # Create Mesh version copy of collection
    coll_mesh = copy_as_mesh(context, coll_font)


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
