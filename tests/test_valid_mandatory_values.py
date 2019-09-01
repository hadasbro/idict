import unittest

from lib.exceptions import MandatoryKeyValueException
from lib.idict import Idict


class TestValidMandatoryValues(unittest.TestCase):
    dict1 = Idict({
        'a': None,
        'b': {
            'bb1': None,
            'bb2': ...
        },
        'c': {
            'cc1': {
                'ccc1': None,
                'ccc2': {
                    'cccc1': ...,
                    'c': None,
                    'cc1': None
                },
                'ccc3': ...
            },
        },
    }, {
        "missing_keys": Idict.OPT.THROW
    })

    def test_validate(self):
        try:
            TestValidMandatoryValues.dict1.validate()
        except MandatoryKeyValueException as ex:
            correct_key = str(ex).find("[b][bb2]")
            res = correct_key != -1
            self.assertTrue(res)

        try:
            TestValidMandatoryValues.dict1['b']['bb2'] = "something"
            TestValidMandatoryValues.dict1.validate()
        except MandatoryKeyValueException as ex:
            correct_key = str(ex).find("[c][cc1][ccc2][cccc1]")
            res = correct_key != -1
            self.assertTrue(res)

        try:
            TestValidMandatoryValues.dict1['c']['cc1']['ccc2']['cccc1'] = "something 2"
            TestValidMandatoryValues.dict1.validate()
        except MandatoryKeyValueException as ex:
            correct_key = str(ex).find("[c][cc1][ccc3]")
            res = correct_key != -1
            self.assertTrue(res)

        try:
            TestValidMandatoryValues.dict1['c']['cc1']['ccc3'] = "something 3"
            TestValidMandatoryValues.dict1.validate()
        except MandatoryKeyValueException:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
            # no more mandatory values


if __name__ == '__main__':
    unittest.main()
