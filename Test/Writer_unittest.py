import unittest
import Serialize-Archive.BinaryWriter as bWrite
import array
import sys


class Serialize_to_Binary(unittest.TestCase):

    def test_serialize_bool(self):
        testVal = True
        rubric = '\x01'
        serializeOut = bWrite.BinaryWriter()
        returnValue = serializeOut.serialize_bool(testVal)
        testResult = serializeOut.getByteArray()
        self.assertTrue(returnValue == testVal, msg="Return value does not equal write value.")
        self.assertTrue(testResult == rubric, msg="Bytes serialized do not match the expected output.")

    def test_serialize_byte(self):
        testVal = 127
        rubric = '\x7f'
        serializeOut = bWrite.BinaryWriter()
        returnValue = serializeOut.serialize_byte(testVal)
        testResult = serializeOut.getByteArray()
        self.assertTrue(returnValue == testVal, msg="Return value does not equal write value.")
        self.assertTrue(testResult == rubric, msg="Bytes serialized do not match the expected output.")

    def test_serialize_short(self):
        testVal = 127
        rubric = '\x7f\x00'
        serializeOut = bWrite.BinaryWriter()
        returnValue = serializeOut.serialize_short(testVal)
        testResult = serializeOut.getByteArray()
        self.assertTrue(returnValue == testVal, msg="Return value does not equal write value.")
        self.assertTrue(testResult == rubric, msg="Bytes serialized do not match the expected output.")

    def test_serialize_int2(self):
        testVal = 127
        rubric = '\x7f\x00'
        serializeOut = bWrite.BinaryWriter()
        serializeOut.m_targetSizeInt = 2
        returnValue = serializeOut.serialize_int(testVal)
        testResult = serializeOut.getByteArray()
        self.assertTrue(returnValue == testVal, msg="Return value does not equal write value.")
        self.assertTrue(testResult == rubric, msg="Bytes serialized do not match the expected output.")

    def test_serialize_int4(self):
        testVal = 127
        rubric = '\x7f\x00\x00\x00'
        serializeOut = bWrite.BinaryWriter()
        serializeOut.m_targetSizeInt = 4
        returnValue = serializeOut.serialize_int(testVal)
        testResult = serializeOut.getByteArray()
        self.assertTrue(returnValue == testVal, msg="Return value does not equal write value.")
        self.assertTrue(testResult == rubric, msg="Bytes serialized do not match the expected output.")

    def test_serialize_int8(self):
        testVal = 127
        rubric = '\x7f\x00\x00\x00\x00\x00\x00\x00'
        serializeOut = bWrite.BinaryWriter()
        serializeOut.m_targetSizeInt = 8
        returnValue = serializeOut.serialize_int(testVal)
        testResult = serializeOut.getByteArray()
        self.assertTrue(returnValue == testVal, msg="Return value does not equal write value.")
        self.assertTrue(testResult == rubric, msg="Bytes serialized do not match the expected output.")

    def test_serialize_long(self):
        testVal = 127L
        rubric = '\x7f\x00\x00\x00\x00\x00\x00\x00'
        serializeOut = bWrite.BinaryWriter()
        returnValue = serializeOut.serialize_long(testVal)
        testResult = serializeOut.getByteArray()
        self.assertTrue(returnValue == testVal, msg="Return value does not equal write value.")
        self.assertTrue(testResult == rubric, msg="Bytes serialized do not match the expected output.")

    def test_serialize_float(self):
        testVal = 3.1415926
        rubric = '\xda\x0fI@'
        serializeOut = bWrite.BinaryWriter()
        returnValue = serializeOut.serialize_float(testVal)
        testResult = serializeOut.getByteArray()
        self.assertTrue(returnValue == testVal, msg="Return value does not equal write value.")
        self.assertTrue(testResult == rubric, msg="Bytes serialized do not match the expected output.")

    def test_serialize_double(self):
        testVal = 3.1415926
        rubric = 'J\xd8\x12M\xfb!\t@'
        serializeOut = bWrite.BinaryWriter()
        returnValue = serializeOut.serialize_double(testVal)
        testResult = serializeOut.getByteArray()
        self.assertTrue(returnValue == testVal, msg="Return value does not equal write value.")
        self.assertTrue(testResult == rubric, msg="Bytes serialized do not match the expected output.")

    def test_serialize_string(self):
        testVal = 'BinaryWriter'
        rubric = '\r\x00\x00\x00BinaryWriter\x00'  # four byte size integer '\r\x00\x00\x00' followed by string and terminator ('\x00').
        serializeOut = bWrite.BinaryWriter()
        returnValue = serializeOut.serialize_string(testVal)
        testResult = serializeOut.getByteArray()
        self.assertTrue(returnValue == testVal, msg="Return value does not equal write value.")
        self.assertTrue(testResult == rubric, msg="Bytes serialized do not match the expected output.")

    def test_serialize_sizedstring(self):
        testVal = 'BinaryWriter'
        size = 16
        rubric = 'BinaryWriter\x00\x00\x00\x00'  # 12 char String followed by terminator and padded to 16
        serializeOut = bWrite.BinaryWriter()
        returnValue = serializeOut.serialize_string(testVal, destinationSize=size)
        testResult = serializeOut.getByteArray()
        self.assertTrue(returnValue == testVal, msg="Return value does not equal write value.")
        self.assertTrue(testResult == rubric, msg="Bytes serialized do not match the expected output.")

    def test_serialize_array(self):
        if sys.byteorder == 'little':
            testVal = array.array('d', [1024, 512, 256])
        else:
            testVal = array.array('d', [1024, 512, 256])
            testVal.byteswap()
        sizebytes = testVal.itemsize*len(testVal)
        rubric = '\x00\x00\x00\x00\x00\x00\x90@\x00\x00\x00\x00\x00\x00\x80@\x00\x00\x00\x00\x00\x00p@'
        serializeOut = bWrite.BinaryWriter()
        returnValue = serializeOut.serialize_array(testVal, sizebytes)
        testResult = serializeOut.getByteArray()
        self.assertTrue(returnValue == testVal, msg="Return value does not equal write value.")
        self.assertTrue(testResult == rubric, msg="Bytes serialized do not match the expected output.")

    def test_align(self):
        alignment = 4
        byteVal = 127
        serializeOut = bWrite.BinaryWriter()
        serializeOut.align(alignment)
        self.assertFalse(serializeOut.bytesSerialized(), msg="Align padded a zero length buffer. No alignment required.")

        serializeOut.serialize_byte(byteVal)
        unpadded = serializeOut.bytesSerialized()
        serializeOut.align(alignment)
        padded = serializeOut.bytesSerialized()
        testResult = unpadded != alignment and padded == alignment
        self.assertTrue(testResult, msg="Alignment padding is incorrect.")

    def test_allocateOrdered(self):
        alloc = 8
        serializeOut = bWrite.BinaryWriter()
        serializeOut.allocateOrdered(alloc)
        size = serializeOut.bytesSerialized()
        testResult = size == alloc
        self.assertTrue(testResult, msg="Incorrect number of bytes allocated.")

    def test_seek(self):
        pos = 8
        serializeOut = bWrite.BinaryWriter()
        serializeOut.seek(pos)
        size = serializeOut.bytesSerialized()
        testResult = size == pos
        self.assertTrue(testResult, msg="Seek beyond end did not correctly allocate bytes.")

        newpos = 2
        serializeOut.seek(pos)
        newsize = serializeOut.bytesSerialized()
        reqFalse = newsize == newpos
        reqTrue = newsize == size
        testResult = reqTrue and not reqFalse
        self.assertTrue(testResult, msg="Seek to allocated space changed allocation.")


if __name__ == '__main__':
    unittest.main()
