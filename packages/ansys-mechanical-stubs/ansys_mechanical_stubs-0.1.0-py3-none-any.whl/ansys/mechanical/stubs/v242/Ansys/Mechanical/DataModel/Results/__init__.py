"""Results subpackage."""
import typing

class ResultDataTable(object):
    """
    Specifies the Result Table.
    """

    @property
    def Item(self) -> typing.Optional["System.Collections.IEnumerable"]:
        """
        Item property.
        """
        return None

    @property
    def Keys(self) -> typing.Optional["System.Collections.Generic.IEnumerable[System.String]"]:
        """
        Keys property.
        """
        return None

    @property
    def Values(self) -> typing.Optional["System.Collections.Generic.IEnumerable[System.Collections.IEnumerable]"]:
        """
        Values property.
        """
        return None

    @property
    def Count(self) -> typing.Optional["System.Int32"]:
        """
        Count property.
        """
        return None

    def ContainsKey(self, key: "System.String") -> "System.Boolean":
        """
        ContainsKey method.
        """
        pass


class ResultVariable(object):
    """
    Specifies column data for the Result Table.
    """

    @property
    def Item(self) -> typing.Optional["System.Double"]:
        """
        Item property.
        """
        return None

    @property
    def Count(self) -> typing.Optional["System.Int32"]:
        """
        Count property.
        """
        return None


