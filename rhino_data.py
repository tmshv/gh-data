import rhinoscriptsyntax as rs
import os
import json


class Attribute:
    def __init__(self, key, value, type):
        self.key = key
        self.value = value
        self.type = type

    def get_value(self):
        return self.value

    def clone(self):
        return Attribute(self.key, self.value, self.type)
        
    def clone_with_value(self, value):
        c = self.clone()
        c.value = value
        return c
        
    def __repr__(self):
        return '<{k} {v} ({t})>'.format(k=self.key, v=self.get_value(), t=self.type)


def get_files(doc_path, doc_name):
    print(doc_path, doc_name)
    doc_dir = os.path.dirname(doc_path)
    name = os.path.splitext(doc_name)[0]

    return (
        os.path.join(doc_dir, '%s-data.json'   % name),
        os.path.join(doc_dir, '%s-config.json' % name)
    )


def read_data():
    try:
        f = open(data_file, 'r')
        data = f.read()
        f.close()
        return json.loads(data)
    except IOError as e:
        return None
    except SyntaxError as e:
        return None


def write_data(data):
    try:
        f = open(data_file, 'w')
        f.write(json.dumps(data, indent=4))
        f.write('\n')
        f.close()
    except:
        pass
    

def read_config(config_file):
    try:
        f = open(config_file, 'r')
        data = f.read()
        f.close()
        return json.loads(data)
    except IOError as e:
        return None
    except SyntaxError as e:
        return None    


def get_object_name(obj):
    return rs.ObjectName(obj)


def get_object_typology(obj):
    name = get_object_name(obj)
    obj_typology, obj_args = name.split(' ')
    return obj_typology


def get_attributes(config, object_type):
    def map_attr(a):
        if type(a) == str:
            return Attribute(a, None, None)
        elif type(a) == list:
            return Attribute(a[0], a[1], a[2])
        elif type(a) == dict:
            return Attribute(a['key'], a['defaultValue'], a['type'])
        else:
            return None

    if object_type in config:
        attrs_list = config[object_type]
        attrs_list = map(map_attr, attrs_list)
        return attrs_list
    else:
        return []


def get_object_data(data, obj):
    oid = str(obj)
    if oid in data:
        obj_data = data[oid]
        return obj_data
    else:
        return {}


def merge_attributes(default, overrideDict):
    merge = []
    for a in default:
        attr = a.clone()
        if a.key in overrideDict:
            attr.value = overrideDict[a.key]
        merge.append(attr)
    return merge


def show_object_dialog(obj, attributes):
    oid = str(obj)
    values = list(map(lambda a: a.get_value(), attributes))
    keys = list(map(lambda a: a.key, attributes))
    result = rs.PropertyListBox(keys, values, 'Object data', oid)
    if result:
        new_attrs = []
        for i in range(len(result)):
            v = result[i]
            new_attrs.append(attributes[i].clone_with_value(v))
        return new_attrs
    else:
        return None


data_file, config_file = get_files(rs.DocumentPath(), rs.DocumentName())
config = read_config(config_file)

data = read_data()
data = data if data else {}

obj = rs.GetObject('Select object:')

obj_typology = get_object_typology(obj)
typology_attributes = get_attributes(config, obj_typology)
obj_data = get_object_data(data, obj)

attributes = merge_attributes(typology_attributes, obj_data)
result = show_object_dialog(obj, attributes)

if result:
     obj_data = {}
     for a in result:
         obj_data[a.key] = a.get_value()    
     data[str(obj)] = obj_data
     write_data(data)