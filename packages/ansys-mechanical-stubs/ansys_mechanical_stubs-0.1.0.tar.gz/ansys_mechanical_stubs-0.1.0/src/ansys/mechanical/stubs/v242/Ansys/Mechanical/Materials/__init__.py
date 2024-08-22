"""Materials subpackage."""
import typing

class ImportSettings(object):
    """
    ImportSettings interface.
    """

    @property
    def Filter(self) -> typing.Optional["System.Collections.Generic.IList[System.String]"]:
        """
        
            All materials will be imported if this list of the names of
            specific materials to be imported is not specified.
            
        """
        return None


