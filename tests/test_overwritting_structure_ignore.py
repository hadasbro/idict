import unittest

from lib.exceptions import ValueNotAllowedException
from lib.idict import Idict


class TestOverwritteStructure(unittest.TestCase):

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
            "missing_keys": Idict.OPT.IGNORE
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
            {'a': 1, 'b': {'bb1': 2}, 'c': {'cc1': {'ccc1': 3, 'ccc2': {'cccc1': 4}}}}
            '''
            expected_hash = "eydhJzogMSwgJ2InOiB7J2J" \
                            "iMSc6IDJ9LCAnYyc6IHsnY2MxJ" \
                            "zogeydjY2MxJzogMywgJ2NjYzInOiB" \
                            "7J2NjY2MxJzogNH19fX0="
            self.assertEqual(dict6.hash_code(), expected_hash)


if __name__ == '__main__':
    unittest.main()
