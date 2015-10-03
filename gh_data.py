import rhinoscriptsyntax as rs
import json
import os

#if file:
#    filename = file
#else:
doc_path = os.path.dirname(rs.DocumentPath())
doc_name = os.path.basename(rs.DocumentPath())
doc_name = os.path.splitext(doc_name)[0]
filename = os.path.join(doc_path, '%s-data.json' % doc_name)

data = {}
try:
    data = json.load(open(filename, 'r'))
except:
    print('Cannot open file %s' % filename)
    pass

def get_value(id, key):
    if id in data:
        kv = data[id]
        if key:
            return kv[key] if key in kv else None
        else:
            return kv.keys()


def cast(value, t):
    try:
        value = t(value)
        return value
    except:
        return value
     

key = cast(get_value(str(id), key), float)
value = cast(get_value(str(id), key), float)
