import unittest

from lib.idict import Idict


class TestAdditionalKeysIgnore(unittest.TestCase):
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
        "missing_keys": Idict.OPT.IGNORE
    })

    def test_additional_keys(self):
        # non existing first element
        try:
            TestAdditionalKeysIgnore.dict1['non_existing'] = 1
            TestAdditionalKeysIgnore.dict1['non_existing2']['non_existing3']['non_existing4'] = 2
            TestAdditionalKeysIgnore.dict1['bither_non_existing'] = 4
            TestAdditionalKeysIgnore.dict1['c']['cc1']['ccc1'] = 5

            print(repr(TestAdditionalKeysIgnore.dict1))
        except Exception as ex:
            print(ex)
            print("EEEEEEEEEEEEEEEEEEEEE")
            self.assertTrue(False)
        finally:
            obj_hash = "eydhJzogTm9uZSwgJ2InOiB7J2JiMSc6IE5vb" \
                       "mUsICdiYjInOiBOb25lfSwgJ2MnOiB7J2NjMSc6" \
                       "IHsnY2NjMSc6IDUsICdjY2MyJzogeydjY2NjMSc6" \
                       "IE5vbmUsICdjJzogTm9uZSwgJ2NjMSc6IE5vbmV9LC" \
                       "AnY2NjMyc6IEVsbGlwc2lzfX19"
            self.assertEqual(TestAdditionalKeysIgnore.dict1.hash_code(), obj_hash)


if __name__ == '__main__':
    unittest.main()
