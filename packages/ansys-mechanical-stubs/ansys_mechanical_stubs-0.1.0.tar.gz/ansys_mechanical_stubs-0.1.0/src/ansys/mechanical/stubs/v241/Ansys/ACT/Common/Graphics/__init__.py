"""Graphics subpackage."""
import typing

class DMCameraWrapper(object):
    """
    
            Wrapper for Camera in Design Modeler.
            
    """

    pass

class MechanicalCameraWrapper(object):
    """
    
            Wrapper for Camera in Mechanical.
            
    """

    @property
    def FocalPoint(self) -> typing.Optional["Ansys.Mechanical.Graphics.Point"]:
        """
        
            The focal point of the camera (coordinates are in the global coordinate system).
            
        """
        return None

    @property
    def UpVector(self) -> typing.Optional["Ansys.ACT.Math.Vector3D"]:
        """
        
            The vector pointing up from the focal point.
            
        """
        return None

    @property
    def ViewVector(self) -> typing.Optional["Ansys.ACT.Math.Vector3D"]:
        """
        
            The vector pointing from the focal point to the camera.
            
        """
        return None

    @property
    def SceneHeight(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        
            Specifies the scene height (in length units) that will be projected and fit to the viewport.
            
        """
        return None

    @property
    def SceneWidth(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        
            Specifies the scene width (in length units) that will be projected and fit to the viewport.
            
        """
        return None

    def Rotate(self, angle: "System.Double", axis: "Ansys.Mechanical.DataModel.Enums.CameraAxisType") -> "System.Void":
        """
        
            Rotates the camera about an axis.
            
        """
        pass

    def SetSpecificViewOrientation(self, type: "Ansys.Mechanical.DataModel.Enums.ViewOrientationType") -> "System.Void":
        """
        
            Sets a specific view orientation.
            
        """
        pass

    def SetFit(self, sel: "Ansys.ACT.Interfaces.Common.ISelectionInfo") -> "System.Void":
        """
        
            Fits the view to the specified selection. If null is supplied, fits the view to the entire model.
            
        """
        pass

    def GetAsString(self, appType: "Ansys.Mechanical.DataModel.Enums.ApplicationType") -> "System.String":
        """
        
            Retrieves the view commands as related to the application type as a string.
            
        """
        pass

    def Zoom(self, zoomVal: "System.Double") -> "System.Void":
        """
        
            Zooms in or out on the model. 
            
        """
        pass

    def Pan(self, x: "Ansys.Core.Units.Quantity", y: "Ansys.Core.Units.Quantity") -> "System.Void":
        """
        
            Shifts the camera position horizontally or vertically based on x and y quantities. 
            
        """
        pass


class MechanicalGraphicsWrapper(object):
    """
    
            Wrapper for Graphics in Mechanical.
            
    """

    @property
    def Unit(self) -> typing.Optional["System.String"]:
        """
        
            Gets the current graphics unit.
            
        """
        return None

    @property
    def ModelViewManager(self) -> typing.Optional["Ansys.ACT.Interfaces.Graphics.IModelViewManager"]:
        """
        
            An instance of the ModelViewManager.
            
        """
        return None

    @property
    def KeyframeAnimationUtility(self) -> typing.Optional["Ansys.ACT.Common.Graphics.KeyframeAnimationUtility"]:
        """
        
            A utility for creating animations based on keyframes.
            
        """
        return None

    @property
    def ResultAnimationOptions(self) -> typing.Optional["Ansys.Mechanical.Graphics.ResultAnimationOptions"]:
        """
        
            Gets the Global Result Animation options.
            
        """
        return None

    @property
    def SectionPlanes(self) -> typing.Optional["Ansys.Mechanical.Graphics.SectionPlanes"]:
        """
        
            Returns the collection of section planes used by graphics
            
        """
        return None

    @property
    def ViewOptions(self) -> typing.Optional["Ansys.Mechanical.Graphics.ViewOptions"]:
        """
        
            Gets the Graphics View Options.
            
        """
        return None

    @property
    def GlobalLegendSettings(self) -> typing.Optional["Ansys.Mechanical.Graphics.GlobalLegendSettings"]:
        """
        
            Gets the Global Graphics Legend Settings.
            
        """
        return None

    @property
    def Camera(self) -> typing.Optional["Ansys.ACT.Common.Graphics.MechanicalCameraWrapper"]:
        """
        
            Gets the camera.
            
        """
        return None

    @property
    def Scene(self) -> typing.Optional["Ansys.ACT.Interfaces.Graphics.IGraphicsCollection"]:
        """
        
            Gets the scene.
            
        """
        return None

    def ExportScreenToImage(self, filePath: "System.String") -> "System.Void":
        """
        ExportScreenToImage method.
        """
        pass

    def ExportImage(self, filePath: "System.String", formatImage: "Ansys.Mechanical.DataModel.Enums.GraphicsImageExportFormat", settings: "Ansys.Mechanical.Graphics.GraphicsImageExportSettings") -> "System.Void":
        """
        
            Exports the current graphics display to a 2D image file.
            
        """
        pass

    def ExportViewports(self, filePath: "System.String", format: "Ansys.Mechanical.DataModel.Enums.GraphicsImageExportFormat", settings: "Ansys.Mechanical.Graphics.GraphicsViewportsExportSettings") -> "System.Void":
        """
        
            Creates a composite of images exported from each open viewport.
            
        """
        pass

    def Export3D(self, filePath: "System.String", format3d: "Ansys.Mechanical.DataModel.Enums.Graphics3DExportFormat", settings: "Ansys.Mechanical.Graphics.Graphics3DExportSettings") -> "System.Void":
        """
        
            Exports the current Graphics display in a 3d format to a file.
            
        """
        pass

    def Redraw(self) -> "System.Void":
        """
        
            Forces the scene to redraw its content.
            
        """
        pass

    def Suspend(self) -> "Ansys.ACT.Interfaces.Graphics.ISuspendController":
        """
        
            Prevents the scene to redraw until the Resume controller method was called.
            
        """
        pass

    def ForceResume(self) -> "System.Void":
        """
        
            Forces the scene to resume. Useful in interactive context (console) if a reference on an
            operation has been lost.
            
        """
        pass

    def CreatePixelPoint(self, x: "System.Int32", y: "System.Int32") -> "Ansys.ACT.Interfaces.Graphics.IPixelPoint":
        """
        
            Creates a point from pixel coordinates (ie. window coordinates).
            
        """
        pass

    def CreateWorldPoint(self, x: "System.Double", y: "System.Double", z: "System.Double") -> "Ansys.ACT.Interfaces.Graphics.IWorldPoint":
        """
        
            Create a point from world coordinates.
            
        """
        pass

    def CreateVector3D(self, x: "System.Double", y: "System.Double", z: "System.Double") -> "Ansys.ACT.Interfaces.Graphics.IVector3D":
        """
        
            Create a 3D vector from world coordinates.
            
        """
        pass


class DMGraphicsWrapper(object):
    """
    
            Wrapper for Graphics in Design Modeler.
            
    """

    @property
    def Scene(self) -> typing.Optional["Ansys.ACT.Interfaces.Graphics.IGraphicsCollection"]:
        """
        
            Gets the scene.
            
        """
        return None

    def Redraw(self) -> "System.Void":
        """
        
            Forces the scene to redraw its content.
            
        """
        pass

    def Suspend(self) -> "Ansys.ACT.Interfaces.Graphics.ISuspendController":
        """
        
            Prevents the scene to redraw until the Resume controller method was called.
            
        """
        pass

    def ForceResume(self) -> "System.Void":
        """
        
            Forces the scene to resume. Useful in interactive context (console) if a reference on an
            operation has been lost.
            
        """
        pass

    def CreatePixelPoint(self, x: "System.Int32", y: "System.Int32") -> "Ansys.ACT.Interfaces.Graphics.IPixelPoint":
        """
        
            Creates a point from pixel coordinates (ie. window coordinates).
            
        """
        pass

    def CreateWorldPoint(self, x: "System.Double", y: "System.Double", z: "System.Double") -> "Ansys.ACT.Interfaces.Graphics.IWorldPoint":
        """
        
            Create a point from world coordinates.
            
        """
        pass

    def CreateVector3D(self, x: "System.Double", y: "System.Double", z: "System.Double") -> "Ansys.ACT.Interfaces.Graphics.IVector3D":
        """
        
            Create a 3D vector from world coordinates.
            
        """
        pass

    def ExportScreenToImage(self, filePath: "System.String") -> "System.Void":
        """
        
            Exports the current Graphics screen to a file.
            
        """
        pass


class ModelViewManager(object):
    """
    ModelViewManager class.
    """

    @property
    def NumberOfViews(self) -> typing.Optional["System.Int32"]:
        """
        
            The number of views currently defined.
            
        """
        return None

    @property
    def ActiveViewPort(self) -> typing.Optional["Ansys.ACT.Common.Graphics.MechanicalViewPort"]:
        """
        ActiveViewPort property.
        """
        return None

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

    def DeleteView(self, viewLabel: "System.String") -> "System.Void":
        """
        
            Delete the specified view by name.
            
        """
        pass

    def DeleteView(self, viewIndex: "System.Int32") -> "System.Void":
        """
        
            Delete the specified view by index.
            
        """
        pass

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

    def ImportModelViews(self, viewfilepath: "System.String") -> "System.Void":
        """
        
            Import model views from the specified file.
            
        """
        pass

    def ExportModelViews(self, viewfilepath: "System.String") -> "System.Void":
        """
        
            Export model views to the specified file.
            
        """
        pass

    def SetViewPorts(self, numViewPorts: "System.Int32", horizontal: "System.Boolean") -> "System.Void":
        """
        
            Set the number of viewports displayed.
            
        """
        pass

    def SetActiveViewPort(self, winRowIndex: "System.Int32", winColIndex: "System.Int32") -> "System.Void":
        """
        
            Set the active of viewport.
            
        """
        pass

    def SetActiveViewPort(self, windowsId: "System.Int32") -> "System.Void":
        """
        
            Active a viewport.
            
        """
        pass


