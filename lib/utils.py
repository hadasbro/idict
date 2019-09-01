from typing import Optional, List, Dict

from lib.exceptions import KeyOnNonDictException, EllipsisException, GeneralException, ValueNotAllowedException


class Utils:

    @staticmethod
    def map_path_to_string(path: Optional[List[str]] = None) -> str:
        return "".join(list(map(lambda el: "[{}]".format(str(el)), path)))

    @staticmethod
    def humanize_path_error(path: Optional[Dict[int, int]] = None) -> KeyOnNonDictException:
        pass

    @staticmethod
    def humanize_dict_error(exc: KeyOnNonDictException,
                            path: Optional[List[str]] = None) -> KeyOnNonDictException:

        rinfo: str = ""

        try:
            if path is None:
                raise GeneralException

            ltry = Utils.map_path_to_string(path)

            lcurrent = Utils.map_path_to_string(path[:-1])

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
    def find_xpath(acum: Dict[int, int], element: int):

        acum_result = []

        def find_recursively(acumi, el):
            try:
                al = acumi[el]
                if al > 0:
                    acum_result.append(al)
                    al = find_recursively(acumi, al)
            except KeyError:
                return 0
            return al

        acum_result.append(element)
        find_recursively(acum, element)
        acum_result.reverse()

        return acum_result

    @staticmethod
    def find_element(nested_dict, value, argpath=(), comparison_type="="):
        for key, val in nested_dict.items():
            path = argpath + (key,)
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

    @staticmethod
    def get_by_path(idict, key_path):
        dictval = idict
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
    def verify_overwritting_dect_type(path_value, key, value) -> bool:
        if key in path_value and isinstance(path_value[key], dict) and not isinstance(value, dict):
            raise ValueNotAllowedException(path_value, key, value)
        return True
