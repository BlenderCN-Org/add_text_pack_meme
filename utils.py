import bpy


def deselect_all(context):
    for ob in context.scene.collection.all_objects:
        ob.select_set('DESELECT')


def delete_collection_and_objects(context, coll_name):
    if coll_name in context.scene.collection.children:
        coll = bpy.data.collections[coll_name]
        for ob in coll.objects:
            coll.objects.unlink(ob)
            bpy.data.objects.remove(ob)
        bpy.data.collections.remove(coll)
