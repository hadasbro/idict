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
            "missing_keys": Idict.OPT.KEY_THROW,
            "ellipsis_as_mandatory": True
        }

        dict6 = Idict(pattern, opts)

        res = False
        try:
            # this is notmal value set (overwritte defaule value)
            dict6['b']['bb1'] = 1
        except ValueNotAllowedException as ex:
            correct_key = str(ex).find("bb1")
            res = correct_key != -1
        else:
            res = False
        finally:
            self.assertFalse(res)

        res = False
        try:
            # illegal structure change interface defines dict
            # under ['c']['cc1'] but we are trying to set integer here
            dict6['c']['cc1'] = 1
        except ValueNotAllowedException as ex:
            correct_key = str(ex).find("<cc1>")
            res = correct_key != -1
        else:
            res = False
        finally:
            self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()
