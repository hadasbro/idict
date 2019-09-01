# I - Dict

![picture](https://img.shields.io/badge/Python-3.7.0%2B-brightgreen)
![picture](https://img.shields.io/badge/License-GNU%20GPL%203.0-blue)

**Dictionary with declared structure in Python**

Tiny extension for [defaultdict](https://docs.python.org/3.3/library/collections.html#collections.defaultdict) Python's class. 
Use this library if you need to ensure or force concrete 
structure for your dictionary and use it as normal dictionary then.

---

## Install

Install from sources.

First stable and tested version will be added to PyPi soon.

---

## Overview

You can provide desired dictionary's structure and specify 
action for non desired usage e.g. specify action if someone 
uses unexpected key or value.

You can also specify required and/or default values for specified keys.

#### General usage
```python
desired_default_structure = {
    'a': 1,
    'c': None
}

options = {
    "missing_keys": Idict.OPT.THROW,
    "ellipsis_as_mandatory": True
}

my_dict = Idict(desired_default_structure, options)

my_dict['a'] = 1

print(repr(my_dict))
# {'a': 1, 'c': None}
```

#### Options

**[ missing_keys ]** - action if unspecified key usage
```python
options = {
    "missing_keys": Idict.OPT.ALLOW
}
```
possible options: `Idict.OPT.`
- `ALLOW` [default value] - allow all other keys and just add to the dictionary.
- `IGNORE` - ignore keys not available in specified interface and allow only specified keys. Always keep the same, desired structure. Ignore tries to change dictionary structure.
- `THROW` - throw an exception `KeyNotAllowedException` if someone tries to set key-value for unspecified key. 
Throw an exception `ValueNotAllowedException` if someone tries to change specified key-value structure. 
See example below.
    
    ```python
    my_dict = Idict({'a': {'aa': {'aaa': 1}}}, options={"missing_keys": Idict.OPT.THROW})
    my_dict['a']['aa'] = 123
    
    '''
    ValueNotAllowedException: 
    [Value Error] Trying to set value <123> for object , key <aa> 
    but in provided interface there is a dictionary under this key - {'aa': {'aaa': 1}}.
    You cannot change expected objects structure
    '''
    ```

**[ ellipsis_as_mandatory ]** - [default = True] use Ellipsis (`...`) as a tag for mandatory keys.  
If this option is settled to `True` then, upon validation, library will check if every key with `Ellipsis` value has new value settled. 
Dictionary will be valid as long as every value tagged by `...` has new value. Otherwise `dict.validate()` will throw an excaption `MandatoryKeyValueException`.
```python
options = {
    "ellipsis_as_mandatory": True
}
```
possible options: 
- True
- False

Example:
```python
# use Ellipsis - ... as a tag for mandatory values
my_dict = Idict({'a': {'aa': None}, 'b': ...}, options={"ellipsis_as_mandatory": True})

my_dict.validate()

# THROWS:
# MandatoryKeyValueException: Key value for key [b]
# is mandatory. Set value for this key or set default value in provided interface. 

my_dict['b'] = "anything"

my_dict.validate()
# OK, no exception, result = True
```



## Examples

+ Allow specified and unspecified keys:

    Default structure and default values are specified in advance.
    We allow other key-value pairs, not only specified ones.

    ```python
    my_dict = Idict({
        'a': 1,
        'b': 2,
        'c': {
            'cc': 3,
        },
        'd': {
            'dd': {
                'ddd': 4
            },
        },
    })
    
    # set/overwrite some values
    my_dict['a'] = 11
    my_dict['c']['cc'] = 33
    my_dict['d']['dd']['new-value'] = 44
    my_dict['e']['ee'] = 55
    
    print(repr(my_dict))
    # {'a': 11, 'b': 2, 'c': {'cc': 33}, 'd': {'dd': {'ddd': 4, 'new-value': 44}}, 'e': {'ee': 55}}
    ```


+ Ignore unexpected keys:
    
    Allow only specified structure, ignore all other key-value pairs.
        
    ```python
    my_dict = Idict({
        'a': 1,
        'c': {
            'cc1': 3,
            'cc2': 4,
        }
    }, {
        "missing_keys": Idict.OPT.IGNORE,
    })
    
    # set/overwrite some values
    my_dict['a'] = 11
    my_dict['b'] = 22
    my_dict['c']['cc1'] = 33
    my_dict['d'] = 55
    
    
    print(repr(my_dict))
    # {'a': 11, 'c': {'cc1': 33, 'cc2': 4}}
    ```

+ Allow only specified keys usage or throw an exception `KeyNotAllowedException`
    
    Throw an exception (KeyNotAllowedException) in case of trying to set value for disallowed key:
       
    ```python
    dict1 = Idict({
        'a': None,
        'b': {
            'bb1': None,
            'bb2': None
        }
    }, {
        "missing_keys": Idict.OPT.THROW
    })
    
    try:
       dict1['non_existing_key'] = "value"
    except KeyNotAllowedException as ex:
        print(ex)
        # [Key Error] You are trying to set value 
        # for key  for your Idict 
        #  but this key is disallowed 
        # and doesnt exist in the provided interface
    ```
        
+ Changing default/provided default dictionary's structure
    ```python
        desired_structure = {
            'a': 'default value <a>',
            'b': {
                'bb1': 'default value ',
            }
        }
    
        my_dict = Idict(desired_structure, {
            "missing_keys": Idict.OPT.ALLOW
        })
    
        my_dict_ign = Idict(desired_structure, {
            "missing_keys": Idict.OPT.IGNORE
        })
    
        my_dict_thr = Idict(desired_structure, {
            "missing_keys": Idict.OPT.THROW
        })
    
        my_dict['b'] = 123
        print(repr(my_dict))
        # OK, result: {'a': 'default value <a>', 'b': 123}
    
        my_dict_ign['b'] = 123
        print(repr(my_dict_ign))
        # illegal trying to change desired dictionary structure
        # this operation will be ignored
        # OK, no exception, result: {'a': 'default value ', 'b': {'bb1': 'default value '}}
    
        my_dict_thr['b'] = 123
        # illegal trying to change desired dictionary structure
        # result: raise ValueNotAllowedException as below
        
        # ValueNotAllowedException: [Value Error] Trying to set value <123> 
        # for object <your_dict:Idict>, key <b> but in provided interface there 
        # is a dictionary under this key - <interface>
        # {'a': 'default value ', 'b': {'bb1': 'default value '}}. 
        # You cannot change expected objects structure
    ```
        
   
+ Validate dictionary, check mandatory keys. 

    Check if all mandatory keys (marked by `Ellipsis` - `...`) are overwritten/settled
    
    ```python
    my_dict1 = Idict({
        'a': None,
        'b': {
            'bb1': None,
            'bb2': ...
        },
    })
    
    try:
        my_dict1.validate()
    except MandatoryKeyValueException as e:
        # Key value for key [b][bb2] is mandatory.
        # Set value for this key or set default value in provided interface.
        pass
    
    my_dict1['b']['bb2'] = 123
    
    print(repr(my_dict1))
    # no Exception, all mandatory keys have value settled
    # {'a': None, 'b': {'bb1': None, 'bb2': 123}}
        
    ```

#### See more
See `./tests` for more examples

---