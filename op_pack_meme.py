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
from mathutils import (
    Vector,
)

# BBox indices top view        # Front view
# 2, 3    6, 7                 # 1, 2    5, 6
# 0, 1    4, 5                 # 0, 3    4, 7


class Rect(object):
    """docstring for Rect."""

    def __init__(self, ob):
        self.ob = ob
        # self.bbox = [Vector(v) for v in ob.bound_box[:]]
        self.name = ob.name
        self.linehint = 0


def set_minmax(self):
    # Set min and max dimensions
    min_x = self.rects[0].ob.dimensions.x
    max_x = 0
    for r in self.rects:
        if r.ob.dimensions.x > max_x:
            max_x = r.ob.dimensions.x
        if r.ob.dimensions.x < min_x:
            min_x = r.ob.dimensions.x
    self.minmax = Vector((min_x, max_x))
    self.minmax_ratio = self.minmax[0] / self.minmax[1]


def set_linehint(self):
    pass


def setup_sim(self, context):
    print('\nSetting up sim...')
    self.rects = [Rect(ob) for ob in self.source.objects]
    self.count = len(self.rects)
    set_minmax(self)
    set_linehint(self)


class OBJECT_OT_pack_meme(Operator):
    bl_idname = 'object.pack_meme'
    bl_label = 'MEME: Pack Meme'
    bl_description = 'Pack Meme'
    bl_options = {'REGISTER', 'UNDO'}

    _timer = None
    source = None
    rects = []
    minmax = Vector((0, 0))
    minmax_ratio = 0

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def modal(self, context, event):
        # print(event.type, event.value)

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            print('\nCANCELLED')
            return {'CANCELLED'}

        if event.type in ['MIDDLEMOUSE', 'WHEELDOWNMOUSE', 'WHEELUPMOUSE']:
            return {'PASS_THROUGH'}

        if event.type == 'TIMER':
            # print('timer')
            return {'RUNNING_MODAL'}

        return {'RUNNING_MODAL'}

    def execute(self, context):
        print('\nEXECUTE')
        self.source = context.view_layer.collections.active.collection
        setup_sim(self, context)
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.3, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        print('\nINVOKE')
        self.execute(context)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
