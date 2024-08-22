"""Application subpackage."""
import typing

class Progress(object):
    """
    Defines a Progress.
    """

    def SetProgress(self, uiProgress: "System.UInt32", uiMessage: "System.String", uiSubProgress: "System.UInt32", uiSubMessage: "System.String") -> "System.Void":
        """
        Set the current progress state
        """
        pass


class ObjectTag(object):
    """
    
            An instance of an ObjectTag.
            
    """

    @property
    def Name(self) -> typing.Optional["System.String"]:
        """
        
            The name of the tag. If the tag exists in ObjectTags, attempting to set the name to a value of another tag in that collection will lead to an exception.
            
        """
        return None

    @property
    def Objects(self) -> typing.Optional["System.Collections.Generic.IEnumerable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]"]:
        """
        
            The list of objects which use this tag.
            
        """
        return None

    def AddObject(self, obj: "Ansys.Mechanical.DataModel.Interfaces.IDataModelObject") -> "System.Void":
        """
        
            Add an object to this tag.
            
        """
        pass

    def RemoveObject(self, obj: "Ansys.Mechanical.DataModel.Interfaces.IDataModelObject") -> "System.Void":
        """
        
            Remove an object from this tag.
            
        """
        pass

    def ClearObjects(self) -> "System.Void":
        """
        
            Clear all objects from this tag.
            
        """
        pass


class ObjectTags(object):
    """
    
            Defines the collection of Mechanical’s tags.
            
    """

    @property
    def Count(self) -> typing.Optional["System.Int32"]:
        """
        
            The number of tags in the collection.
            
        """
        return None

    @property
    def Item(self) -> typing.Optional["Ansys.Mechanical.Application.ObjectTag"]:
        """
        Item property.
        """
        return None

    @property
    def Item(self) -> typing.Optional["Ansys.Mechanical.Application.ObjectTag"]:
        """
        Item property.
        """
        return None

    @property
    def TagNames(self) -> typing.Optional["System.Collections.Generic.List[System.String]"]:
        """
        
            The names of the tags in the collection.
            
        """
        return None

    def Add(self, tag: "Ansys.Mechanical.Application.ObjectTag") -> "System.Void":
        """
        
            Adds a new tag to the collection. Throws an error if the tag already exists in the collection.
            
        """
        pass

    def Remove(self, tag: "Ansys.Mechanical.Application.ObjectTag") -> "System.Boolean":
        """
        
            Removes a tag if it exists in the collection.
            
        """
        pass

    def GetTag(self, tagName: "System.String") -> "Ansys.Mechanical.Application.ObjectTag":
        """
        
            Returns the tag in the collection with the given name.
            
        """
        pass

    def IndexOf(self, tag: "Ansys.Mechanical.Application.ObjectTag") -> "System.Int32":
        """
        
            Returns the index of the given tag. If the given tag does not exist in the collection, returns -1.
            
        """
        pass

    def RemoveAt(self, index: "System.Int32") -> "System.Void":
        """
        
            Removes the tag at the given index from the collection.
            
        """
        pass

    def Clear(self) -> "System.Void":
        """
        
            Clears the collection, removing all objects from the tags in the collection.
            
        """
        pass

    def Contains(self, tag: "Ansys.Mechanical.Application.ObjectTag") -> "System.Boolean":
        """
        
            Returns whether or not the collection contains the given tag.
            
        """
        pass


class Message(object):
    """
    
            A message.
            
    """

    @property
    def Source(self) -> typing.Optional["Ansys.Mechanical.DataModel.Interfaces.IDataModelObject"]:
        """
        
            The source object of the message.
            
        """
        return None

    @property
    def StringID(self) -> typing.Optional["System.String"]:
        """
        
            The string ID of the message.
            
        """
        return None

    @property
    def DisplayString(self) -> typing.Optional["System.String"]:
        """
        
            The display string of the message.
            
        """
        return None

    @property
    def Location(self) -> typing.Optional["Ansys.ACT.Interfaces.Common.ISelectionInfo"]:
        """
        
            The location of the message.
            
        """
        return None

    @property
    def TimeStamp(self) -> typing.Optional["System.DateTime"]:
        """
        
            The timestamp of the message.
            
        """
        return None

    @property
    def RelatedObjects(self) -> typing.Optional["System.Collections.Generic.IEnumerable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]"]:
        """
        
            The list of objects related to the message.
            
        """
        return None

    @property
    def Severity(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.MessageSeverityType"]:
        """
        
            The severity of the message.
            
        """
        return None


class Messages(object):
    """
    
            Defines the collection of Mechanical's messages.
            
    """

    @property
    def Count(self) -> typing.Optional["System.Int32"]:
        """
        
            Get the number of messages.
            
        """
        return None

    def Add(self, item: "Ansys.Mechanical.Application.Message") -> "System.Void":
        """
        
            Add a new message.
            
        """
        pass

    def Remove(self, item: "Ansys.Mechanical.Application.Message") -> "System.Boolean":
        """
        
            Remove a specific message in the list.
            
        """
        pass

    def Clear(self) -> "System.Void":
        """
        
            Clear the list of the messages.
            
        """
        pass

    def Contains(self, item: "Ansys.Mechanical.Application.Message") -> "System.Boolean":
        """
        
            Check if a message is in the current list of messages.
            
        """
        pass

    def ShowErrors(self) -> "System.Void":
        """
        
            Shows errors with current project.
            
        """
        pass


