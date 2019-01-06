__author__ = "Raymond Stewart"
__copyright__ = "Copyright 2018"
__credits__ = ["Raymond Stewart"]
__license__ = "EULA"
__version__ = "1.0.0"
__maintainer__ = "Raymond Stewart"
__email__ = "info@raymond-stewart.com"

import abc
import struct

class Enum(tuple):
    __getattr__ = tuple.index
    __isabstractmethod__ = False  #HACK: Required to use in abc property. Prevents indexing tuple by this method name.


class BinarySerializer(object):
    __metaclass__ = abc.ABCMeta

    ENDIANNESS = Enum(['BIG', 'LITTLE'])

    DEFAULT_ENDIANNESS = ENDIANNESS.LITTLE
    DEFAULT_TARGET_ALIGN_BOOL = 1
    DEFAULT_TARGET_ALIGN_BYTE = 1
    DEFAULT_TARGET_ALIGN_SHORT = 2
    DEFAULT_TARGET_ALIGN_INT = 4
    DEFAULT_TARGET_ALIGN_LONG = 8
    DEFAULT_TARGET_ALIGN_FLOAT = 4
    DEFAULT_TARGET_ALIGN_DOUBLE = 8
    DEFAULT_TARGET_SIZE_INT = 4

    def __init__(self):
        self.m_endianness = self.DEFAULT_ENDIANNESS
        self.m_targetAlignBool = self.DEFAULT_TARGET_ALIGN_BOOL
        self.m_targetAlignByte = self.DEFAULT_TARGET_ALIGN_BYTE
        self.m_targetAlignShort = self.DEFAULT_TARGET_ALIGN_SHORT
        self.m_targetAlignInt = self.DEFAULT_TARGET_ALIGN_INT
        self.m_targetAlignLong = self.DEFAULT_TARGET_ALIGN_LONG
        self.m_targetAlignFloat = self.DEFAULT_TARGET_ALIGN_FLOAT
        self.m_targetAlignDouble = self.DEFAULT_TARGET_ALIGN_DOUBLE
        self.m_targetSizeInt = self.DEFAULT_TARGET_SIZE_INT

        self.m_structBool = struct.Struct(self.endianness + '?')
        self.m_structByte = struct.Struct(self.endianness + 'b')
        self.m_structShort = struct.Struct(self.endianness + 'h')
        self.m_structInt = struct.Struct(self.endianness + 'i')
        self.m_structLong = struct.Struct(self.endianness + 'q')
        self.m_structFloat = struct.Struct(self.endianness + 'f')
        self.m_structDouble = struct.Struct(self.endianness + 'd')

        self.m_alignByFmt = {'?': self.DEFAULT_TARGET_ALIGN_BOOL,
                        'b': self.DEFAULT_TARGET_ALIGN_BYTE,
                        'h': self.DEFAULT_TARGET_ALIGN_SHORT,
                        'i': self.DEFAULT_TARGET_ALIGN_INT,
                        'l': self.DEFAULT_TARGET_ALIGN_INT,
                        'q': self.DEFAULT_TARGET_ALIGN_LONG,
                        'f': self.DEFAULT_TARGET_ALIGN_FLOAT,
                        'd': self.DEFAULT_TARGET_ALIGN_DOUBLE}

    @property
    def endianness(self):
        return ('>' if self.m_endianness == self.ENDIANNESS.BIG else '<')

    @abc.abstractmethod
    def bytesSerialized(self):
        pass

    @abc.abstractmethod
    def align(self, boundary ):
        pass

    @abc.abstractmethod
    def seek(self, pos ):
        pass

    @abc.abstractmethod
    def serialize_bool(self, value):
        pass

    @abc.abstractmethod
    def serialize_byte(self, value):
        pass

    @abc.abstractmethod
    def serialize_short(self, value):
        pass

    @abc.abstractmethod
    def serialize_int(self, value):
        pass

    @abc.abstractmethod
    def serialize_long(self, value):
        pass

    @abc.abstractmethod
    def serialize_string(self, value, destinationSize = None):
        pass

    @abc.abstractmethod
    def serialize_float(self, value):
        pass

    @abc.abstractmethod
    def serialize_double(self, value):
        pass

    @abc.abstractmethod
    def serialize_array(self, value):
        pass

