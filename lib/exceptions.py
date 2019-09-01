from typing import Union, Optional, List, Callable


class GeneralException(Exception):
    def __init__(self, msg: str = ""):
        super().__init__(msg)


class EllipsisException(Exception):
    def __init__(self, msg: Union[str, int] = None):
        super().__init__(str(msg))


class KeyOnNonDictException(Exception):

    def __init__(self, key: str = None, msg: str = None):
        self.key: str = key
        self.msg: str = msg
        super().__init__(key, msg)

    def __str__(self):
        return self.msg


class MandatoryKeyValueException(Exception):

    def __init__(self, msg: str = None):
        self.msg: str = msg
        super().__init__(msg)

    def __str__(self):
        return self.msg


class KeyNotAllowedException(Exception):

    def __init__(self, key: str = "", path_builder: Optional[Callable[[List[Union[int, str]]], str]] = None):

        ltry: str = ""

        try:
            if path_builder is None:
                raise GeneralException
            ltry = path_builder()
        except TypeError:
            pass

        if ltry == "[0]":
            ltry = ""

        message: str = "[Key Error] You are trying to set value for key <{}> " \
                       "for your Idict <your_dict:Idict>{} but this key is disallowed " \
                       "and doesnt exist in the provided interface".format(key, ltry)

        super().__init__(message)


class ValueNotAllowedException(Exception):

    def __init__(self, path_value, key, value):
        message: str = "[Value Error] Trying to set value <{}> for object <your_dict:Idict>, key <{}> " \
                       "but in provided interface there is a dictionary under this key - " \
                       "<interface>{}. You cannot change expected objects structure".format(value, key, path_value)

        super().__init__(message)
