import bpy
import bpy.types as T
import bpy.props as P
from bpy import data as D, context as C


bl_info = {
    "name": "Bone Collection Toggle",
    "category": "3D View",
    "author": "piparkaq",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Item",
    "description": "Adds a panel with toggleable buttons for showing/hiding armature bone collections",
    "warning": "Experimental",
    "doc_url": "https://github.com/stuf/surimi_bone_collection_toggle",
    "tracker_url": "https://github.com/stuf/surimi_bone_collection_toggle/issues"
}


class SURIMI_PT_bone_collection_toggle(T.Panel):
    """Interface listing bone collections for the active armature,
       allowing toggling visibility of collections."""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'
    bl_idname = 'SURIMI_PT_bone_collection_toggle'
    bl_label = 'Bone Collections'

    @classmethod
    def poll(cls, ctx: T.Context):
        # Only show the UI if the currently active object is an armature
        return ctx.active_object.type == 'ARMATURE'

    def draw(self, ctx: T.Context):
        obj = ctx.active_object
        data: T.Armature = obj.data
        colls = data.collections

        layout = self.layout

        row = layout.row()

        for ix, (name, collection) in enumerate(colls.items()):
            op = row.operator(OBJECT_OT_surimi_toggle_bone_collection.bl_idname,
                              text=name,
                              depress=collection.is_visible,
                              )

            op.bone_collection = collection.name

            if ix % 2 == 1:
                row = layout.row()


class OBJECT_OT_surimi_toggle_bone_collection(T.Operator):
    bl_idname = 'surimi.toggle_bone_collection'
    bl_label = 'Toggle Bone Collection'
    bl_description = 'Toggles a bone collection\'s visibility'
    bl_options = {'REGISTER', 'UNDO'}

    bone_collection: P.StringProperty(name='Bone Collection')

    def execute(self, ctx: T.Context):
        if not ctx.active_object.type == 'ARMATURE':
            self.report({'ERROR'},
                        'Operator can only be called on armatures',
                        )
            return {'CANCELLED'}

        if not self.bone_collection:
            self.report({'ERROR'},
                        'Operator requires a bone collection name',
                        )
            return {'CANCELLED'}

        obj = ctx.active_object
        d: T.Armature = obj.data
        colls = d.collections

        coll = colls[self.bone_collection]
        coll.is_visible = not coll.is_visible

        return {'FINISHED'}

#


CLASSES = [SURIMI_PT_bone_collection_toggle,
           OBJECT_OT_surimi_toggle_bone_collection]


def register():
    for CLS in CLASSES:
        bpy.utils.register_class(CLS)


def unregister():
    for CLS in reversed(CLASSES):
        bpy.utils.unregister_class(CLS)
