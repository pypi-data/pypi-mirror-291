"""
Module: notset.py
This module defines the NotSet object
"""


class NotSetObject:
    """
    This class represents a NotSetObject.

    The NotSetObject class is used to represent an config that is not set.
    It provides a __bool__() method that always returns False.

    Methods:
        __bool__(): Returns False

    Examples:
        not_set = NotSetObject()
        if not_set:
            print("The object is set.")
        else:
            print("The object is not set.")

    """

    def __bool__(self) -> bool:
        return False


NotSet = NotSetObject()
