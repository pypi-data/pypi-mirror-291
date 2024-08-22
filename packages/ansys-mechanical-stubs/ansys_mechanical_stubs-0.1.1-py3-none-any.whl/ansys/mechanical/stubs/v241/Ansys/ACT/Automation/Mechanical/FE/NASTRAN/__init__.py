"""NASTRAN subpackage."""
import typing

class NASTRANCommand(object):
    """
    NASTRANCommand class.
    """

    @property
    def Name(self) -> typing.Optional["System.String"]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional["System.UInt32"]:
        """
        
            Gets the command index.
            
        """
        return None


class GenericCommand(object):
    """
    
            Generic command.
            
    """

    @property
    def Arguments(self) -> typing.Optional["System.Collections.Generic.IReadOnlyList[System.Object]"]:
        """
        
            Gets the arguments.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional["System.String"]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional["System.UInt32"]:
        """
        
            Gets the command index.
            
        """
        return None


class CaseControlCommand(object):
    """
    
            Case control command.
            
    """

    @property
    def Text(self) -> typing.Optional["System.String"]:
        """
        
            Gets the text.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional["System.String"]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional["System.UInt32"]:
        """
        
            Gets the command index.
            
        """
        return None


class NastranOption(object):
    """
    
            Option.
            
    """

    pass

class NastranOptionLine(object):
    """
    
            Option line.
            
    """

    pass

class OptionsControlCommand(object):
    """
    
            Options control command.
            
    """

    @property
    def Arguments(self) -> typing.Optional["System.Collections.Generic.IReadOnlyList[System.Object]"]:
        """
        
            Gets the arguments.
            
        """
        return None

    @property
    def OptionLines(self) -> typing.Optional["System.Collections.Generic.IReadOnlyList[System.Object]"]:
        """
        
            Gets the option lines.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional["System.String"]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional["System.UInt32"]:
        """
        
            Gets the command index.
            
        """
        return None


