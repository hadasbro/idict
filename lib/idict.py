import collections
from enum import Enum
from typing import Any, Dict, List, Union

from lib.exceptions import EllipsisException, KeyOnNonDictException, KeyNotAllowedException, MandatoryKeyValueException
from lib.utils import Utils


class Idict(collections.defaultdict):
    class OPT(Enum):
        KEY_ALLOW = 1
        KEY_IGNORE = 2
        KEY_THROW = 3

    default_options: Dict[str, Union[OPT, bool]] = {
        "missing_keys": OPT.KEY_IGNORE,
        "ellipsis_as_mandatory": True
    }

    dependencies: Dict[int, int] = {}

    locked_keys: Dict[int, List[str]] = {}

    id_key: Dict[str, Any] = {}

    prev_id = 0

    def __init__(self, kargs, options: Dict[str, Union[OPT, bool]] = {}, deep=0):

        self.options = {**Idict.default_options, **options}

        self.kargs = kargs

        self.block_key = None

        collections.defaultdict.__init__(
            self, lambda: self.__class__(kargs, options, deep)._construct(id(self), self.locked_keys, self.dependencies,
                                                                          self.id_key, self.options)
        )

        if deep == 0:
            deep = + 1
            '''
            __init__ called first time, on first created object
            (in every new recursive object deep is > 0)
            '''
            self.__init_pattern()

    def _construct(self,
                   prev_id=0,
                   locked_keys: Dict[int, List[Any]] = {},
                   dependencies: Dict[int, int] = {},
                   id_key: Dict[str, Any] = {},
                   options: Dict[str, Union[OPT, bool]] = {}
                   ):

        self.options = options

        self.dependencies: Dict[int, int] = dependencies

        self.id_key: Dict[str, Any] = id_key

        self.prev_id = prev_id

        self.locked_keys: Dict[int, List[Any]] = locked_keys

        return self

    def __init_pattern(self):
        Idict.__recucrive_init(self.kargs, self)
        pass

    def __setitem__(self, k, v) -> None:

        ids = id(self)

        if not isinstance(v, Idict):

            try:
                element_path = Utils.find_xpath(self.dependencies, self.prev_id)

                try:
                    element_path = list(map(lambda x: self.id_key[x], element_path))
                    element_path.append(k)
                except KeyError:
                    '''
                    key 0, root parent, just
                    pass and let program continue
                    '''
                    pass

                if len(element_path) == 1 and element_path[0] == 0 and k not in self.kargs.keys():
                    '''
                    root element is not available in the interface
                    '''
                    raise EllipsisException(0)

                # throws EllipsisException
                Utils.get_by_path(self.kargs, element_path)

            except EllipsisException:

                if self.options["missing_keys"] is self.OPT.KEY_ALLOW:
                    '''
                    allow key even if doesnt exist in the interface.
                    Pass and let program to save key-value
                    '''
                    pass
                elif self.options["missing_keys"] is self.OPT.KEY_IGNORE \
                        or self.options["missing_keys"] is self.OPT.KEY_THROW:
                    '''
                    dissallow / filter key which is not available in
                    the interface. Add key to the list of dissallowed
                    keys for this Object to be checked in next iteration
                    '''

                    if ids not in self.locked_keys.keys():
                        self.locked_keys[ids] = [k]
                    else:
                        self.locked_keys[ids].append(k)
                    '''
                    interrupt here and prevent __setitem__
                    to set a value for that key
                    '''
                    if self.options["missing_keys"] is self.OPT.KEY_THROW:
                        raise KeyNotAllowedException(k, lambda: Utils.map_path_to_string(element_path))

                    return

            except KeyOnNonDictException as kex:
                raise Utils.humanize_dict_error(kex, element_path)

        elif ids in self.locked_keys.keys() and k in self.locked_keys[ids]:
            '''
            if key is on the list of disallowed keys,
            then interrupt this iteration here and
            prevent __setitem__ to initialise new dict
            '''
            return

        else:
            '''
            Scenario where disallowed key is in the middle of the interface e.g.
            interface is pattern = {{'j': {'k2': {'a': 777}}}}
            and keys init is: d['j']['non_existing']['a'] = 100
            '''
            element_path = Utils.find_xpath(self.dependencies, self.prev_id)

            try:
                element_path = list(map(lambda x: self.id_key[x], element_path))
                element_path.append(k)
            except KeyError:
                '''
                key 0, root parent, just
                pass and let program continue
                '''
                pass

            try:

                Utils.get_by_path(self.kargs, element_path)

                if len(element_path) == 1 and element_path[0] == 0 and k not in self.kargs.keys():
                    '''
                    root element is not available in the interface
                    '''
                    raise EllipsisException(0)

            except EllipsisException:
                if self.options["missing_keys"] is self.OPT.KEY_ALLOW:
                    pass
                elif self.options["missing_keys"] is self.OPT.KEY_IGNORE:
                    return
                elif self.options["missing_keys"] is self.OPT.KEY_THROW:
                    raise KeyNotAllowedException(k, element_path)

            self.id_key[ids] = k

        '''
        chain rerursive dictionaries
        '''
        self.dependencies[ids] = self.prev_id

        super().__setitem__(k, v)

    def __repr__(self):
        return repr(dict(self))

    def __str__(self):
        return "container:" + str(id(self)) + " dict: " + str(dict(self))

    @staticmethod
    def __recucrive_init(pattern: Dict[str, Any], root: 'Idict'):
        """
        __recucrive_init

        This is static method on purpose this method rerursively set all elements
        on passed dict (Idict class object) and force Idict to autoset itself like
        it would be done normally uppon statement as below
        dict['a']['b']['c'] = 1

        :param pattern:
        :param root:
        :return:
        """
        for i in pattern:
            if isinstance(pattern[i], dict):
                # root[i] = {}
                if i not in root:
                    root[i] = {}
                Idict.__recucrive_init(pattern[i], root[i])
            else:
                root[i] = pattern[i]

    def validate(self) -> bool:

        if self.options["ellipsis_as_mandatory"] is True:

            path = Utils.find_element(dict(self), ...)

            if path is None:
                return True
            else:
                msg: str = "Key value for key <your_idict: Idict>{} is mandatory. " \
                           "Set value for this key or set default value in provided " \
                           "interface. ".format(Utils.map_path_to_string(list(path)))
                raise MandatoryKeyValueException(msg)

        return True
