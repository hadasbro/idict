from lib.idict import Idict

if __name__ == '__main__':
    pattern = {
        'test': None,
        'a': None,
        'b': {
            'ins': ...,
            'another': ...,
            'one_more': None
        },
        'c': {
            'c1': {
                'c2': ...
            }
        },
        'j': {
            'k2': {
                'a': ...,
                'b': ...
            },
            'k3': {
                'c': ...
            },
            'k4': {
                'cg': ...
            }
        }
    }

    d = Idict(pattern, {
        "missing_keys": Idict.OPT.KEY_IGNORE,
        "ellipsis_as_mandatory": True
    })

    # d['a'] = 1
    # # d['a']['b'] = 12
    # d['b']['c'] = 55
    # d['j']['k']['a'] = 112

    d['a'] = 1
    d['b']['ins'] = {'xx': {'y': 1234}}
    d['j']['k4']['cg'] = "overwritten"

    d['b']['another'] = 2
    d['b']['xxdisallowed'] = 2

    # d['b']['fake_key1'] = 2
    # d['b']['fake_key2']['fake_key_deeper'] = 2
    # d['c']['c1']['c2'] = 3

    # d['b']['one_more']['fake_overwritting_key'] = 3 # KeyOnNonDictException: [Element Error]

    # d['c']['c1']['fake_key21'] = 4
    # d['c']['c1']['fake_key']['fake_key2']['fake_key3']['fake_key']['fake_key'] = 5
    # d['c']['fake_key44'] = 6
    # d['c']['fake_key2'] = 7
    # d['c']['fake_key']['c2'] = 8

    # d['fake_key7'] = 9

    # d['fake_key8']['a'] = 10
    # d['fake_key81']['aaa'] = 11
    # d['fake_key82']['aaa']['bbb'] = 12
    #
    # d['fake_key9']['aaa']['bbb'] = 13
    # d['j']['k2']['a'] = 1
    # d['j']['k3']['c'] = 2
    # d['j']['k4']['cg'] = 3
    # d['j']['k4']['cgx'] = 4
    # d['j']['k4']['cgx2'] = 41

    # d['j']['xxxxxxxxxx']['cgx2'] = 41
    # d['j']['k4xxxxxxxxxx']['cgx2'] = 41
    # d['j']['aaaaa']['cgx2'] = 41
    # d['xxxxxxxxxxxxxxxxxxxxxxxx']['aaaaa']['cgx2'] = 41
    # d['xxxxxxxxxxxxxxxxxxxxxxxx'] = 41

    # print(d.validate())

    # print("----------")
    # print(d['j']['k4']['cgx'])
    # print((d))
    print(" FINAL RESULT >>> ", repr(d))
