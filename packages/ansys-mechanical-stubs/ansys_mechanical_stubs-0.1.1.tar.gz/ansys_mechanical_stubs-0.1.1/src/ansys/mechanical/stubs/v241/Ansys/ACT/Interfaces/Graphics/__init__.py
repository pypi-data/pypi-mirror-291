"""Graphics subpackage."""
import typing

class IModelViewManager(object):
    """
    
            
            
    """

    @property
    def NumberOfViews(self) -> typing.Optional["System.Int32"]:
        """
        
            The number of views currently defined.
            
        """
        return None

    def ApplyModelView(self, viewIndex: "System.Int32") -> "System.Void":
        """
        
            Apply the view specified by index.
            
        """
        pass

    def ApplyModelView(self, viewLabel: "System.String") -> "System.Void":
        """
        
            Apply the view specified by name.
            
        """
        pass

    def CaptureModelView(self, index: "System.Int32", mode: "System.String") -> "System.Void":
        """
        
            Save the view specified by index as a PNG image to the project userfiles.
            
        """
        pass

    def CaptureModelView(self, viewLabel: "System.String", mode: "System.String") -> "System.Void":
        """
        
            Save the view specified as an image to the project userfiles.
            
        """
        pass

    def CreateView(self) -> "System.Void":
        """
        
            Create a view from current graphics with default naming.
            
        """
        pass

    def CreateView(self, viewName: "System.String") -> "System.Void":
        """
        
            Create a view from current graphics with the specified name.
            
        """
        pass

    def DeleteView(self, viewIndex: "System.Int32") -> "System.Void":
        """
        
            Delete the specified view by index.
            
        """
        pass

    def DeleteView(self, viewLabel: "System.String") -> "System.Void":
        """
        
            Apply the view specified by name.
            
        """
        pass

    def ExportModelViews(self, viewfilepath: "System.String") -> "System.Void":
        """
        
            Export model views to the specified file.
            
        """
        pass

    def ImportModelViews(self, viewfilepath: "System.String") -> "System.Void":
        """
        
            Import model views from the specified file.
            
        """
        pass

    def RenameView(self, viewIndex: "System.Int32", newLabel: "System.String") -> "System.Void":
        """
        
            Rename the model view specified by viewIndex to newLabel.
            
        """
        pass

    def RenameView(self, viewLabel: "System.String", newLabel: "System.String") -> "System.Void":
        """
        
            Rename the model view specified  to newLabel.
            
        """
        pass


