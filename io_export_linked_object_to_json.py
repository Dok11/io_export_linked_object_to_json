import json

import bpy
from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from mathutils import Quaternion

bl_info = {
    'name': 'Export Linked Objects to JSON',
    'author': 'Oleg Postoev',
    'version': (0, 0, 2),
    'blender': (2, 80, 0),
    'location': 'File > Export',
    'description': '',
    'warning': '',
    'wiki_url': '',
    'support': 'COMMUNITY',
    'category': 'Import-Export',
}


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def save_liked_data_to_json(context, filepath):
    """
    Function save data about linked objects into JSON as array of object with fields:
        name
        position
        quaternion
        scale
        filename
        parent
        visible

    :param context:
    :param filepath:
    :return:
    """

    print('running save_liked_data_to_json...')

    # Collect data into data_json
    json_data = []
    for item in bpy.data.objects:
        if item.type == 'EMPTY' and item.instance_type == 'COLLECTION':
            asset_name = bpy.data.objects[item.name].instance_collection.name
            print('asset_name is', asset_name)

            asset_file_name = bpy.data.collections[asset_name].library.name_full

            item_rotation_mode = item.rotation_mode
            item.rotation_mode = 'QUATERNION'

            rot = item.rotation_quaternion
            quaternion = Quaternion((rot[0], rot[1], rot[3], -rot[2]))

            data = {
                'name': item.name,
                'position': {
                    'x': truncate(-item.location.x, 1),
                    'y': truncate(item.location.z, 1),
                    'z': truncate(item.location.y, 1),
                },
                'quaternion': {
                    'w': truncate(quaternion.w, 3),
                    'x': truncate(-quaternion.x, 3),
                    'y': truncate(quaternion.y, 3),
                    'z': truncate(-quaternion.z, 3),
                },
                'scale': {
                    'x': truncate(-item.scale.x, 2),
                    'y': truncate(item.scale.z, 2),
                    'z': truncate(-item.scale.y, 2),
                },
                'parent': asset_name,
                'filename': asset_file_name.replace('.blend', ''),
                'visible': not (item.hide_viewport or item.hide_render),
            }
            json_data.append(data)

            item.rotation_mode = item_rotation_mode

    print('json_data')
    print(json_data)

    # Save data
    f = open(filepath, 'w', encoding='utf-8')
    json.dump(json_data, f, ensure_ascii=False, indent=2)
    f.close()

    print('Saved file: ' + filepath)
    return {'FINISHED'}


class ExportLinkedObjects(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = 'export_linked_objects.data'
    bl_label = 'Export to JSON'

    # ExportHelper mixin class uses this
    filename_ext = '.json'

    filter_glob: StringProperty(
        default='*.json',
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        return save_liked_data_to_json(context, self.filepath)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportLinkedObjects.bl_idname, text='Export Linked Objects to JSON')


def register():
    print('register 8')
    bpy.utils.register_class(ExportLinkedObjects)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportLinkedObjects)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == '__main__':
    register()
