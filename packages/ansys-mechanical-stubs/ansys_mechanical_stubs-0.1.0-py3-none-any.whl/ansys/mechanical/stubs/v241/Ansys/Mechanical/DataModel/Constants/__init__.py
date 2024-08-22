"""Constants subpackage."""
import typing

class Colors(object):
    """
    Color constants, in BGR bitfield layout.
    """

    @classmethod
    @property
    def Blue(cls) -> typing.Optional["System.UInt32"]:
        """
        Blue property.
        """
        return 16711680

    @classmethod
    @property
    def Cyan(cls) -> typing.Optional["System.UInt32"]:
        """
        Cyan property.
        """
        return 16776960

    @classmethod
    @property
    def Green(cls) -> typing.Optional["System.UInt32"]:
        """
        Green property.
        """
        return 65280

    @classmethod
    @property
    def Yellow(cls) -> typing.Optional["System.UInt32"]:
        """
        Yellow property.
        """
        return 65535

    @classmethod
    @property
    def Red(cls) -> typing.Optional["System.UInt32"]:
        """
        Red property.
        """
        return 255

    @classmethod
    @property
    def Gray(cls) -> typing.Optional["System.UInt32"]:
        """
        Gray property.
        """
        return 11053224

    @classmethod
    @property
    def White(cls) -> typing.Optional["System.UInt32"]:
        """
        White property.
        """
        return 16777215


