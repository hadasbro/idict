import unittest

from lib.idict import Idict


class TestOverwritteDefault(unittest.TestCase):
    dict2 = Idict({
        'a': 'default value <a>',
        'g': 'default value <g>',
        'b': {
            'bb1': 'default value <b><bb1>',
            'bb2': 'default value <b><bb2>',
        },
        'c': {
            'cc1': {
                'ccc1': 'default value <c><cc1><ccc1>',
                'ccc2': {
                    'cccc1': 'default value <c><cc1><ccc2><cccc1>',
                    'c': 'default value <c><cc1><ccc2><c>',
                    'cc1': 'default value <c><cc1><ccc2><cc1>',
                },
            },
        },
    }, {
        "missing_keys": Idict.OPT.KEY_THROW,
        "ellipsis_as_mandatory": True
    })

    pattern2 = {
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

    dict3 = Idict(pattern2, opts)

    dict4 = Idict(pattern2, opts)

    dict5 = Idict(pattern2, opts)

    def test_overwritte_defaults1(self):
        TestOverwritteDefault.dict2['a'] = "overwritten value <a>"
        TestOverwritteDefault.dict2['b']['bb1'] = "overwritten value <b><bb1>"
        TestOverwritteDefault.dict2['c']['cc1']['ccc1'] = "overwritten value <c><cc1><ccc1>"
        TestOverwritteDefault.dict2['c']['cc1']['ccc2']['cccc1'] = "default value <c><cc1><ccc2><cccc1>"

        self.assertEqual(TestOverwritteDefault.dict2['a'], 'overwritten value <a>')

        self.assertEqual(TestOverwritteDefault.dict2['g'], 'default value <g>')

        self.assertEqual(TestOverwritteDefault.dict2['b']['bb1'], 'overwritten value <b><bb1>')

        self.assertEqual(TestOverwritteDefault.dict2['c']['cc1']['ccc1'], 'overwritten value <c><cc1><ccc1>')

        self.assertEqual(TestOverwritteDefault.dict2['c']['cc1']['ccc2']['c'], 'default value <c><cc1><ccc2><c>')

        self.assertEqual(TestOverwritteDefault.dict2['c']['cc1']['ccc2']['cc1'], 'default value <c><cc1><ccc2><cc1>')

        self.assertEqual(TestOverwritteDefault.dict2['c']['cc1']['ccc2']['cccc1'],
                         'default value <c><cc1><ccc2><cccc1>')

        self.assertEqual(TestOverwritteDefault.dict2['c']['cc1']['ccc2']['c'], 'default value <c><cc1><ccc2><c>')

        self.assertEqual(TestOverwritteDefault.dict2['c']['cc1']['ccc2']['cc1'], 'default value <c><cc1><ccc2><cc1>')

    def test_overwritte_defaults2(self):
        TestOverwritteDefault.dict3['a'] = 11
        TestOverwritteDefault.dict3['b']['bb1'] = 22
        TestOverwritteDefault.dict3['c']['cc1']['ccc1'] = 33
        TestOverwritteDefault.dict3['c']['cc1']['ccc2']['cccc1'] = 44

        TestOverwritteDefault.dict4['a'] = 11
        TestOverwritteDefault.dict4['c']['cc1']['ccc1'] = 33

        self.assertEqual(TestOverwritteDefault.dict3['a'], 11)
        self.assertEqual(TestOverwritteDefault.dict3['b']['bb1'], 22)
        self.assertEqual(TestOverwritteDefault.dict3['c']['cc1']['ccc1'], 33)
        self.assertEqual(TestOverwritteDefault.dict3['c']['cc1']['ccc2']['cccc1'], 44)
        self.assertEqual(TestOverwritteDefault.dict4['a'], 11)
        self.assertEqual(TestOverwritteDefault.dict4['b']['bb1'], 2)
        self.assertEqual(TestOverwritteDefault.dict4['c']['cc1']['ccc1'], 33)
        self.assertEqual(TestOverwritteDefault.dict4['c']['cc1']['ccc2']['cccc1'], 4)
        self.assertEqual(TestOverwritteDefault.dict5['a'], 1)
        self.assertEqual(TestOverwritteDefault.dict5['b']['bb1'], 2)
        self.assertEqual(TestOverwritteDefault.dict5['c']['cc1']['ccc1'], 3)
        self.assertEqual(TestOverwritteDefault.dict5['c']['cc1']['ccc2']['cccc1'], 4)


if __name__ == '__main__':
    unittest.main()
