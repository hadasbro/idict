# from __future__ import annotations
import base64
import collections
import copy
from enum import Enum
from typing import Any, Dict, List, Union, Optional
from lib import KT, KV
from lib.exceptions import EllipsisException, KeyOnNonDictException, \
    KeyNotAllowedException, MandatoryKeyValueException, \
    ValueNotAllowedException
from lib.utils import Utils


class Idict(collections.defaultdict):
    """
    Idict - main dynamic dictionary class

    Note:
        Idict obects are initiated recursively bu lambda expression
        lambda: self.
                __class__(kargs, options, deep).
                _construct(id(self), self.locked_keys, self.dependencies, self.id_key, self.options)

    Attributes:
        options (Optional[Dict[str, Union[OPT, bool]]]): options,
        default {missing_keys: OPT.ALLOW, "ellipsis_as_mandatory": True}
        dependencies (Dict[int, int]): denendencies between object id : id2
        locked_keys (Dict[int, List[KT]]): locked keys, parameter used internally
        id_key (Dict[int, KT]): objetc's id associated with key in the dict

    """

    class OPT(Enum):
        """
        OPT options enum
        """
        ALLOW = 1
        IGNORE = 2
        THROW = 3

    default_options: Dict[str, Union[OPT, bool]] = {
        "missing_keys": OPT.ALLOW,
        "ellipsis_as_mandatory": True
    }

    dependencies: Dict[int, int] = {}

    locked_keys: Dict[int, List[KT]] = {}

    id_key: Dict[int, KT] = {}

    prev_id = 0

    def __init__(
            self,
            kargs: Dict[KT, KV],
            options: Optional[Dict[str, Union[OPT, bool]]] = None,
            deep: int = 0
    ) -> None:
        """
        __init__

        Args:
            kargs (Dict[KT, KV]): specified, expected, default dictionary
            options (Optional[Dict[str, Union[OPT, bool]]]): opts
            deep (int): obj deep

        Returns:
            None

        """
        opt = options if options is not None else {}
        self.options = {**Idict.default_options, **opt}

        self.kargs = copy.deepcopy(kargs)

        self.block_key = None

        if deep == 0:
            # Keep recursive bookkeeping isolated per root instance.
            self.dependencies = {}
            self.locked_keys = {}
            self.id_key = {}

        collections.defaultdict.__init__(
            self,
            lambda: self.__class__(self.kargs, self.options, deep)._construct(
                    id(self), self.locked_keys, self.dependencies, self.id_key, self.options
            )
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
        """
        _construct

        Args:
            prev_id (int): prev_id
            locked_keys (Dict[int, List[KT]]): locked_keys
            dependencies (Dict[int, int]): dependencies
            id_key (Dict[int, KT]): id_key
            options (Dict[str, Union[OPT, bool]]): options

        Returns:
            Idict: self class object
        """

        self.options = options

        self.dependencies = dependencies

        self.id_key = id_key

        self.prev_id = prev_id

        self.locked_keys = locked_keys

        return self

    def __init_pattern(self) -> None:
        """
        __init_pattern

        Returns:
            None

        """
        Idict.__recucrive_init(self.kargs, self.options, self)

    def __setitem__(self, k: KT, v: KV) -> None:
        """
        __setitem__

        Args:
            k (KT): key
            v (KV): value

        Returns:
            None

        Raises:
            EllipsisException: if used root element is not available in the interface
            ValueNotAllowedException: if we dont accept values from outside provided pattern
            and we have such value set in the code
            KeyNotAllowedException: if we have value set for disallowed key
            KeyOnNonDictException: if we are trying to set key-val pair on non-dict element

        """
        ids: int = id(self)

        if not isinstance(v, Idict):

            element_path: List[Any] = []

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

                if isinstance(path_value, dict) and k in path_value \
                        and isinstance(path_value[k], dict) and isinstance(v, dict):
                    raise ValueNotAllowedException(path_value[k], k, v)

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

    def update(self, other: Optional[Any] = None, **kwargs: Any) -> None:
        """
        update

        Uses __setitem__ for every assignment to preserve Idict constraints.
        """
        if other is not None:
            items = other.items() if hasattr(other, "items") else other
            for k, v in items:
                self[k] = v

        for k, v in kwargs.items():
            self[k] = v

    def setdefault(self, key: KT, default: Optional[KV] = None) -> Optional[KV]:
        """
        setdefault

        Uses __setitem__ for first assignment to preserve Idict constraints.
        """
        if key in self:
            return self[key]

        self[key] = default
        return self[key]

    def __ior__(self, other: Any) -> 'Idict':
        self.update(other)
        return self

    def __or__(self, other: Any) -> 'Idict':
        copied = copy.copy(self)
        copied.update(other)
        return copied

    def __ror__(self, other: Any) -> 'Idict':
        copied = Idict(self.kargs, self.options)
        copied.update(other)
        copied.update(dict(self))
        return copied

    def __copy__(self) -> 'Idict':
        copied = Idict(self.kargs, self.options)
        self.__merge_data(copied, self.__to_plain_data(dict(self)))
        return copied

    def __deepcopy__(self, memo: Dict[int, Any]) -> 'Idict':
        return self.__copy__()

    def __reduce__(self) -> Any:
        raise TypeError("Idict does not support pickle serialization yet. Use dict(idict) instead.")

    def __repr__(self) -> str:
        """
        __repr__

        Returns:
            str: repr value
        """
        return repr(dict(self))

    def __str__(self) -> str:
        """
        __str__

        Returns:
            str: str obj representation
        """
        return "container:" + str(id(self)) + " dict: " + str(dict(self))

    @staticmethod
    def __recucrive_init(pattern: Dict[str, Any], options: Dict[str, Union[OPT, bool]], root: 'Idict') -> Any:
        """
        __recucrive_init

        This is static method on purpose this method rerursively set all elements
        on passed dict (Idict class object) and force Idict to autoset itself like
        it would be done normally uppon statement as below
        dict['a']['b']['c'] = 1

        Args:
            pattern (Dict[str, Any]): pattern/expected dictionary structure
            options (Dict[str, Union[OPT, bool]]): opts
            root (Idict): root element object

        Returns:

        """
        for i in pattern:
            if isinstance(pattern[i], dict):
                if i not in root:
                    root[i] = Idict(pattern[i], options)
                    Idict.__recucrive_init(pattern[i], options, root[i])
                else:
                    Idict.__recucrive_init(pattern[i], options, root[i])
            else:
                root[i] = copy.deepcopy(pattern[i])

    def validate(self) -> bool:
        """
        validate

        Returns:
            bool: True if all OK, otherwise raises MandatoryKeyValueException

        Raises:
            MandatoryKeyValueException: if we have any mandatory key with no value settled

        """
        if self.options["ellipsis_as_mandatory"] is True:
            self.__validate_mandatory_against_schema(self.kargs, dict(self), [])

        return True

    @classmethod
    def __validate_mandatory_against_schema(
            cls,
            schema: Dict[KT, KV],
            payload: Dict[KT, KV],
            path: List[KT]
    ) -> None:
        for key, schema_value in schema.items():
            new_path = path + [key]

            if schema_value is ...:
                if key not in payload or payload.get(key) is ...:
                    msg: str = "Key value for key <your_idict: Idict>{} is mandatory. " \
                               "Set value for this key or set default value in provided " \
                               "interface. ".format(Utils.map_path_to_string(new_path))
                    raise MandatoryKeyValueException(msg)
                continue

            if isinstance(schema_value, dict):
                nested_payload: Dict[KT, KV] = {}
                if key in payload and isinstance(payload[key], dict):
                    nested_payload = payload[key]
                cls.__validate_mandatory_against_schema(schema_value, nested_payload, new_path)

    @classmethod
    def __to_plain_data(cls, value: Any) -> Any:
        if isinstance(value, Idict):
            value = dict(value)

        if isinstance(value, dict):
            return {k: cls.__to_plain_data(v) for k, v in value.items()}

        if isinstance(value, list):
            return [cls.__to_plain_data(v) for v in value]

        if isinstance(value, tuple):
            return tuple(cls.__to_plain_data(v) for v in value)

        if isinstance(value, set):
            return {cls.__to_plain_data(v) for v in value}

        return copy.deepcopy(value)

    @classmethod
    def __merge_data(cls, target: 'Idict', source: Dict[Any, Any]) -> None:
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], Idict):
                cls.__merge_data(target[key], value)
            else:
                target[key] = value

    def hash_code(self) -> str:
        """
        hash_code

        Returns:
            str
        """
        encoded_bytes = base64.b64encode(self.__repr__().encode("utf-8"))
        return str(encoded_bytes, "utf-8")
