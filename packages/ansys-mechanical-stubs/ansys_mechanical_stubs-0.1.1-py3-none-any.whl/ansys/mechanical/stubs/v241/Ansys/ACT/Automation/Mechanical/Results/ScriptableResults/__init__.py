"""ScriptableResults subpackage."""
import typing

class PythonResult(object):
    """
    Defines a PythonResult.
    """

    @property
    def InternalObject(self) -> typing.Optional["Ansys.Common.Interop.DSObjectsAuto.IDSScriptDefinedResultAuto"]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def Mode(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the Mode.
        """
        return None

    @property
    def DisplayTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets or sets the DisplayTime.
        """
        return None

    @property
    def By(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.SetDriverStyle"]:
        """
        Gets or sets the By.
        """
        return None

    @property
    def Location(self) -> typing.Optional["Ansys.ACT.Interfaces.Common.ISelectionInfo"]:
        """
        Gets or sets the Location.
        """
        return None

    @property
    def DataModelObjectCategory(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory"]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def Children(self) -> typing.Optional["System.Collections.Generic.IList[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]"]:
        """
        Gets the list of children.
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
    def Text(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the text in the script tab for the Python Code object.
        """
        return None

    @property
    def PropertyProvider(self) -> typing.Optional["Ansys.ACT.Interfaces.Mechanical.IPropertyProvider"]:
        """
        
            Gets or sets the propperty provider instance associated with this python code object.
            
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional["Ansys.Common.Interop.DSObjectsAuto.IDSPythonCodeAuto"]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ScriptExecutionScope(self) -> typing.Optional["System.String"]:
        """
        The scope identifier in which the code execution will take place.
        """
        return None

    @property
    def Connected(self) -> typing.Optional["System.Boolean"]:
        """
        Gets whether the callbacks are currently connected.
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

    def Evaluate(self) -> "System.Void":
        """
        Evaluate method.
        """
        pass

    def EvaluateAllResults(self) -> "System.Void":
        """
        Evaluate all results.
        """
        pass

    def ClearGeneratedData(self) -> "System.Void":
        """
        ClearGeneratedData method.
        """
        pass

    def ExportAnimation(self, filePath: "System.String", format: "Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat", settings: "Ansys.Mechanical.Graphics.AnimationExportSettings") -> "System.Void":
        """
        Run the ExportAnimation action.
        """
        pass

    def GetChildren(self, recurses: "System.Boolean", children: "System.Collections.Generic.IList[ChildrenType]") -> "System.Collections.Generic.IList[ChildrenType]":
        """
        Gets the list of children, filtered by type.
        """
        pass

    def GetChildren(self, category: "Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory", recurses: "System.Boolean", children: "System.Collections.Generic.IList[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]") -> "System.Collections.Generic.IList[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]":
        """
        Gets the list of children, filtered by type.
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

    def ReloadProperties(self) -> "System.Void":
        """
        
            Reload properties to update properties provided by the provider.
            
        """
        pass

    def Connect(self) -> "System.Void":
        """
        
            Register the python code.
            
        """
        pass

    def Delete(self) -> "System.Void":
        """
        Run the Delete action.
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


class ScriptDefinedResultFolder(object):
    """
    Defines a ScriptDefinedResultFolder.
    """

    @property
    def InternalObject(self) -> typing.Optional["Ansys.Common.Interop.DSObjectsAuto.IDSScriptResultFolderAuto"]:
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
    def Children(self) -> typing.Optional["System.Collections.Generic.IList[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]"]:
        """
        Gets the list of children.
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

    def EvaluateAllResults(self) -> "System.Void":
        """
        EvaluatesAllResults.
        """
        pass

    def AddPythonResult(self) -> "Ansys.ACT.Automation.Mechanical.Results.ScriptableResults.PythonResult":
        """
        Creates a new PythonResult
        """
        pass

    def GetChildren(self, recurses: "System.Boolean", children: "System.Collections.Generic.IList[ChildrenType]") -> "System.Collections.Generic.IList[ChildrenType]":
        """
        Gets the list of children, filtered by type.
        """
        pass

    def GetChildren(self, category: "Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory", recurses: "System.Boolean", children: "System.Collections.Generic.IList[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]") -> "System.Collections.Generic.IList[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]":
        """
        Gets the list of children, filtered by type.
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


