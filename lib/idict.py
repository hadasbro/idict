# from __future__ import annotations
import base64
import collections
from enum import Enum
from typing import Any, Dict, List, Union, Optional
from lib import KT, KV
from lib.exceptions import EllipsisException, KeyOnNonDictException, \
    KeyNotAllowedException, MandatoryKeyValueException, \
    ValueNotAllowedException
from lib.utils import Utils


class Idict(collections.defaultdict):

    class OPT(Enum):
        ALLOW = 1
        IGNORE = 2
        THROW = 3

    default_options: Dict[str, Union[OPT, bool]] = {
        "missing_keys": OPT.IGNORE,
        "ellipsis_as_mandatory": True
    }

    dependencies: Dict[int, int] = {}

    locked_keys: Dict[int, List[KT]] = {}

    id_key: Dict[int, KT] = {}

    prev_id = 0

    def __init__(self, kargs: Dict[KT, KV], options: Optional[Dict[str, Union[OPT, bool]]] = None, deep=0) -> None:

        opt = options if options is not None else {}
        self.options = {**Idict.default_options, **opt}

        self.kargs = kargs

        self.block_key = None

        collections.defaultdict.__init__(
            self,
            lambda: self.
                __class__(kargs, options, deep).
                _construct(id(self), self.locked_keys, self.dependencies, self.id_key, self.options)
        )

        if deep == 0:
            deep = + 1
            '''
            __init__ called first time, on first created object
            (in every new recursive object deep is > 0)
            '''
            self.__init_pattern()

    def _construct(self,
                   prev_id: int,
                   locked_keys: Dict[int, List[KT]],
                   dependencies: Dict[int, int],
                   id_key: Dict[int, KT],
                   options: Dict[str, Union[OPT, bool]]
                   ) -> 'Idict':

        self.options: Dict[str, Union[Idict.OPT, bool]] = options

        self.dependencies: Dict[int, int] = dependencies

        self.id_key: Dict[int, KT] = id_key

        self.prev_id: int = prev_id

        self.locked_keys: Dict[int, List[Any]] = locked_keys

        return self

    def __init_pattern(self) -> None:
        Idict.__recucrive_init(self.kargs, self.options, self)

    def __setitem__(self, k: KT, v: KV) -> None:

        ids: int = id(self)

        if not isinstance(v, Idict):

            element_path = []

            try:
                element_path: List[int] = Utils.find_xpath(self.dependencies, self.prev_id)
                try:
                    element_path: List[KT] = list(map(lambda x: self.id_key[x], element_path))
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
                path_value: Union[Dict[KT, KV], KV] = Utils.get_by_path(self.kargs, element_path)

                # throws ValueNotAllowedException
                Utils.verify_overwritting_dect_type(path_value, k, v)

            except ValueNotAllowedException as ex:
                if self.options["missing_keys"] is self.OPT.THROW:
                    raise ex
                elif self.options["missing_keys"] is self.OPT.IGNORE:
                    return

            except EllipsisException:

                if self.options["missing_keys"] is self.OPT.ALLOW:
                    '''
                    allow key even if doesnt exist in the interface.
                    Pass and let program to save key-value
                    '''
                    pass
                elif self.options["missing_keys"] is self.OPT.IGNORE \
                        or self.options["missing_keys"] is self.OPT.THROW:
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
                    if self.options["missing_keys"] is self.OPT.THROW:
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
                element_path: List[KT] = list(map(lambda x: self.id_key[x], element_path))
                element_path.append(k)
            except KeyError:
                '''
                key 0, root parent, just
                pass and let program continue
                '''
                pass

            try:

                path_value = Utils.get_by_path(self.kargs, element_path)

                # throws ValueNotAllowedException
                Utils.verify_overwritting_dect_type(path_value, k, v)

                if len(element_path) == 1 and element_path[0] == 0 and k not in self.kargs.keys():
                    '''
                    root element is not available in the interface
                    '''
                    raise EllipsisException(0)

            except ValueNotAllowedException as ex:
                if self.options["missing_keys"] is self.OPT.THROW:
                    raise ex
                elif self.options["missing_keys"] is self.OPT.IGNORE:
                    return

            except EllipsisException:
                if self.options["missing_keys"] is self.OPT.ALLOW:
                    pass
                elif self.options["missing_keys"] is self.OPT.IGNORE:
                    return
                elif self.options["missing_keys"] is self.OPT.THROW:
                    raise KeyNotAllowedException(k, lambda: Utils.map_path_to_string(element_path))

            self.id_key[ids] = k

        '''
        chain rerursive dictionaries
        '''
        self.dependencies[ids] = self.prev_id

        super().__setitem__(k, v)

    def __repr__(self) -> str:
        return repr(dict(self))

    def __str__(self) -> str:
        return "container:" + str(id(self)) + " dict: " + str(dict(self))

    @staticmethod
    def __recucrive_init(pattern: Dict[str, Any], options: Dict[str, Union[OPT, bool]], root: 'Idict') -> Any:
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
                if i not in root:
                    root[i] = Idict(pattern[i], options)
                    Idict.__recucrive_init(pattern[i], options, root[i])
                else:
                    Idict.__recucrive_init(pattern[i], options, root[i])
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

    def hash_code(self) -> str:
        encoded_bytes = base64.b64encode(self.__repr__().encode("utf-8"))
        return str(encoded_bytes, "utf-8")
