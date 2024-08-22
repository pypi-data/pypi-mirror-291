"""ConstructionLines subpackage."""
import typing

class ConstructionLine(object):
    """
    
                
    """

    @property
    def Edges(self) -> typing.Optional["System.Collections.Generic.IList[System.Object]"]:
        """
        
                Creates for the user an IEdge representation of each edge in this Construction Line.
            
        """
        return None

    @property
    def Points(self) -> typing.Optional["System.Collections.Generic.IList[System.Object]"]:
        """
        
                Returns all points in this Construction Line, both those that have been created
                as well as virtual representations.
            
        """
        return None

    @property
    def Planes(self) -> typing.Optional["System.Collections.Generic.IList[System.Object]"]:
        """
        
                Creates for the user an Plane representation of each plane in this Construction Line.
            
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional["Ansys.Common.Interop.DSLines.IDSLinesPythonInteraction"]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def DataModelObjectCategory(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory"]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def Comments(self) -> typing.Optional["System.Collections.Generic.IEnumerable[Ansys.ACT.Automation.Mechanical.Comment]"]:
        """
        Gets the list of associated comments.
        """
        return None

    @property
    def Figures(self) -> typing.Optional["System.Collections.Generic.IEnumerable[Ansys.ACT.Automation.Mechanical.Figure]"]:
        """
        Gets the list of associated figures.
        """
        return None

    @property
    def Images(self) -> typing.Optional["System.Collections.Generic.IEnumerable[Ansys.ACT.Automation.Mechanical.Image]"]:
        """
        Gets the list of associated images.
        """
        return None

    @property
    def ReadOnly(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the ReadOnly.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional["System.Object"]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def Properties(self) -> typing.Optional["System.Collections.Generic.IReadOnlyList[Ansys.ACT.Automation.Mechanical.Property]"]:
        """
        
            Gets the list of properties for this object.
            
        """
        return None

    @property
    def VisibleProperties(self) -> typing.Optional["System.Collections.Generic.IReadOnlyList[Ansys.ACT.Automation.Mechanical.Property]"]:
        """
        
            Gets the list of properties that are visible for this object.
            
        """
        return None

    def CreatePoints(self, pointDefinitionCollection: "System.Collections.Generic.IEnumerable[System.Object]") -> "System.Collections.Generic.IList[System.Object]":
        """
        CreatePoints method.
        """
        pass

    def CreatePlanarPoints(self, plane: "Ansys.Mechanical.DataModel.ConstructionLines.Plane", pointDefinitionCollection: "System.Collections.Generic.IEnumerable[System.Object]") -> "System.Collections.Generic.IList[System.Object]":
        """
        CreatePlanarPoints method.
        """
        pass

    def CreatePlane(self, sketchPlaneDefinition: "System.Object") -> "Ansys.Mechanical.DataModel.ConstructionLines.Plane":
        """
        
                Create a plane.
            
        """
        pass

    def CreateStraightLines(self, pointCollection: "System.Collections.Generic.IEnumerable[Ansys.Mechanical.DataModel.ConstructionLines.Point]") -> "System.Collections.Generic.IList[System.Object]":
        """
        CreateStraightLines method.
        """
        pass

    def CreateStraightLines(self, pointCollection: "System.Collections.Generic.IEnumerable[Ansys.Mechanical.DataModel.ConstructionLines.Point]", connectionCollection: "System.Collections.Generic.IEnumerable[System.Collections.Generic.IEnumerable[System.Object]]") -> "System.Collections.Generic.IList[System.Object]":
        """
        CreateStraightLines method.
        """
        pass

    def FlipEdges(self, edgesToFlip: "System.Collections.Generic.IEnumerable[Ansys.Mechanical.DataModel.ConstructionLines.Edges.IEdge]") -> "System.Void":
        """
        FlipEdges method.
        """
        pass

    def DeleteEdges(self, edgeCollection: "System.Collections.Generic.IEnumerable[Ansys.Mechanical.DataModel.ConstructionLines.Edges.IEdge]") -> "System.Void":
        """
        DeleteEdges method.
        """
        pass

    def DeletePlane(self, plane: "Ansys.Mechanical.DataModel.ConstructionLines.Plane", forceDelete: "System.Boolean") -> "System.Void":
        """
        
                Delete a plane associated with this construction line.
            
        """
        pass

    def AddToGeometry(self) -> "Ansys.ACT.Interfaces.Geometry.IGeoPart":
        """
        
                Add a part to Geometry with line bodies as contained in this ConstructionLine instance.
            
        """
        pass

    def UpdateGeometry(self) -> "System.Void":
        """
        
                Update the corresponding part with any changes made in this ConstructionLine instance.
            
        """
        pass

    def RemoveFromGeometry(self) -> "System.Void":
        """
        
                Remove the corresponding part from the geometry.
            
        """
        pass

    def GetPartFromGeometry(self) -> "Ansys.ACT.Interfaces.Geometry.IGeoPart":
        """
        
                Get the corresponding part for a ConstructionLine instance.
            
        """
        pass

    def Undo(self) -> "System.Void":
        """
        
                Undo the last operation in this Construction Line instance.
            
        """
        pass

    def Redo(self) -> "System.Void":
        """
        
                Redo and undone operation in this Construction Line instance.
            
        """
        pass

    def AddComment(self) -> "Ansys.ACT.Automation.Mechanical.Comment":
        """
        Creates a new child Comment.
        """
        pass

    def AddFigure(self) -> "Ansys.ACT.Automation.Mechanical.Figure":
        """
        Creates a new child Figure.
        """
        pass

    def AddImage(self, filePath: "System.String") -> "Ansys.ACT.Automation.Mechanical.Image":
        """
        
            Creates a new child Image.
            If a filePath is provided, the image will be loaded from that file,
            if not, the image will be a screen capture of the Geometry window.
            
        """
        pass

    def Activate(self) -> "System.Void":
        """
        Activate the current object.
        """
        pass

    def CopyTo(self, other: "Ansys.ACT.Automation.Mechanical.DataModelObject") -> "System.Void":
        """
        
            Copies all visible properties from this object to another.
            
        """
        pass

    def Duplicate(self) -> "Ansys.Mechanical.DataModel.Interfaces.IDataModelObject":
        """
        
            Creates a copy of the current DataModelObject.
            
        """
        pass

    def GroupAllSimilarChildren(self) -> "System.Void":
        """
        Run the GroupAllSimilarChildren action.
        """
        pass

    def GroupSimilarObjects(self) -> "Ansys.ACT.Automation.Mechanical.TreeGroupingFolder":
        """
        Run the GroupSimilarObjects action.
        """
        pass

    def PropertyByName(self, name: "System.String") -> "Ansys.ACT.Automation.Mechanical.Property":
        """
        
            Get a property by its unique name.
            
        """
        pass

    def PropertyByAPIName(self, name: "System.String") -> "Ansys.ACT.Automation.Mechanical.Property":
        """
        
            Get a property by its API name.
            If multiple properties have the same API Name, only the first property with that name will be returned.
            
        """
        pass

    def CreateParameter(self, propName: "System.String") -> "Ansys.ACT.Interfaces.Mechanical.IParameter":
        """
        
            Creates a new parameter for a Property.
            
        """
        pass

    def GetParameter(self, propName: "System.String") -> "Ansys.ACT.Interfaces.Mechanical.IParameter":
        """
        
            Gets the parameter corresponding to the given property.
            
        """
        pass

    def RemoveParameter(self, propName: "System.String") -> "System.Void":
        """
        
            Removes the parameter from the parameter set corresponding to the given property.
            
        """
        pass


