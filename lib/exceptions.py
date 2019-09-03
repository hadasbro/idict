from typing import Union, Optional, List, Callable, Any


class GeneralException(Exception):
    """
    GeneralException
    """

    def __init__(self, msg: str = "") -> None:
        """
        __init__

        Args:
            msg (str): msg

        Returns:
            None
        """
        super().__init__(self, msg)


class EllipsisException(Exception):
    """
    EllipsisException
    """

    def __init__(self, msg: Union[str, int] = None):
        """
        __init__

        Args:
            msg (Union[str, int]): msg

        Returns:
            None
        """
        super().__init__(self, str(msg))


class KeyOnNonDictException(Exception):
    """
    KeyOnNonDictException
    """

    def __init__(self, key: str = "", msg: str = "") -> None:
        """
        __init__

        Args:
            key (str): key
            msg (str): message

        Returns:
            None
        """
        self.key: str = key
        self.msg: str = msg
        super().__init__(self, msg)

    def __str__(self) -> str:
        """
        __str__

        Returns:
            str: string repr

        Returns:
            str: str repr
        """
        return self.msg


class MandatoryKeyValueException(Exception):
    """
    MandatoryKeyValueException
    """

    def __init__(self, msg: str = "") -> None:
        """
        __init__

        Args:
            msg (msg): msg

        Returns:
            None
        """
        self.msg: str = msg
        super().__init__(self, msg)

    def __str__(self) -> str:
        """
        __str__

        Returns:
            str: str repr
        """
        return self.msg


class KeyNotAllowedException(Exception):
    """
    KeyNotAllowedException
    """

    def __init__(self, key: str = "", path_builder: Optional[Callable[[List[Union[int, str]]], str]] = None) -> None:
        """
        __init__

        Args:
            key (str): key
            path_builder (Optional[Callable[[List[Union[int, str]]], str]]): path to search in

        Returns:
            None

        Raises:
            GeneralException: if path_builder is None

        """
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

        super().__init__(self, message)


class ValueNotAllowedException(Exception):
    """
    ValueNotAllowedException
    """

    def __init__(self, path_value: str, key: Union[str, int], value: Any) -> None:
        """
        __init__

        Args:
            path_value (str): path
            key (Union[str, int]): key
            value (Any): value

        Returns:
            None
        """
        message: str = "[Value Error] Trying to set value <{}> for object <your_dict:Idict>, key <{}> " \
                       "but in provided interface there is a dictionary under this key - " \
                       "<interface>{}. You cannot change expected objects structure".format(value, key, path_value)

        super().__init__(self, message)
