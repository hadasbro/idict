import unittest

from lib.exceptions import KeyNotAllowedException
from lib.idict import Idict


class TestAdditionalKeysThrow(unittest.TestCase):
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
        "missing_keys": Idict.OPT.THROW
    })

    def test_non_existing_first_element(self):
        # non existing first element
        res = False
        try:
            TestAdditionalKeysThrow.dict1['non_existing'] = 1
        except KeyNotAllowedException as ex:
            correct_key = str(ex).find("<non_existing>")
            res = correct_key != -1
        finally:
            self.assertTrue(res)

    def test_non_existing_first_element_and_deeper_element(self):

        # non existing first element and deeper element
        res = False
        try:
            TestAdditionalKeysThrow.dict1['non_existing2']['non_existing3'] = 1
        except KeyNotAllowedException as ex:
            correct_key = str(ex).find("<non_existing2>")
            res = correct_key != -1
        finally:
            self.assertTrue(res)

    def test_non_existing_first_element_and_deeper_element2(self):
        # non existing first element and deeper element
        res = False
        try:
            TestAdditionalKeysThrow.dict1['non_existing5']['non_existing3']['none_existing4'] = 1
        except KeyNotAllowedException as ex:
            correct_key = str(ex).find("<non_existing5>")
            res = correct_key != -1
        finally:
            self.assertTrue(res)

    def test_existing_key_and_existing_key_deeper_and_as_the_last_element_first(self):
        # existing key and existing key deeper and as the last element
        res = False

        try:
            TestAdditionalKeysThrow.dict1['c']['non_existing8'] = 1
        except KeyNotAllowedException as ex:
            correct_key = str(ex).find("<non_existing8>")
            res = correct_key != -1
        finally:
            self.assertTrue(res)

    def test_existing_key_and_existing_key_deeper_and_as_the_last_element_sec(self):
        # existing key and existing key deeper and as the last element
        res = False

        try:
            TestAdditionalKeysThrow.dict1['c']['cc1']['non_existing'] = 1
        except KeyNotAllowedException as ex:
            correct_key = str(ex).find("<non_existing>")
            res = correct_key != -1
        finally:
            self.assertTrue(res)

    def test_existing_key_and_existing_key_deeper_and_as_the_last_element_third(self):
        # existing key and existing key deeper and as the last element
        res = False

        try:
            TestAdditionalKeysThrow.dict1['c']['another_non_existing8']['ccc1'] = 1
        except KeyNotAllowedException as ex:
            correct_key = str(ex).find("<another_non_existing8>")
            res = correct_key != -1
        finally:
            self.assertTrue(res)

    def test_existing_key_at_the_beginning_and_multiple_non_existing_keys_later(self):
        # existing key at the beginning and multiple non existing keys later
        res = False

        try:
            TestAdditionalKeysThrow.dict1['c']['non_existing10']['non_existing11']['non_existing12']['non_existing13'] = 1
        except KeyNotAllowedException as ex:
            correct_key = str(ex).find("<non_existing10>")
            res = correct_key != -1
        finally:
            self.assertTrue(res)

    def test_mix_of_non_existing_and_existing_keys(self):
        # mix of non existing and existing keys
        res = False

        try:
            res = False
            TestAdditionalKeysThrow.dict1['c']['non_existing11']['c1']['ccc1']['non_existing13'] = 1
        except KeyNotAllowedException as ex:
            correct_key = str(ex).find("<non_existing11>")
            res = correct_key != -1
        finally:
            self.assertTrue(res)

    def test_non_existing_key_in_the_middle_of_existing_keys(self):
        # non existing key in the middle of existing keys
        res = False
        try:
            TestAdditionalKeysThrow.dict1['c']['cc1']['non_existing15']['cccc1'] = 5
        except KeyNotAllowedException as ex:
            correct_key = str(ex).find("<non_existing15>")
            res = correct_key != -1
        finally:
            self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()
