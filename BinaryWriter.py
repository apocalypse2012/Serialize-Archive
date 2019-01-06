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


SHORT_MIN = -32767
SHORT_MAX = 32767

class BinaryWriter(BinarySerializer.BinarySerializer):

    def __init__(self):
        super(BinaryWriter, self).__init__()
        self.m_buffer = ctypes.create_string_buffer(0)

    def align(self, boundary):
        bufSize = ctypes.sizeof(self.m_buffer)
        
        howFarIn = bufSize % boundary
        pad = (boundary - howFarIn)
        if not howFarIn:
            return
        fmt = self.endianness + str(pad) + 'x'
        self.allocateOrdered(pad)
        struct.pack_into(fmt, self.m_buffer, bufSize)

    def seek(self, pos):
        bufSize = ctypes.sizeof(self.m_buffer)
        
        paddingNeeded = pos - bufSize
        if paddingNeeded > 0:
            fmt = self.endianness + str(paddingNeeded) + 'x'
            self.allocateOrdered(paddingNeeded)
            struct.pack_into(fmt, self.m_buffer, bufSize)

    def bytesSerialized(self):
        return ctypes.sizeof(self.m_buffer)

    def allocateOrdered(self, size):
        bufSize = ctypes.sizeof(self.m_buffer)
        bufSize += size
        ctypes.resize(self.m_buffer, bufSize)

    def serialize_bool(self, value):
        self.align(self.m_targetAlignBool)
        bufSize = ctypes.sizeof(self.m_buffer)
        data = 1 if value else 0
        self.allocateOrdered(self.m_targetAlignBool)
        self.m_structBool.pack_into(self.m_buffer, bufSize, data)
        return value

    def serialize_byte(self, value):
        self.align(self.m_targetAlignByte)
        bufSize = ctypes.sizeof(self.m_buffer)
        self.allocateOrdered(self.m_targetAlignByte)
        self.m_structByte.pack_into(self.m_buffer, bufSize, value)
        return value

    def serialize_short(self, value):
        self.align(self.m_targetAlignShort)
        bufSize = ctypes.sizeof(self.m_buffer)
        self.allocateOrdered(self.m_targetAlignShort)
        self.m_structShort.pack_into(self.m_buffer, bufSize, value)
        return value

    def serialize_int(self, value):
        self.align(self.m_targetAlignInt)

        assert(self.m_targetSizeInt == 2 or
               self.m_targetSizeInt == 4 or
               self.m_targetSizeInt == 8)

        if self.m_targetSizeInt == 2:
            if value < SHORT_MIN or value > SHORT_MAX:
                raise(TypeError("Write int exceeds platform short size"))
            fmt = self.endianness + 'h'
            bufSize = ctypes.sizeof(self.m_buffer)
            
            self.allocateOrdered(2)
            struct.pack_into(fmt, self.m_buffer, bufSize, value)
        elif self.m_targetSizeInt == 8:
            fmt = self.endianness + 'q'
            bufSize = ctypes.sizeof(self.m_buffer)
            self.allocateOrdered(8)
            struct.pack_into(fmt, self.m_buffer, bufSize, value)
        else:
            fmt = self.endianness + 'l'
            bufSize = ctypes.sizeof(self.m_buffer)
            self.allocateOrdered(4)
            struct.pack_into(fmt, self.m_buffer, bufSize, value)
        return value

    def serialize_long(self, value):
        self.align(self.m_targetAlignLong)
        bufSize = ctypes.sizeof(self.m_buffer)
        self.allocateOrdered(8)
        self.m_structLong.pack_into(self.m_buffer, bufSize, value)
        return value

    def serialize_string(self, value, destinationSize = None):
        strVal = ctypes.create_string_buffer(value)  # adds string terminator.
        strLen = ctypes.sizeof(strVal)

        if destinationSize:
            if strLen > destinationSize:
                raise(ValueError("String is larger than size specified"))
            bufSize = ctypes.sizeof(self.m_buffer)
            fmt = self.endianness + str(strLen) + 's'
            self.allocateOrdered(strLen)
            struct.pack_into(fmt, self.m_buffer, bufSize, value)

            bufSize = ctypes.sizeof(self.m_buffer)
            unfilled = destinationSize - strLen
            fmt = self.endianness + str(unfilled) + 'x'
            self.allocateOrdered(unfilled)
            struct.pack_into(fmt, self.m_buffer, bufSize)

        else:
            self.serialize_int(strLen)
            bufSize = ctypes.sizeof(self.m_buffer)
            fmt = self.endianness + str(strLen) + 's'
            self.allocateOrdered(strLen)
            struct.pack_into(fmt, self.m_buffer, bufSize, value)
        return value


    def serialize_float(self, value):
        self.align(self.m_targetAlignFloat)
        bufSize = ctypes.sizeof(self.m_buffer)
        self.allocateOrdered(self.m_targetAlignFloat)
        self.m_structFloat.pack_into(self.m_buffer, bufSize, value)
        return value

    def serialize_double(self, value):
        self.align(self.m_targetAlignDouble)
        bufSize = ctypes.sizeof(self.m_buffer)
        self.allocateOrdered(self.m_targetAlignDouble)
        self.m_structDouble.pack_into(self.m_buffer, bufSize, value)
        return value

    def serialize_array(self, value, size):
        # unpack array value
        typeCode = value.typecode
        fmt = self.endianness + str(len(value)) + typeCode
        arrayVal = struct.unpack_from(fmt, value, 0)

        # pack array value into buffer
        self.align(self.m_alignByFmt[typeCode])
        bufSize = ctypes.sizeof(self.m_buffer)
        self.allocateOrdered(size)
        struct.pack_into(fmt, self.m_buffer, bufSize, *arrayVal)
        return value


    def getByteArray(self):
        return self.m_buffer.raw

if __name__ == '__main__':
    writer = BinaryWriter()
    writer.serialize_boolean(False)
    writer.serialize_boolean(True)
    writer.serialize_short(255)
    writer.serialize_long(4096)
    writer.serialize_string('shit', destinationSize=10)
    writer.serialize_string('shit')
    import pprint
    pprint.pprint(writer.getByteArray())
