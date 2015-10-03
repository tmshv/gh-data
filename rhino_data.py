import rhinoscriptsyntax as rs
import os
import json

attributes = ['window_width', 'window_height']

doc_path = rs.DocumentPath()
doc_name = rs.DocumentName()
data_file = os.path.join(
    os.path.dirname(doc_path),
    '%s-data.json' % os.path.splitext(doc_name)[0]
)

print(data_file)


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
    

obj_id = rs.GetObject('Select object:')
oid = str(obj_id)

print(oid)

data = read_data()
data = data if data else {}

values = list(map(lambda i: '', attributes))
keys = attributes
if oid in data:
    obj_data = data[oid]
    keys = obj_data.keys()
    values = obj_data.values()

    
values = rs.PropertyListBox(keys, values, 'Object data', oid)
if values:
    obj_data = {}
    for i in range(len(keys)):
        obj_data[keys[i]] = values[i]
    
    data[oid] = obj_data
    write_data(data)

print('done')