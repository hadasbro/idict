from typing import Optional, List, Dict, Union, Tuple, Any

from lib import KT, KV
from lib.exceptions import KeyOnNonDictException, EllipsisException, GeneralException, ValueNotAllowedException


class Utils:
    """
    Utils class
    """

    @staticmethod
    def map_path_to_string(path: Optional[List[str]] = None) -> str:
        """
        map_path_to_string

        Args:
            path (Optional[List[str]]): pthto map

        Returns:
            str: path
        """
        path = path if path is not None else []
        return "".join(list(map(lambda el: "[{}]".format(str(el)), path)))

    @staticmethod
    def humanize_path_error(path: Optional[Dict[int, int]] = None) -> KeyOnNonDictException:
        """
        humanize_path_error

        Args:
            path (Optional[Dict[int, int]]): path to map

        Returns:
            KeyOnNonDictException: exception
        """
        pass

    @staticmethod
    def humanize_dict_error(exc: KeyOnNonDictException,
                            path: Optional[List[str]] = None) -> KeyOnNonDictException:
        """
        humanize_dict_error

        Args:
            exc (KeyOnNonDictException): exception to humanize
            path (Optional[List[str]]): path

        Returns:
            KeyOnNonDictException: exception
            GeneralException: if path is None
        """

        rinfo: str = ""

        try:
            if path is None:
                raise GeneralException

            ltry: str = Utils.map_path_to_string(path)

            lcurrent: str = Utils.map_path_to_string(path[:-1])

            rinfo = "<your_dict:Idict>{} but <interface>{} in provided interface is a not " \
                    "dictionary and cannot be treated as dict" \
                .format(ltry, lcurrent)

        except GeneralException:
            pass

        exc.msg = "[Element Error] You are trying to use non-dictionary " \
                  "element as a dictionary. " \
                  + rinfo \
                  + " [Details] " + str(exc.msg)

        return exc

    @staticmethod
    def find_xpath(acum: Dict[int, int], element: int) -> List[int]:
        """
        find_xpath

        Args:
            acum (Dict[int, int]): dictionary path
            element (int): element to find

        Returns:
            List[int]: list of IDs
        """

        acum_result: List[int] = []

        def find_recursively(acumi: Dict[int, int], el: int) -> Any:
            """
            find_recursively inner function
            Args:
                acumi (Dict[int, int]): path
                el (int): element

            Returns:
                Any

            """
            try:
                al: Any = acumi[el]
                if al > 0:
                    acum_result.append(al)
                    find_recursively(acumi, al)
            except KeyError:
                return 0
            return al

        acum_result.append(element)
        find_recursively(acum, element)
        acum_result.reverse()

        return acum_result

    @staticmethod
    def find_element(
            nested_dict: Dict[KT, KV],
            value: KV,
            apath: Tuple[KT, ...] = (),
            comparison_type: str = "="
    ) -> Union[Tuple[KT, ...], None]:
        """
        find_element

        Args:
            nested_dict (Dict[KT, KV]): dictionary to search in
            value (KV): value to search
            apath (Tuple[KT, ...]): path tuple
            comparison_type (str): comparison type

        Returns:
            Union[Tuple[KT, ...]: element or tuple of elements
        """
        for key, val in nested_dict.items():
            path = apath + (key,)
            if comparison_type == "is":
                predicate = val is value
            else:
                predicate = val == value

            if predicate:
                return path
            elif hasattr(val, 'items'):
                pa = Utils.find_element(val, value, path, comparison_type)
                if pa is not None:
                    return pa
        return None

    @staticmethod
    def get_by_path(idict: Dict[KT, KV], key_path: Union[List[KT], KT]) -> Union[Dict[KT, KV], KV]:
        """
        get_by_path

        Args:
            idict (Dict[KT, KV]):
            key_path (KT): key path

        Returns:
            Union[Dict[KT, KV], KV]: dictionary result

        Raises:
            EllipsisException: if there is no key
            KeyOnNonDictException: if attribute error

        """
        dictval: Dict[KT, KV] = idict
        for k in key_path:
            try:
                '''
                Ellipsis == not settled and != None 
                we allow None as a normal value
                '''
                if k not in dictval.keys() and k != 0:
                    raise EllipsisException()

                if k == 0:
                    continue

            except AttributeError as ae:
                raise KeyOnNonDictException(k, str(ae))

            dictval = dictval.get(k)

        return dictval

    @staticmethod
    def verify_overwritting_dect_type(path_value: Union[Dict[KT, KV], KV], key: KT, value: KV) -> bool:
        """
        verify_overwritting_dect_type

        Args:
            path_value (Union[Dict[KT, KV], KV]): path
            key (KT): key
            value (KV): value

        Returns:
            bool: True if OK, exception if not

        Raises:
            ValueNotAllowedException: if there is no val

        """

        if not isinstance(path_value, dict):
            return True

        if key in path_value and isinstance(path_value[key], dict) and not isinstance(value, dict):
            raise ValueNotAllowedException(path_value[key], key, value)

        return True
