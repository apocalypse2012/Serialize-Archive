__author__ = "Raymond Stewart"
__copyright__ = "Copyright 2018"
__credits__ = ["Raymond Stewart"]
__license__ = "EULA"
__version__ = "1.0.0"
__maintainer__ = "Raymond Stewart"
__email__ = "info@raymond-stewart.com"

from . import BinarySerializer
import struct
import ctypes
import array
import sys


class BinaryReader(BinarySerializer.BinarySerializer):

    def __init__(self, bytes):
        super(BinaryReader, self).__init__()
        self.m_buffer = bytes
        self.m_pos = 0

    def align(self, boundary):
        howFarIn = self.m_pos % boundary
        if not howFarIn:
            return
        self.m_pos += (boundary - howFarIn)

    def seek(self, pos):
        self.m_pos = pos

    def bytesSerialized(self):
        return self.m_pos

    def serialize_bool(self, value):
        self.align(self.m_targetAlignBool)
        retVal = False if self.m_structBool.unpack_from(self.m_buffer, self.m_pos) == 0 else True
        self.m_pos += self.m_targetAlignBool
        return retVal

    def serialize_byte(self, value):
        self.align(self.m_targetAlignByte)
        retVal = self.m_structByte.unpack_from(self.m_buffer, self.m_pos)[0]
        self.m_pos += self.m_targetAlignByte
        return retVal

    def serialize_short(self, value):
        self.align(self.m_targetAlignShort)
        retVal = self.m_structShort.unpack_from(self.m_buffer, self.m_pos)[0]
        self.m_pos += self.m_targetAlignShort
        return retVal

    def serialize_int(self, value):
        self.align(self.m_targetAlignInt)
        assert(self.m_targetSizeInt == 2 or
               self.m_targetSizeInt == 4 or
               self.m_targetSizeInt == 8)

        if self.m_targetSizeInt == 2:
            fmt = self.endianness + 'h'
            retVal = struct.unpack_from(fmt, self.m_buffer, self.m_pos)[0]
            self.m_pos += 2
            return retVal
        elif self.m_targetSizeInt == 8:
            fmt = self.endianness + 'q'
            retVal = struct.unpack_from(fmt, self.m_buffer, self.m_pos)[0]
            self.m_pos += 8
            return retVal
        else:
            fmt = self.endianness + 'l'
            retVal = struct.unpack_from(fmt, self.m_buffer, self.m_pos)[0]
            self.m_pos += 4
            return retVal

    def serialize_long(self, value):
        self.align(self.m_targetAlignLong)
        retVal = self.m_structLong.unpack_from(self.m_buffer, self.m_pos)[0]
        self.m_pos += self.m_targetAlignLong
        return retVal

    def serialize_string(self, value, destinationSize = None):
        if not destinationSize:
            destinationSize = self.serialize_int(None)
        fmt = self.endianness + str(destinationSize) + 's'
        retVal = struct.unpack_from(fmt, self.m_buffer, self.m_pos)[0]
        retVal = ctypes.c_char_p(retVal)
        self.m_pos += destinationSize
        return retVal.value

    def serialize_float(self, value):
        self.align(self.m_targetAlignFloat)
        retVal = self.m_structFloat.unpack_from(self.m_buffer, self.m_pos)[0]
        self.m_pos += self.m_targetAlignFloat
        return retVal

    def serialize_double(self, value):
        self.align(self.m_targetAlignDouble)
        retVal = self.m_structDouble.unpack_from(self.m_buffer, self.m_pos)[0]
        self.m_pos += self.m_targetAlignDouble
        return retVal

    def serialize_array(self, value, size):
        if (size % value.itemsize):
            raise ValueError("Array byte size must be evenly divisible by type byte size.\nArrayBytes {}, TypeByte {}".format(size,value.itemsize))

        # identify reqs
        arrayCount = int(size / value.itemsize)
        typeCode = value.typecode

        # unpack from buffer
        self.align(self.m_alignByFmt[typeCode])
        fmt = self.endianness + str(arrayCount) + typeCode
        data = struct.unpack_from(fmt, self.m_buffer, self.m_pos)
        self.m_pos += size

        # pack into array value
        retVal = array.array(typeCode, data)
        return retVal

    def getByteArray(self):
        return self.m_buffer
