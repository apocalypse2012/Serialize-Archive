import unittest
import Serialize-Archive.BinarySerializer as ser


class fail_stub_serializer(ser.BinarySerializer):

    CALLS_MADE = list()

    def __init__(self):
        super(fail_stub_serializer, self).__init__()


class Serializer_interface(unittest.TestCase):

    def test_instantiate_ABC(self):
        self.assertRaises(TypeError, ser.BinarySerializer)

    def test_instantiate_override_fail(self):
        self.assertRaises(TypeError, fail_stub_serializer)


if __name__ == '__main__':
    unittest.main()
    