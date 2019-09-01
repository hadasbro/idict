import unittest

from lib.exceptions import ValueNotAllowedException
from lib.idict import Idict


class TestOverwritteStructureAllow(unittest.TestCase):

    def test_overwritte_defaults1(self):

        pattern = {
            'a': 1,
            'b': {
                'bb1': 2,
            },
            'c': {
                'cc1': {
                    'ccc1': 3,
                    'ccc2': {
                        'cccc1': 4,
                    },
                },
            },
        }

        opts = {
            "missing_keys": Idict.OPT.ALLOW
        }

        dict6 = Idict(pattern, opts)

        try:
            # structure change is allowed
            dict6['c']['cc1'] = 1
        except ValueNotAllowedException:
            self.assertTrue(False)
        else:
            '''
            dict6.__repr__()
            {'a': 1, 'b': {'bb1': 1}, 'c': {'cc1': 1}}
            '''
            self.assertEqual(dict6.hash_code(), "eydhJzogMSwgJ2InOiB7J2JiMSc6IDJ9LCAnYyc6IHsnY2MxJzogMX19")


if __name__ == '__main__':
    unittest.main()
