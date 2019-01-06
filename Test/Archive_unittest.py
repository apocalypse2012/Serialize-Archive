__author__ = "Raymond Stewart"
__version__ = "1.0.0"
__maintainer__ = "Raymond Stewart"
__email__ = "info@raymond-stewart.com"

import unittest
import collections
import array
import Serialize-Archive.Archive as archive
import Serialize-Archive.BinarySerializer as ser

class stub_serializer(ser.BinarySerializer):

    CALLS_MADE = list()

    def __init__(self):
        super(stub_serializer, self).__init__()

    def __getattribute__(self, name):
        if name is not 'get_calls' and name is not 'CALLS_MADE':
            stub_serializer.CALLS_MADE.append(name)
        return super(stub_serializer, self).__getattribute__(name)

    def get_calls(self):
        return_calls = tuple(self.CALLS_MADE)
        self.CALLS_MADE = list()
        return return_calls

    def bytesSerialized(self):
        return 0

    def align(self, boundary ):
        pass

    def seek(self, pos ):
        pass

    def serialize_bool(self, value):
        return value

    def serialize_byte(self, value):
        return value

    def serialize_short(self, value):
        return value

    def serialize_int(self, value):
        return value

    def serialize_long(self, value):
        return value

    def serialize_string(self, value, destinationSize = None):
        return value

    def serialize_float(self, value):
        return value

    def serialize_double(self, value):
        return value

    def serialize_array(self, value, size):
        return value


class archive_interface(unittest.TestCase):

    def setUp(self):
        self.serializer = stub_serializer()
        self.archiver = archive.Archive(self.serializer)

    def test_archive_int(self):
        testVal = 10
        returnVal = self.archiver.serialize_prim(testVal)
        result = 'serialize_int' in self.serializer.get_calls()
        self.assertTrue(result, msg="Correct serializer method not called.")
        self.assertEqual(testVal, returnVal, msg="Test and result values are not the same.")

    def test_archive_long(self):
        testVal = 10L
        returnVal = self.archiver.serialize_prim(testVal)
        result = 'serialize_long' in self.serializer.get_calls()
        self.assertTrue(result, msg="Correct serializer method not called.")
        self.assertEqual(testVal, returnVal, msg="Test and result values are not the same.")

    def test_archive_bool(self):
        testVal = True
        returnVal = self.archiver.serialize_prim(testVal)
        result = 'serialize_bool' in self.serializer.get_calls()
        self.assertTrue(result, msg="Correct serializer method not called.")
        self.assertEqual(testVal, returnVal, msg="Test and result values are not the same.")

    def test_archive_double(self):
        testVal = 1.0
        returnVal = self.archiver.serialize_prim(testVal)
        result = 'serialize_double' in self.serializer.get_calls()
        self.assertTrue(result, msg="Correct serializer method not called.")
        self.assertEqual(testVal, returnVal, msg="Test and result values are not the same.")

    def test_archive_string(self):
        testVal = "foo"
        returnVal = self.archiver.serialize_prim(testVal)
        result = 'serialize_string' in self.serializer.get_calls()
        self.assertTrue(result, msg="Correct serializer method not called.")
        self.assertEqual(testVal, returnVal, msg="Test and result values are not the same.")

    def test_archive_unicode(self):
        testVal = u"foo"
        returnVal = self.archiver.serialize_prim(testVal)
        result = 'serialize_string' in self.serializer.get_calls()
        self.assertTrue(result, msg="Correct serializer method not called.")
        self.assertEqual(testVal, returnVal, msg="Test and result values are not the same.")

    def test_archive_orderedDict(self):
        testVal = collections.OrderedDict([('a', True), ('b', 1), ('b', 1L), ('c', 1.0), ('d', 'foo'), ('e', u'foo')])
        returnVal = self.archiver.serialize(testVal)
        calls = self.serializer.get_calls()
        methods = ['serialize_bool', 'serialize_int', 'serialize_long', 'serialize_double', 'serialize_string', 'serialize_string']
        result = reduce(lambda x, y: x and (y in calls), methods)
        self.assertTrue(result, msg="Correct serializer methods not called.")
        self.assertEqual(testVal, returnVal, msg="Test and result values are not the same.")

    def test_archive_array(self):
        testVal = array.array('d', [1.0, 2.0, 3.0])
        returnVal = self.archiver.serialize(testVal)
        result = 'serialize_array' in self.serializer.get_calls()
        self.assertTrue(result, msg="Correct serializer method not called.")
        self.assertEqual(testVal, returnVal, msg="Test and result values are not the same.")

    def test_archive_dict(self):
        testVal = {'list_data': ['fee', 'phi', 'foe', 'fum'], 'list_default': [str()]}
        returnVal = self.archiver.serialize(testVal)
        result = 'serialize_string' in self.serializer.get_calls()
        self.assertTrue(result, msg="Correct serializer method not called.")
        self.assertEqual(testVal, returnVal, msg="Test and result values are not the same.")

    def test_archive_defaultdict(self):
        testVal = {'list_data': [], 'list_default': [str()]}
        returnVal = self.archiver.serialize(testVal)
        self.assertEqual(testVal, returnVal, msg="Test and result values are not the same.")

    def test_archive_invalidType(self):
        self.assertRaises(ValueError, self.archiver.serialize, tuple())

    def test_archive_badlist(self):
        self.assertRaises(KeyError, self.archiver.serialize, dict())

if __name__ == '__main__':
    unittest.main()
