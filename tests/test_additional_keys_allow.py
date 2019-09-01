import unittest

from lib.idict import Idict


class TestAdditionalKeysAllow(unittest.TestCase):
    dict1 = Idict({
        'a': None,
        'b': {
            'bb1': None,
            'bb2': None
        },
        'c': {
            'cc1': {
                'ccc1': None,
                'ccc2': {
                    'cccc1': None,
                    'c': None,
                    'cc1': None
                },
                'ccc3': ...
            },
        },
    }, {
        "missing_keys": Idict.OPT.ALLOW
    })

    def test_additional_keys(self):
        # non existing first element
        try:
            TestAdditionalKeysAllow.dict1['non_existing'] = 1
            TestAdditionalKeysAllow.dict1['non_existing2']['non_existing3']['non_existing4'] = 2
            TestAdditionalKeysAllow.dict1['bither_non_existing'] = 4
            TestAdditionalKeysAllow.dict1['c']['cc1']['ccc1'] = 5

        except Exception as ex:
            print(ex)
            self.assertTrue(False)
        finally:
            obj_hash = "eydhJzogTm9uZSwgJ2InOiB7J2JiMSc6IE5vbmUsICdiY" \
                   "jInOiBOb25lfSwgJ2MnOiB7J2NjMSc6IHsnY2NjMSc6IDUs" \
                   "ICdjY2MyJzogeydjY2NjMSc6IE5vbmUsICdjJzogTm9uZSwgJ" \
                   "2NjMSc6IE5vbmV9LCAnY2NjMyc6IEVsbGlwc2lzfX0sICdub25" \
                   "fZXhpc3RpbmcnOiAxLCAnbm9uX2V4aXN0aW5nMic6IHsnbm9uX" \
                   "2V4aXN0aW5nMyc6IHsnbm9uX2V4aXN0aW5nNCc6IDJ9fSwgJ2" \
                   "JpdGhlcl9ub25fZXhpc3RpbmcnOiA0fQ=="
            self.assertEqual(TestAdditionalKeysAllow.dict1.hash_code(), obj_hash)


if __name__ == '__main__':
    unittest.main()
