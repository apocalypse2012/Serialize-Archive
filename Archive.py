__author__ = "Raymond Stewart"
__copyright__ = "Copyright 2018"
__credits__ = ["Raymond Stewart"]
__license__ = "EULA"
__version__ = "1.0.0"
__maintainer__ = "Raymond Stewart"
__email__ = "info@raymond-stewart.com"

import array
import collections
from copy import deepcopy

class Archive(object):

    def __init__(self, bSerial):
        self.m_serializer = bSerial

    @staticmethod
    def isValidCollectionType(value):
        validTypes = (collections.OrderedDict, array.array, dict)
        return isinstance(value, validTypes)

    @staticmethod
    def isValidPrimType(value):
        validTypes = (bool, int, long, float, str, unicode)
        return isinstance(value, validTypes)

    def getBytes(self):
        return self.m_serializer.getByteArray()

    def serialize_prim(self, attrObj):
        if isinstance(attrObj, bool):
            b = self.m_serializer.serialize_bool(attrObj)
            return b

        elif isinstance(attrObj, int):
            i = self.m_serializer.serialize_int(attrObj)
            return i

        elif isinstance(attrObj, long):
            l = self.m_serializer.serialize_long(attrObj)
            return l

        elif isinstance(attrObj, float):  # Python is double precision by default
            d = self.m_serializer.serialize_double(attrObj)
            return d

        # TODO: Handle unicode
        elif isinstance(attrObj, str):
            s = self.m_serializer.serialize_string(attrObj)
            return s

        elif isinstance(attrObj, unicode):
            strValue = attrObj.encode("utf-8")
            s = self.serialize_prim(strValue)
            uStrValue = unicode(s,encoding='utf-8')
            return uStrValue

        else:
            raise ValueError("Supplied data is of invalid type, {}".format(type(attrObj)))

    def serialize(self, obj):

        if self.isValidCollectionType(obj):
            if isinstance(obj, collections.OrderedDict):
                for name in obj.iterkeys():
                    value = obj[name]
                    serialVal = self.serialize(value)
                    obj[name] = serialVal

            elif isinstance(obj, array.array):
                arraySize = self.serialize_prim(obj.itemsize*len(obj))
                attrVal = self.m_serializer.serialize_array(obj, arraySize)
                return attrVal

            else:
                data = obj.get('list_data')
                default = obj.get('list_default')
                if isinstance(data, list) and default is not None:
                    arraySize = len(data)
                    if arraySize:
                        arraySize = self.serialize_prim(arraySize)
                        for idx in xrange(arraySize):
                            value = data[idx]
                            serialVal = self.serialize(value)
                            data[idx] = serialVal

                    else:
                        arraySize = self.serialize_prim(0)
                        for idx in xrange(arraySize):
                            value = deepcopy(default)
                            serialVal = self.serialize(value)
                            data.append(serialVal)

                    obj['list_data'] = data
                else:
                    raise KeyError

        elif self.isValidPrimType(obj):
            attrVal = self.serialize_prim(obj)
            return attrVal

        else:
            raise ValueError("{}: Cannot serialize invalid type, {}".format(str(obj), type(obj)))

        return obj
