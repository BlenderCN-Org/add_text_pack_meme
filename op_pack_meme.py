import bpy
from bpy.types import (
    Operator,
    )
# from bpy.props import (
#     IntProperty,
#     FloatProperty,
#     )
from .utils import (
    deselect_all,
    delete_collection_and_objects,
)


def active(context, ob=None):
    if not ob:
        return context.view_layer.objects.active
    else:
        context.view_layer.objects.active = ob


def copy_as_mesh(context, coll_font):
    deselect_all(context)
    coll_name = coll_font.name + ' - mesh'
    delete_collection_and_objects(context, coll_name)
    coll_mesh = bpy.data.collections.new(coll_name)
    context.scene.collection.children.link(coll_mesh)
    # Copy objects
    new_obs = []
    for orig in coll_font.objects:
        new_ob = bpy.data.objects[orig.name].copy()
        new_ob.data = new_ob.data.copy()
        new_ob.name = orig.name + ' - mesh'
        new_obs.append(new_ob)
        coll_mesh.objects.link(new_ob)

        # Convert to Mesh
        active(context, new_ob)
        new_ob.select_set('SELECT')
        orig.select_set('DESELECT')
        bpy.ops.object.convert(target='MESH', keep_original=False)


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
