import unittest
import Serialize-Archive.BinaryReader as bRead
import array
import sys


class Serialize_to_Binary(unittest.TestCase):

    def test_serialize_bool(self):
        testVal = '\x01'
        input = False
        rubric = True
        serializeIn = bRead.BinaryReader(testVal)
        returnValue = serializeIn.serialize_bool(input)
        self.assertTrue(returnValue == rubric, msg="Return value does not equal expected value.")

    def test_serialize_byte(self):
        testVal = '\x7f'
        rubric = 127
        serializeIn = bRead.BinaryReader(testVal)
        returnValue = serializeIn.serialize_byte(int())
        self.assertTrue(returnValue == rubric, msg="Return value does not equal expected value.")

    def test_serialize_short(self):
        testVal = '\x7f\x00'
        rubric = 127
        serializeIn = bRead.BinaryReader(testVal)
        returnValue = serializeIn.serialize_short(int())
        self.assertTrue(returnValue == rubric, msg="Return value does not equal expected value.")

    def test_serialize_int2(self):
        testVal = '\x7f\x00'
        rubric = 127
        serializeIn = bRead.BinaryReader(testVal)
        serializeIn.m_targetSizeInt = 2
        returnValue = serializeIn.serialize_int(int())
        self.assertTrue(returnValue == rubric, msg="Return value does not equal expected value.")

    def test_serialize_int4(self):
        testVal = '\x7f\x00\x00\x00'
        rubric = 127
        serializeIn = bRead.BinaryReader(testVal)
        serializeIn.m_targetSizeInt = 4
        returnValue = serializeIn.serialize_int(int())
        self.assertTrue(returnValue == rubric, msg="Return value does not equal expected value.")

    def test_serialize_int8(self):
        testVal = '\x7f\x00\x00\x00\x00\x00\x00\x00'
        rubric = 127
        serializeIn = bRead.BinaryReader(testVal)
        serializeIn.m_targetSizeInt = 8
        returnValue = serializeIn.serialize_int(int())
        self.assertTrue(returnValue == rubric, msg="Return value does not equal expected value.")

    def test_serialize_long(self):
        testVal = '\x7f\x00\x00\x00\x00\x00\x00\x00'
        rubric = 127L
        serializeIn = bRead.BinaryReader(testVal)
        returnValue = serializeIn.serialize_long(long())
        self.assertTrue(returnValue == rubric, msg="Return value does not equal expected value.")

    def test_serialize_float(self):
        testVal = '\xda\x0fI@'
        rubric = 3.1415926
        serializeIn = bRead.BinaryReader(testVal)
        returnValue = serializeIn.serialize_float(float())
        self.assertAlmostEqual(rubric, returnValue, places=4, msg="Return value does not equal expected value.")

    def test_serialize_double(self):
        testVal = 'J\xd8\x12M\xfb!\t@'
        rubric = 3.1415926
        serializeIn = bRead.BinaryReader(testVal)
        returnValue = serializeIn.serialize_double(testVal)
        self.assertTrue(returnValue == rubric, msg="Return value does not equal expected value.")

    def test_serialize_string(self):
        testVal = '\r\x00\x00\x00BinaryReader\x00'  # four byte size integer '\r\x00\x00\x00' followed by string and terminator ('\x00').
        rubric = 'BinaryReader'
        serializeIn = bRead.BinaryReader(testVal)
        returnValue = serializeIn.serialize_string(testVal)
        self.assertTrue(returnValue == rubric, msg="Return value does not equal expected value.")

    def test_serialize_sizedstring(self):
        testVal = 'BinaryReader\x00\x00\x00\x00'  # 12 char String followed by terminator and padded to 16
        size = 16
        rubric = 'BinaryReader'
        serializeIn = bRead.BinaryReader(testVal)
        returnValue = serializeIn.serialize_string(testVal, destinationSize=size)
        self.assertTrue(returnValue == rubric, msg="Return value does not equal expected value.")

    def test_serialize_array(self):
        testVal = '\x00\x00\x00\x00\x00\x00\x90@\x00\x00\x00\x00\x00\x00\x80@\x00\x00\x00\x00\x00\x00p@'
        if sys.byteorder == 'little':
            rubric = array.array('d', [1024, 512, 256])
        else:
            rubric = array.array('d', [1024, 512, 256])
            rubric.byteswap()
        sizebytes = rubric.itemsize*len(rubric)
        serializeIn = bRead.BinaryReader(testVal)
        returnValue = serializeIn.serialize_array(array.array('d'), sizebytes)
        self.assertTrue(returnValue == rubric, msg="Return value does not equal expected value.")

    def test_align(self):
        testVal = '\x7f\x00\x00\x00\x00\x00\x00\x00'
        alignment = 8
        byteVal = 127

        serializeIn = bRead.BinaryReader(testVal)
        serializeIn.align(alignment)
        self.assertFalse(serializeIn.bytesSerialized(), msg="Align padded a zero length buffer. No alignment required.")

        serializeIn.serialize_byte(byteVal)
        unpadded = serializeIn.bytesSerialized()
        serializeIn.align(alignment)
        padded = serializeIn.bytesSerialized()
        testResult = unpadded != alignment and padded == alignment
        self.assertTrue(testResult, msg="Alignment padding is incorrect.")

    def test_getByteArray(self):
        testVal = '\x7f\x00\x00\x00\x00\x00\x00\x00'
        serializeIn = bRead.BinaryReader(testVal)
        testResult = serializeIn.getByteArray() == testVal
        self.assertTrue(testResult, msg="ByteArray Output is not equal to ByteArray Input.")

    def test_seek(self):
        pos = 8
        testVal = '\x7f\x00\x00\x00\x00\x00\x00\x00'
        serializeIn = bRead.BinaryReader(testVal)
        serializeIn.seek(pos)
        size = serializeIn.bytesSerialized()
        testResult = size == pos
        self.assertTrue(testResult, msg="Seek did not update buffer position.")



if __name__ == '__main__':
    unittest.main()
