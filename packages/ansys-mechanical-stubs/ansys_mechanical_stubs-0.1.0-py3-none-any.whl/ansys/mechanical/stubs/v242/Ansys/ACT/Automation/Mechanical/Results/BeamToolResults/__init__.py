"""BeamToolResults subpackage."""
import typing

class BeamTool(object):
    """
    Defines a BeamTool.
    """

    @property
    def InternalObject(self) -> typing.Optional["Ansys.Common.Interop.DSObjectsAuto.IDSBeamToolAuto"]:
        """
        Gets the internal object. For advanced usage only.
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
        Run the EvaluateAllResults action.
        """
        pass

    def AddDirectionalDeformation(self) -> "Ansys.ACT.Automation.Mechanical.Results.DeformationResults.DirectionalDeformation":
        """
        Creates a new DirectionalDeformation
        """
        pass

    def AddDirectStress(self) -> "Ansys.ACT.Automation.Mechanical.Results.BeamToolResults.DirectStress":
        """
        Creates a new DirectStress
        """
        pass

    def AddMaximumBendingStress(self) -> "Ansys.ACT.Automation.Mechanical.Results.BeamToolResults.MaximumBendingStress":
        """
        Creates a new MaximumBendingStress
        """
        pass

    def AddMaximumCombinedStress(self) -> "Ansys.ACT.Automation.Mechanical.Results.BeamToolResults.MaximumCombinedStress":
        """
        Creates a new MaximumCombinedStress
        """
        pass

    def AddMinimumBendingStress(self) -> "Ansys.ACT.Automation.Mechanical.Results.BeamToolResults.MinimumBendingStress":
        """
        Creates a new MinimumBendingStress
        """
        pass

    def AddMinimumCombinedStress(self) -> "Ansys.ACT.Automation.Mechanical.Results.BeamToolResults.MinimumCombinedStress":
        """
        Creates a new MinimumCombinedStress
        """
        pass

    def AddTotalDeformation(self) -> "Ansys.ACT.Automation.Mechanical.Results.DeformationResults.TotalDeformation":
        """
        Creates a new TotalDeformation
        """
        pass

    def Delete(self) -> "System.Void":
        """
        Run the Delete action.
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


class BeamToolResult(object):
    """
    Defines a BeamToolResult.
    """

    @property
    def InternalObject(self) -> typing.Optional["Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto"]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def BeamToolStressResultType(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.BeamToolStressResultType"]:
        """
        Gets or sets the BeamToolStressResultType.
        """
        return None

    @property
    def DataModelObjectCategory(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory"]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def PlotData(self) -> typing.Optional["Ansys.Mechanical.DataModel.Results.ResultDataTable"]:
        """
        Gets the result table.
        """
        return None

    @property
    def Location(self) -> typing.Optional["Ansys.ACT.Interfaces.Common.ISelectionInfo"]:
        """
        Gets or sets the Location.
        """
        return None

    @property
    def TimeForMinimumOfMinimumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the minimum of minimum values.
        """
        return None

    @property
    def TimeForMinimumOfMaximumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the minimum of maximum values.
        """
        return None

    @property
    def LoadStepForMinimumOfMinimumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the minimum of minimum values.
        """
        return None

    @property
    def LoadStepForMinimumOfMaximumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the minimum of maximum values.
        """
        return None

    @property
    def TimeForMaximumOfMinimumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the maximum of minimum values.
        """
        return None

    @property
    def TimeForMaximumOfMaximumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the maximum of maximum values.
        """
        return None

    @property
    def LoadStepForMaximumOfMinimumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the maximum of minimum values.
        """
        return None

    @property
    def LoadStepForMaximumOfMaximumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the maximum of maximum values.
        """
        return None

    @property
    def IsSolved(self) -> typing.Optional["System.Boolean"]:
        """
        Gets the IsSolved.
        """
        return None

    @property
    def CoordinateSystem(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.CoordinateSystem"]:
        """
        
            Gets or sets the Coordinate System. 
            Accepts/Returns None for Solution Coordinate System in the general case (if applicable). 
            Accepts/Returns None for Fiber Coordinate System for a result that is sub scoped by ply.
            
        """
        return None

    @property
    def ScopingMethod(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GeometryDefineByType"]:
        """
        Gets or sets the ScopingMethod.
        """
        return None

    @property
    def SetNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the Set Number.
        """
        return None

    @property
    def CombinationNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the Combination Number for a Solution Combination result.
        """
        return None

    @property
    def SolutionCombinationDriver(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.SolutionCombinationDriverStyle"]:
        """
        Gets or sets the SolutionCombinationDriver.
        """
        return None

    @property
    def Path(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.Path"]:
        """
        Path property.
        """
        return None

    @property
    def Surface(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.Surface"]:
        """
        Surface property.
        """
        return None

    @property
    def SurfaceCoating(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.SurfaceCoating"]:
        """
        SurfaceCoating property.
        """
        return None

    @property
    def NamedSelections(self) -> typing.Optional["System.Collections.Generic.IEnumerable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]"]:
        """
        Gets or sets the NamedSelections.
        """
        return None

    @property
    def WaterfallShowTextOnMosaic(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the Waterfall Mosaic Text Property.
        """
        return None

    @property
    def CrackFrontNumber(self) -> typing.Optional["System.Int32"]:
        """
        Gets or sets the CrackFrontNumber.
        """
        return None

    @property
    def GlobalIDs(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the GlobalIDs.
        """
        return None

    @property
    def Identifier(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the Identifier.
        """
        return None

    @property
    def IterationNumber(self) -> typing.Optional["System.Int32"]:
        """
        Gets the IterationNumber.
        """
        return None

    @property
    def LoadStep(self) -> typing.Optional["System.Int32"]:
        """
        Gets the LoadStep.
        """
        return None

    @property
    def MaximumOccursOn(self) -> typing.Optional["System.String"]:
        """
        Gets the MaximumOccursOn.
        """
        return None

    @property
    def MinimumOccursOn(self) -> typing.Optional["System.String"]:
        """
        Gets the MinimumOccursOn.
        """
        return None

    @property
    def LoadStepNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the LoadStepNumber.
        """
        return None

    @property
    def SolverComponentIDs(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the SolverComponentIDs.
        """
        return None

    @property
    def Substep(self) -> typing.Optional["System.Int32"]:
        """
        Gets the Substep.
        """
        return None

    @property
    def Average(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Average.
        """
        return None

    @property
    def Maximum(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Maximum.
        """
        return None

    @property
    def MaximumOfMaximumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MaximumOfMaximumOverTime.
        """
        return None

    @property
    def MaximumOfMinimumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MaximumOfMinimumOverTime.
        """
        return None

    @property
    def Minimum(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Minimum.
        """
        return None

    @property
    def MinimumOfMaximumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MinimumOfMaximumOverTime.
        """
        return None

    @property
    def MinimumOfMinimumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MinimumOfMinimumOverTime.
        """
        return None

    @property
    def Time(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Time.
        """
        return None

    @property
    def DisplayTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets or sets the DisplayTime.
        """
        return None

    @property
    def GraphControlsXAxis(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GraphControlsXAxis"]:
        """
        Gets or sets the GraphControlsXAxis.
        """
        return None

    @property
    def DisplayOption(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.ResultAveragingType"]:
        """
        Gets or sets the DisplayOption.
        """
        return None

    @property
    def DpfEvaluation(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.DpfEvaluationType"]:
        """
        Gets or sets the DpfEvaluation.
        """
        return None

    @property
    def By(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.SetDriverStyle"]:
        """
        Gets or sets the By.
        """
        return None

    @property
    def ItemType(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.ResultFileItemType"]:
        """
        Gets or sets the ItemType.
        """
        return None

    @property
    def CalculateTimeHistory(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the CalculateTimeHistory.
        """
        return None

    @property
    def Suppressed(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the Suppressed.
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

    def ClearGeneratedData(self) -> "System.Void":
        """
        Run the ClearGeneratedData action.
        """
        pass

    def EvaluateAllResults(self) -> "System.Void":
        """
        Run the EvaluateAllResults action.
        """
        pass

    def FetchRemoteResults(self) -> "System.Void":
        """
        Run the FetchRemoteResult action.
        """
        pass

    def ExportToTextFile(self, filePath: "System.String") -> "System.Void":
        """
        Run the ExportToTextFile action.
        """
        pass

    def ExportAnimation(self, filePath: "System.String", format: "Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat", settings: "Ansys.Mechanical.Graphics.AnimationExportSettings") -> "System.Void":
        """
        Run the ExportAnimation action.
        """
        pass

    def DuplicateWithoutResults(self) -> "Ansys.Mechanical.DataModel.Interfaces.IDataModelObject":
        """
        Run the DuplicateWithoutResults action.
        """
        pass

    def CreateResultsAtAllSets(self) -> "System.Collections.Generic.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]":
        """
        Creates results at all sets for results under a solution.
        """
        pass

    def PromoteToNamedSelection(self) -> "System.Collections.Generic.IEnumerable[Ansys.ACT.Automation.Mechanical.NamedSelection]":
        """
        Run the PromoteToNamedSelection action.
        """
        pass

    def CreateParameter(self, propName: "System.String") -> "Ansys.ACT.Interfaces.Mechanical.IParameter":
        """
        CreateParameter method.
        """
        pass

    def AddAlert(self) -> "Ansys.ACT.Automation.Mechanical.Results.Alert":
        """
        Creates a new Alert
        """
        pass

    def AddConvergence(self) -> "Ansys.ACT.Automation.Mechanical.Results.Convergence":
        """
        Creates a new Convergence
        """
        pass

    def RenameBasedOnDefinition(self) -> "System.Void":
        """
        Run the RenameBasedOnDefinition action.
        """
        pass

    def Delete(self) -> "System.Void":
        """
        Run the Delete action.
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


class DirectStress(object):
    """
    Defines a DirectStress.
    """

    @property
    def InternalObject(self) -> typing.Optional["Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto"]:
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
    def BeamToolStressResultType(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.BeamToolStressResultType"]:
        """
        Gets or sets the BeamToolStressResultType.
        """
        return None

    @property
    def PlotData(self) -> typing.Optional["Ansys.Mechanical.DataModel.Results.ResultDataTable"]:
        """
        Gets the result table.
        """
        return None

    @property
    def Location(self) -> typing.Optional["Ansys.ACT.Interfaces.Common.ISelectionInfo"]:
        """
        Gets or sets the Location.
        """
        return None

    @property
    def TimeForMinimumOfMinimumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the minimum of minimum values.
        """
        return None

    @property
    def TimeForMinimumOfMaximumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the minimum of maximum values.
        """
        return None

    @property
    def LoadStepForMinimumOfMinimumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the minimum of minimum values.
        """
        return None

    @property
    def LoadStepForMinimumOfMaximumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the minimum of maximum values.
        """
        return None

    @property
    def TimeForMaximumOfMinimumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the maximum of minimum values.
        """
        return None

    @property
    def TimeForMaximumOfMaximumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the maximum of maximum values.
        """
        return None

    @property
    def LoadStepForMaximumOfMinimumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the maximum of minimum values.
        """
        return None

    @property
    def LoadStepForMaximumOfMaximumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the maximum of maximum values.
        """
        return None

    @property
    def IsSolved(self) -> typing.Optional["System.Boolean"]:
        """
        Gets the IsSolved.
        """
        return None

    @property
    def CoordinateSystem(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.CoordinateSystem"]:
        """
        
            Gets or sets the Coordinate System. 
            Accepts/Returns None for Solution Coordinate System in the general case (if applicable). 
            Accepts/Returns None for Fiber Coordinate System for a result that is sub scoped by ply.
            
        """
        return None

    @property
    def ScopingMethod(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GeometryDefineByType"]:
        """
        Gets or sets the ScopingMethod.
        """
        return None

    @property
    def SetNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the Set Number.
        """
        return None

    @property
    def CombinationNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the Combination Number for a Solution Combination result.
        """
        return None

    @property
    def SolutionCombinationDriver(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.SolutionCombinationDriverStyle"]:
        """
        Gets or sets the SolutionCombinationDriver.
        """
        return None

    @property
    def Path(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.Path"]:
        """
        Path property.
        """
        return None

    @property
    def Surface(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.Surface"]:
        """
        Surface property.
        """
        return None

    @property
    def SurfaceCoating(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.SurfaceCoating"]:
        """
        SurfaceCoating property.
        """
        return None

    @property
    def NamedSelections(self) -> typing.Optional["System.Collections.Generic.IEnumerable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]"]:
        """
        Gets or sets the NamedSelections.
        """
        return None

    @property
    def WaterfallShowTextOnMosaic(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the Waterfall Mosaic Text Property.
        """
        return None

    @property
    def CrackFrontNumber(self) -> typing.Optional["System.Int32"]:
        """
        Gets or sets the CrackFrontNumber.
        """
        return None

    @property
    def GlobalIDs(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the GlobalIDs.
        """
        return None

    @property
    def Identifier(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the Identifier.
        """
        return None

    @property
    def IterationNumber(self) -> typing.Optional["System.Int32"]:
        """
        Gets the IterationNumber.
        """
        return None

    @property
    def LoadStep(self) -> typing.Optional["System.Int32"]:
        """
        Gets the LoadStep.
        """
        return None

    @property
    def MaximumOccursOn(self) -> typing.Optional["System.String"]:
        """
        Gets the MaximumOccursOn.
        """
        return None

    @property
    def MinimumOccursOn(self) -> typing.Optional["System.String"]:
        """
        Gets the MinimumOccursOn.
        """
        return None

    @property
    def LoadStepNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the LoadStepNumber.
        """
        return None

    @property
    def SolverComponentIDs(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the SolverComponentIDs.
        """
        return None

    @property
    def Substep(self) -> typing.Optional["System.Int32"]:
        """
        Gets the Substep.
        """
        return None

    @property
    def Average(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Average.
        """
        return None

    @property
    def Maximum(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Maximum.
        """
        return None

    @property
    def MaximumOfMaximumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MaximumOfMaximumOverTime.
        """
        return None

    @property
    def MaximumOfMinimumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MaximumOfMinimumOverTime.
        """
        return None

    @property
    def Minimum(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Minimum.
        """
        return None

    @property
    def MinimumOfMaximumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MinimumOfMaximumOverTime.
        """
        return None

    @property
    def MinimumOfMinimumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MinimumOfMinimumOverTime.
        """
        return None

    @property
    def Time(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Time.
        """
        return None

    @property
    def DisplayTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets or sets the DisplayTime.
        """
        return None

    @property
    def GraphControlsXAxis(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GraphControlsXAxis"]:
        """
        Gets or sets the GraphControlsXAxis.
        """
        return None

    @property
    def DisplayOption(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.ResultAveragingType"]:
        """
        Gets or sets the DisplayOption.
        """
        return None

    @property
    def DpfEvaluation(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.DpfEvaluationType"]:
        """
        Gets or sets the DpfEvaluation.
        """
        return None

    @property
    def By(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.SetDriverStyle"]:
        """
        Gets or sets the By.
        """
        return None

    @property
    def ItemType(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.ResultFileItemType"]:
        """
        Gets or sets the ItemType.
        """
        return None

    @property
    def CalculateTimeHistory(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the CalculateTimeHistory.
        """
        return None

    @property
    def Suppressed(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the Suppressed.
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

    def ClearGeneratedData(self) -> "System.Void":
        """
        Run the ClearGeneratedData action.
        """
        pass

    def EvaluateAllResults(self) -> "System.Void":
        """
        Run the EvaluateAllResults action.
        """
        pass

    def FetchRemoteResults(self) -> "System.Void":
        """
        Run the FetchRemoteResult action.
        """
        pass

    def ExportToTextFile(self, filePath: "System.String") -> "System.Void":
        """
        Run the ExportToTextFile action.
        """
        pass

    def ExportAnimation(self, filePath: "System.String", format: "Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat", settings: "Ansys.Mechanical.Graphics.AnimationExportSettings") -> "System.Void":
        """
        Run the ExportAnimation action.
        """
        pass

    def DuplicateWithoutResults(self) -> "Ansys.Mechanical.DataModel.Interfaces.IDataModelObject":
        """
        Run the DuplicateWithoutResults action.
        """
        pass

    def CreateResultsAtAllSets(self) -> "System.Collections.Generic.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]":
        """
        Creates results at all sets for results under a solution.
        """
        pass

    def PromoteToNamedSelection(self) -> "System.Collections.Generic.IEnumerable[Ansys.ACT.Automation.Mechanical.NamedSelection]":
        """
        Run the PromoteToNamedSelection action.
        """
        pass

    def CreateParameter(self, propName: "System.String") -> "Ansys.ACT.Interfaces.Mechanical.IParameter":
        """
        CreateParameter method.
        """
        pass

    def AddAlert(self) -> "Ansys.ACT.Automation.Mechanical.Results.Alert":
        """
        Creates a new Alert
        """
        pass

    def AddConvergence(self) -> "Ansys.ACT.Automation.Mechanical.Results.Convergence":
        """
        Creates a new Convergence
        """
        pass

    def RenameBasedOnDefinition(self) -> "System.Void":
        """
        Run the RenameBasedOnDefinition action.
        """
        pass

    def Delete(self) -> "System.Void":
        """
        Run the Delete action.
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


class MaximumBendingStress(object):
    """
    Defines a MaximumBendingStress.
    """

    @property
    def InternalObject(self) -> typing.Optional["Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto"]:
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
    def BeamToolStressResultType(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.BeamToolStressResultType"]:
        """
        Gets or sets the BeamToolStressResultType.
        """
        return None

    @property
    def PlotData(self) -> typing.Optional["Ansys.Mechanical.DataModel.Results.ResultDataTable"]:
        """
        Gets the result table.
        """
        return None

    @property
    def Location(self) -> typing.Optional["Ansys.ACT.Interfaces.Common.ISelectionInfo"]:
        """
        Gets or sets the Location.
        """
        return None

    @property
    def TimeForMinimumOfMinimumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the minimum of minimum values.
        """
        return None

    @property
    def TimeForMinimumOfMaximumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the minimum of maximum values.
        """
        return None

    @property
    def LoadStepForMinimumOfMinimumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the minimum of minimum values.
        """
        return None

    @property
    def LoadStepForMinimumOfMaximumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the minimum of maximum values.
        """
        return None

    @property
    def TimeForMaximumOfMinimumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the maximum of minimum values.
        """
        return None

    @property
    def TimeForMaximumOfMaximumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the maximum of maximum values.
        """
        return None

    @property
    def LoadStepForMaximumOfMinimumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the maximum of minimum values.
        """
        return None

    @property
    def LoadStepForMaximumOfMaximumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the maximum of maximum values.
        """
        return None

    @property
    def IsSolved(self) -> typing.Optional["System.Boolean"]:
        """
        Gets the IsSolved.
        """
        return None

    @property
    def CoordinateSystem(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.CoordinateSystem"]:
        """
        
            Gets or sets the Coordinate System. 
            Accepts/Returns None for Solution Coordinate System in the general case (if applicable). 
            Accepts/Returns None for Fiber Coordinate System for a result that is sub scoped by ply.
            
        """
        return None

    @property
    def ScopingMethod(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GeometryDefineByType"]:
        """
        Gets or sets the ScopingMethod.
        """
        return None

    @property
    def SetNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the Set Number.
        """
        return None

    @property
    def CombinationNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the Combination Number for a Solution Combination result.
        """
        return None

    @property
    def SolutionCombinationDriver(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.SolutionCombinationDriverStyle"]:
        """
        Gets or sets the SolutionCombinationDriver.
        """
        return None

    @property
    def Path(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.Path"]:
        """
        Path property.
        """
        return None

    @property
    def Surface(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.Surface"]:
        """
        Surface property.
        """
        return None

    @property
    def SurfaceCoating(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.SurfaceCoating"]:
        """
        SurfaceCoating property.
        """
        return None

    @property
    def NamedSelections(self) -> typing.Optional["System.Collections.Generic.IEnumerable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]"]:
        """
        Gets or sets the NamedSelections.
        """
        return None

    @property
    def WaterfallShowTextOnMosaic(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the Waterfall Mosaic Text Property.
        """
        return None

    @property
    def CrackFrontNumber(self) -> typing.Optional["System.Int32"]:
        """
        Gets or sets the CrackFrontNumber.
        """
        return None

    @property
    def GlobalIDs(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the GlobalIDs.
        """
        return None

    @property
    def Identifier(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the Identifier.
        """
        return None

    @property
    def IterationNumber(self) -> typing.Optional["System.Int32"]:
        """
        Gets the IterationNumber.
        """
        return None

    @property
    def LoadStep(self) -> typing.Optional["System.Int32"]:
        """
        Gets the LoadStep.
        """
        return None

    @property
    def MaximumOccursOn(self) -> typing.Optional["System.String"]:
        """
        Gets the MaximumOccursOn.
        """
        return None

    @property
    def MinimumOccursOn(self) -> typing.Optional["System.String"]:
        """
        Gets the MinimumOccursOn.
        """
        return None

    @property
    def LoadStepNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the LoadStepNumber.
        """
        return None

    @property
    def SolverComponentIDs(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the SolverComponentIDs.
        """
        return None

    @property
    def Substep(self) -> typing.Optional["System.Int32"]:
        """
        Gets the Substep.
        """
        return None

    @property
    def Average(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Average.
        """
        return None

    @property
    def Maximum(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Maximum.
        """
        return None

    @property
    def MaximumOfMaximumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MaximumOfMaximumOverTime.
        """
        return None

    @property
    def MaximumOfMinimumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MaximumOfMinimumOverTime.
        """
        return None

    @property
    def Minimum(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Minimum.
        """
        return None

    @property
    def MinimumOfMaximumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MinimumOfMaximumOverTime.
        """
        return None

    @property
    def MinimumOfMinimumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MinimumOfMinimumOverTime.
        """
        return None

    @property
    def Time(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Time.
        """
        return None

    @property
    def DisplayTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets or sets the DisplayTime.
        """
        return None

    @property
    def GraphControlsXAxis(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GraphControlsXAxis"]:
        """
        Gets or sets the GraphControlsXAxis.
        """
        return None

    @property
    def DisplayOption(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.ResultAveragingType"]:
        """
        Gets or sets the DisplayOption.
        """
        return None

    @property
    def DpfEvaluation(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.DpfEvaluationType"]:
        """
        Gets or sets the DpfEvaluation.
        """
        return None

    @property
    def By(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.SetDriverStyle"]:
        """
        Gets or sets the By.
        """
        return None

    @property
    def ItemType(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.ResultFileItemType"]:
        """
        Gets or sets the ItemType.
        """
        return None

    @property
    def CalculateTimeHistory(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the CalculateTimeHistory.
        """
        return None

    @property
    def Suppressed(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the Suppressed.
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

    def ClearGeneratedData(self) -> "System.Void":
        """
        Run the ClearGeneratedData action.
        """
        pass

    def EvaluateAllResults(self) -> "System.Void":
        """
        Run the EvaluateAllResults action.
        """
        pass

    def FetchRemoteResults(self) -> "System.Void":
        """
        Run the FetchRemoteResult action.
        """
        pass

    def ExportToTextFile(self, filePath: "System.String") -> "System.Void":
        """
        Run the ExportToTextFile action.
        """
        pass

    def ExportAnimation(self, filePath: "System.String", format: "Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat", settings: "Ansys.Mechanical.Graphics.AnimationExportSettings") -> "System.Void":
        """
        Run the ExportAnimation action.
        """
        pass

    def DuplicateWithoutResults(self) -> "Ansys.Mechanical.DataModel.Interfaces.IDataModelObject":
        """
        Run the DuplicateWithoutResults action.
        """
        pass

    def CreateResultsAtAllSets(self) -> "System.Collections.Generic.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]":
        """
        Creates results at all sets for results under a solution.
        """
        pass

    def PromoteToNamedSelection(self) -> "System.Collections.Generic.IEnumerable[Ansys.ACT.Automation.Mechanical.NamedSelection]":
        """
        Run the PromoteToNamedSelection action.
        """
        pass

    def CreateParameter(self, propName: "System.String") -> "Ansys.ACT.Interfaces.Mechanical.IParameter":
        """
        CreateParameter method.
        """
        pass

    def AddAlert(self) -> "Ansys.ACT.Automation.Mechanical.Results.Alert":
        """
        Creates a new Alert
        """
        pass

    def AddConvergence(self) -> "Ansys.ACT.Automation.Mechanical.Results.Convergence":
        """
        Creates a new Convergence
        """
        pass

    def RenameBasedOnDefinition(self) -> "System.Void":
        """
        Run the RenameBasedOnDefinition action.
        """
        pass

    def Delete(self) -> "System.Void":
        """
        Run the Delete action.
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


class MaximumCombinedStress(object):
    """
    Defines a MaximumCombinedStress.
    """

    @property
    def InternalObject(self) -> typing.Optional["Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto"]:
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
    def BeamToolStressResultType(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.BeamToolStressResultType"]:
        """
        Gets or sets the BeamToolStressResultType.
        """
        return None

    @property
    def PlotData(self) -> typing.Optional["Ansys.Mechanical.DataModel.Results.ResultDataTable"]:
        """
        Gets the result table.
        """
        return None

    @property
    def Location(self) -> typing.Optional["Ansys.ACT.Interfaces.Common.ISelectionInfo"]:
        """
        Gets or sets the Location.
        """
        return None

    @property
    def TimeForMinimumOfMinimumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the minimum of minimum values.
        """
        return None

    @property
    def TimeForMinimumOfMaximumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the minimum of maximum values.
        """
        return None

    @property
    def LoadStepForMinimumOfMinimumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the minimum of minimum values.
        """
        return None

    @property
    def LoadStepForMinimumOfMaximumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the minimum of maximum values.
        """
        return None

    @property
    def TimeForMaximumOfMinimumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the maximum of minimum values.
        """
        return None

    @property
    def TimeForMaximumOfMaximumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the maximum of maximum values.
        """
        return None

    @property
    def LoadStepForMaximumOfMinimumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the maximum of minimum values.
        """
        return None

    @property
    def LoadStepForMaximumOfMaximumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the maximum of maximum values.
        """
        return None

    @property
    def IsSolved(self) -> typing.Optional["System.Boolean"]:
        """
        Gets the IsSolved.
        """
        return None

    @property
    def CoordinateSystem(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.CoordinateSystem"]:
        """
        
            Gets or sets the Coordinate System. 
            Accepts/Returns None for Solution Coordinate System in the general case (if applicable). 
            Accepts/Returns None for Fiber Coordinate System for a result that is sub scoped by ply.
            
        """
        return None

    @property
    def ScopingMethod(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GeometryDefineByType"]:
        """
        Gets or sets the ScopingMethod.
        """
        return None

    @property
    def SetNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the Set Number.
        """
        return None

    @property
    def CombinationNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the Combination Number for a Solution Combination result.
        """
        return None

    @property
    def SolutionCombinationDriver(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.SolutionCombinationDriverStyle"]:
        """
        Gets or sets the SolutionCombinationDriver.
        """
        return None

    @property
    def Path(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.Path"]:
        """
        Path property.
        """
        return None

    @property
    def Surface(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.Surface"]:
        """
        Surface property.
        """
        return None

    @property
    def SurfaceCoating(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.SurfaceCoating"]:
        """
        SurfaceCoating property.
        """
        return None

    @property
    def NamedSelections(self) -> typing.Optional["System.Collections.Generic.IEnumerable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]"]:
        """
        Gets or sets the NamedSelections.
        """
        return None

    @property
    def WaterfallShowTextOnMosaic(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the Waterfall Mosaic Text Property.
        """
        return None

    @property
    def CrackFrontNumber(self) -> typing.Optional["System.Int32"]:
        """
        Gets or sets the CrackFrontNumber.
        """
        return None

    @property
    def GlobalIDs(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the GlobalIDs.
        """
        return None

    @property
    def Identifier(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the Identifier.
        """
        return None

    @property
    def IterationNumber(self) -> typing.Optional["System.Int32"]:
        """
        Gets the IterationNumber.
        """
        return None

    @property
    def LoadStep(self) -> typing.Optional["System.Int32"]:
        """
        Gets the LoadStep.
        """
        return None

    @property
    def MaximumOccursOn(self) -> typing.Optional["System.String"]:
        """
        Gets the MaximumOccursOn.
        """
        return None

    @property
    def MinimumOccursOn(self) -> typing.Optional["System.String"]:
        """
        Gets the MinimumOccursOn.
        """
        return None

    @property
    def LoadStepNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the LoadStepNumber.
        """
        return None

    @property
    def SolverComponentIDs(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the SolverComponentIDs.
        """
        return None

    @property
    def Substep(self) -> typing.Optional["System.Int32"]:
        """
        Gets the Substep.
        """
        return None

    @property
    def Average(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Average.
        """
        return None

    @property
    def Maximum(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Maximum.
        """
        return None

    @property
    def MaximumOfMaximumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MaximumOfMaximumOverTime.
        """
        return None

    @property
    def MaximumOfMinimumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MaximumOfMinimumOverTime.
        """
        return None

    @property
    def Minimum(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Minimum.
        """
        return None

    @property
    def MinimumOfMaximumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MinimumOfMaximumOverTime.
        """
        return None

    @property
    def MinimumOfMinimumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MinimumOfMinimumOverTime.
        """
        return None

    @property
    def Time(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Time.
        """
        return None

    @property
    def DisplayTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets or sets the DisplayTime.
        """
        return None

    @property
    def GraphControlsXAxis(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GraphControlsXAxis"]:
        """
        Gets or sets the GraphControlsXAxis.
        """
        return None

    @property
    def DisplayOption(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.ResultAveragingType"]:
        """
        Gets or sets the DisplayOption.
        """
        return None

    @property
    def DpfEvaluation(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.DpfEvaluationType"]:
        """
        Gets or sets the DpfEvaluation.
        """
        return None

    @property
    def By(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.SetDriverStyle"]:
        """
        Gets or sets the By.
        """
        return None

    @property
    def ItemType(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.ResultFileItemType"]:
        """
        Gets or sets the ItemType.
        """
        return None

    @property
    def CalculateTimeHistory(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the CalculateTimeHistory.
        """
        return None

    @property
    def Suppressed(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the Suppressed.
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

    def ClearGeneratedData(self) -> "System.Void":
        """
        Run the ClearGeneratedData action.
        """
        pass

    def EvaluateAllResults(self) -> "System.Void":
        """
        Run the EvaluateAllResults action.
        """
        pass

    def FetchRemoteResults(self) -> "System.Void":
        """
        Run the FetchRemoteResult action.
        """
        pass

    def ExportToTextFile(self, filePath: "System.String") -> "System.Void":
        """
        Run the ExportToTextFile action.
        """
        pass

    def ExportAnimation(self, filePath: "System.String", format: "Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat", settings: "Ansys.Mechanical.Graphics.AnimationExportSettings") -> "System.Void":
        """
        Run the ExportAnimation action.
        """
        pass

    def DuplicateWithoutResults(self) -> "Ansys.Mechanical.DataModel.Interfaces.IDataModelObject":
        """
        Run the DuplicateWithoutResults action.
        """
        pass

    def CreateResultsAtAllSets(self) -> "System.Collections.Generic.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]":
        """
        Creates results at all sets for results under a solution.
        """
        pass

    def PromoteToNamedSelection(self) -> "System.Collections.Generic.IEnumerable[Ansys.ACT.Automation.Mechanical.NamedSelection]":
        """
        Run the PromoteToNamedSelection action.
        """
        pass

    def CreateParameter(self, propName: "System.String") -> "Ansys.ACT.Interfaces.Mechanical.IParameter":
        """
        CreateParameter method.
        """
        pass

    def AddAlert(self) -> "Ansys.ACT.Automation.Mechanical.Results.Alert":
        """
        Creates a new Alert
        """
        pass

    def AddConvergence(self) -> "Ansys.ACT.Automation.Mechanical.Results.Convergence":
        """
        Creates a new Convergence
        """
        pass

    def RenameBasedOnDefinition(self) -> "System.Void":
        """
        Run the RenameBasedOnDefinition action.
        """
        pass

    def Delete(self) -> "System.Void":
        """
        Run the Delete action.
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


class MinimumBendingStress(object):
    """
    Defines a MinimumBendingStress.
    """

    @property
    def InternalObject(self) -> typing.Optional["Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto"]:
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
    def BeamToolStressResultType(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.BeamToolStressResultType"]:
        """
        Gets or sets the BeamToolStressResultType.
        """
        return None

    @property
    def PlotData(self) -> typing.Optional["Ansys.Mechanical.DataModel.Results.ResultDataTable"]:
        """
        Gets the result table.
        """
        return None

    @property
    def Location(self) -> typing.Optional["Ansys.ACT.Interfaces.Common.ISelectionInfo"]:
        """
        Gets or sets the Location.
        """
        return None

    @property
    def TimeForMinimumOfMinimumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the minimum of minimum values.
        """
        return None

    @property
    def TimeForMinimumOfMaximumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the minimum of maximum values.
        """
        return None

    @property
    def LoadStepForMinimumOfMinimumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the minimum of minimum values.
        """
        return None

    @property
    def LoadStepForMinimumOfMaximumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the minimum of maximum values.
        """
        return None

    @property
    def TimeForMaximumOfMinimumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the maximum of minimum values.
        """
        return None

    @property
    def TimeForMaximumOfMaximumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the maximum of maximum values.
        """
        return None

    @property
    def LoadStepForMaximumOfMinimumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the maximum of minimum values.
        """
        return None

    @property
    def LoadStepForMaximumOfMaximumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the maximum of maximum values.
        """
        return None

    @property
    def IsSolved(self) -> typing.Optional["System.Boolean"]:
        """
        Gets the IsSolved.
        """
        return None

    @property
    def CoordinateSystem(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.CoordinateSystem"]:
        """
        
            Gets or sets the Coordinate System. 
            Accepts/Returns None for Solution Coordinate System in the general case (if applicable). 
            Accepts/Returns None for Fiber Coordinate System for a result that is sub scoped by ply.
            
        """
        return None

    @property
    def ScopingMethod(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GeometryDefineByType"]:
        """
        Gets or sets the ScopingMethod.
        """
        return None

    @property
    def SetNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the Set Number.
        """
        return None

    @property
    def CombinationNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the Combination Number for a Solution Combination result.
        """
        return None

    @property
    def SolutionCombinationDriver(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.SolutionCombinationDriverStyle"]:
        """
        Gets or sets the SolutionCombinationDriver.
        """
        return None

    @property
    def Path(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.Path"]:
        """
        Path property.
        """
        return None

    @property
    def Surface(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.Surface"]:
        """
        Surface property.
        """
        return None

    @property
    def SurfaceCoating(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.SurfaceCoating"]:
        """
        SurfaceCoating property.
        """
        return None

    @property
    def NamedSelections(self) -> typing.Optional["System.Collections.Generic.IEnumerable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]"]:
        """
        Gets or sets the NamedSelections.
        """
        return None

    @property
    def WaterfallShowTextOnMosaic(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the Waterfall Mosaic Text Property.
        """
        return None

    @property
    def CrackFrontNumber(self) -> typing.Optional["System.Int32"]:
        """
        Gets or sets the CrackFrontNumber.
        """
        return None

    @property
    def GlobalIDs(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the GlobalIDs.
        """
        return None

    @property
    def Identifier(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the Identifier.
        """
        return None

    @property
    def IterationNumber(self) -> typing.Optional["System.Int32"]:
        """
        Gets the IterationNumber.
        """
        return None

    @property
    def LoadStep(self) -> typing.Optional["System.Int32"]:
        """
        Gets the LoadStep.
        """
        return None

    @property
    def MaximumOccursOn(self) -> typing.Optional["System.String"]:
        """
        Gets the MaximumOccursOn.
        """
        return None

    @property
    def MinimumOccursOn(self) -> typing.Optional["System.String"]:
        """
        Gets the MinimumOccursOn.
        """
        return None

    @property
    def LoadStepNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the LoadStepNumber.
        """
        return None

    @property
    def SolverComponentIDs(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the SolverComponentIDs.
        """
        return None

    @property
    def Substep(self) -> typing.Optional["System.Int32"]:
        """
        Gets the Substep.
        """
        return None

    @property
    def Average(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Average.
        """
        return None

    @property
    def Maximum(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Maximum.
        """
        return None

    @property
    def MaximumOfMaximumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MaximumOfMaximumOverTime.
        """
        return None

    @property
    def MaximumOfMinimumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MaximumOfMinimumOverTime.
        """
        return None

    @property
    def Minimum(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Minimum.
        """
        return None

    @property
    def MinimumOfMaximumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MinimumOfMaximumOverTime.
        """
        return None

    @property
    def MinimumOfMinimumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MinimumOfMinimumOverTime.
        """
        return None

    @property
    def Time(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Time.
        """
        return None

    @property
    def DisplayTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets or sets the DisplayTime.
        """
        return None

    @property
    def GraphControlsXAxis(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GraphControlsXAxis"]:
        """
        Gets or sets the GraphControlsXAxis.
        """
        return None

    @property
    def DisplayOption(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.ResultAveragingType"]:
        """
        Gets or sets the DisplayOption.
        """
        return None

    @property
    def DpfEvaluation(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.DpfEvaluationType"]:
        """
        Gets or sets the DpfEvaluation.
        """
        return None

    @property
    def By(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.SetDriverStyle"]:
        """
        Gets or sets the By.
        """
        return None

    @property
    def ItemType(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.ResultFileItemType"]:
        """
        Gets or sets the ItemType.
        """
        return None

    @property
    def CalculateTimeHistory(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the CalculateTimeHistory.
        """
        return None

    @property
    def Suppressed(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the Suppressed.
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

    def ClearGeneratedData(self) -> "System.Void":
        """
        Run the ClearGeneratedData action.
        """
        pass

    def EvaluateAllResults(self) -> "System.Void":
        """
        Run the EvaluateAllResults action.
        """
        pass

    def FetchRemoteResults(self) -> "System.Void":
        """
        Run the FetchRemoteResult action.
        """
        pass

    def ExportToTextFile(self, filePath: "System.String") -> "System.Void":
        """
        Run the ExportToTextFile action.
        """
        pass

    def ExportAnimation(self, filePath: "System.String", format: "Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat", settings: "Ansys.Mechanical.Graphics.AnimationExportSettings") -> "System.Void":
        """
        Run the ExportAnimation action.
        """
        pass

    def DuplicateWithoutResults(self) -> "Ansys.Mechanical.DataModel.Interfaces.IDataModelObject":
        """
        Run the DuplicateWithoutResults action.
        """
        pass

    def CreateResultsAtAllSets(self) -> "System.Collections.Generic.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]":
        """
        Creates results at all sets for results under a solution.
        """
        pass

    def PromoteToNamedSelection(self) -> "System.Collections.Generic.IEnumerable[Ansys.ACT.Automation.Mechanical.NamedSelection]":
        """
        Run the PromoteToNamedSelection action.
        """
        pass

    def CreateParameter(self, propName: "System.String") -> "Ansys.ACT.Interfaces.Mechanical.IParameter":
        """
        CreateParameter method.
        """
        pass

    def AddAlert(self) -> "Ansys.ACT.Automation.Mechanical.Results.Alert":
        """
        Creates a new Alert
        """
        pass

    def AddConvergence(self) -> "Ansys.ACT.Automation.Mechanical.Results.Convergence":
        """
        Creates a new Convergence
        """
        pass

    def RenameBasedOnDefinition(self) -> "System.Void":
        """
        Run the RenameBasedOnDefinition action.
        """
        pass

    def Delete(self) -> "System.Void":
        """
        Run the Delete action.
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


class MinimumCombinedStress(object):
    """
    Defines a MinimumCombinedStress.
    """

    @property
    def InternalObject(self) -> typing.Optional["Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto"]:
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
    def BeamToolStressResultType(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.BeamToolStressResultType"]:
        """
        Gets or sets the BeamToolStressResultType.
        """
        return None

    @property
    def PlotData(self) -> typing.Optional["Ansys.Mechanical.DataModel.Results.ResultDataTable"]:
        """
        Gets the result table.
        """
        return None

    @property
    def Location(self) -> typing.Optional["Ansys.ACT.Interfaces.Common.ISelectionInfo"]:
        """
        Gets or sets the Location.
        """
        return None

    @property
    def TimeForMinimumOfMinimumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the minimum of minimum values.
        """
        return None

    @property
    def TimeForMinimumOfMaximumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the minimum of maximum values.
        """
        return None

    @property
    def LoadStepForMinimumOfMinimumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the minimum of minimum values.
        """
        return None

    @property
    def LoadStepForMinimumOfMaximumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the minimum of maximum values.
        """
        return None

    @property
    def TimeForMaximumOfMinimumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the maximum of minimum values.
        """
        return None

    @property
    def TimeForMaximumOfMaximumValues(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Get the Time for the maximum of maximum values.
        """
        return None

    @property
    def LoadStepForMaximumOfMinimumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the maximum of minimum values.
        """
        return None

    @property
    def LoadStepForMaximumOfMaximumValues(self) -> typing.Optional["System.UInt32"]:
        """
        Get the Load Step for the maximum of maximum values.
        """
        return None

    @property
    def IsSolved(self) -> typing.Optional["System.Boolean"]:
        """
        Gets the IsSolved.
        """
        return None

    @property
    def CoordinateSystem(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.CoordinateSystem"]:
        """
        
            Gets or sets the Coordinate System. 
            Accepts/Returns None for Solution Coordinate System in the general case (if applicable). 
            Accepts/Returns None for Fiber Coordinate System for a result that is sub scoped by ply.
            
        """
        return None

    @property
    def ScopingMethod(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GeometryDefineByType"]:
        """
        Gets or sets the ScopingMethod.
        """
        return None

    @property
    def SetNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the Set Number.
        """
        return None

    @property
    def CombinationNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the Combination Number for a Solution Combination result.
        """
        return None

    @property
    def SolutionCombinationDriver(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.SolutionCombinationDriverStyle"]:
        """
        Gets or sets the SolutionCombinationDriver.
        """
        return None

    @property
    def Path(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.Path"]:
        """
        Path property.
        """
        return None

    @property
    def Surface(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.Surface"]:
        """
        Surface property.
        """
        return None

    @property
    def SurfaceCoating(self) -> typing.Optional["Ansys.ACT.Automation.Mechanical.SurfaceCoating"]:
        """
        SurfaceCoating property.
        """
        return None

    @property
    def NamedSelections(self) -> typing.Optional["System.Collections.Generic.IEnumerable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]"]:
        """
        Gets or sets the NamedSelections.
        """
        return None

    @property
    def WaterfallShowTextOnMosaic(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the Waterfall Mosaic Text Property.
        """
        return None

    @property
    def CrackFrontNumber(self) -> typing.Optional["System.Int32"]:
        """
        Gets or sets the CrackFrontNumber.
        """
        return None

    @property
    def GlobalIDs(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the GlobalIDs.
        """
        return None

    @property
    def Identifier(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the Identifier.
        """
        return None

    @property
    def IterationNumber(self) -> typing.Optional["System.Int32"]:
        """
        Gets the IterationNumber.
        """
        return None

    @property
    def LoadStep(self) -> typing.Optional["System.Int32"]:
        """
        Gets the LoadStep.
        """
        return None

    @property
    def MaximumOccursOn(self) -> typing.Optional["System.String"]:
        """
        Gets the MaximumOccursOn.
        """
        return None

    @property
    def MinimumOccursOn(self) -> typing.Optional["System.String"]:
        """
        Gets the MinimumOccursOn.
        """
        return None

    @property
    def LoadStepNumber(self) -> typing.Optional["System.UInt32"]:
        """
        Gets or sets the LoadStepNumber.
        """
        return None

    @property
    def SolverComponentIDs(self) -> typing.Optional["System.String"]:
        """
        Gets or sets the SolverComponentIDs.
        """
        return None

    @property
    def Substep(self) -> typing.Optional["System.Int32"]:
        """
        Gets the Substep.
        """
        return None

    @property
    def Average(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Average.
        """
        return None

    @property
    def Maximum(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Maximum.
        """
        return None

    @property
    def MaximumOfMaximumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MaximumOfMaximumOverTime.
        """
        return None

    @property
    def MaximumOfMinimumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MaximumOfMinimumOverTime.
        """
        return None

    @property
    def Minimum(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Minimum.
        """
        return None

    @property
    def MinimumOfMaximumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MinimumOfMaximumOverTime.
        """
        return None

    @property
    def MinimumOfMinimumOverTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the MinimumOfMinimumOverTime.
        """
        return None

    @property
    def Time(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets the Time.
        """
        return None

    @property
    def DisplayTime(self) -> typing.Optional["Ansys.Core.Units.Quantity"]:
        """
        Gets or sets the DisplayTime.
        """
        return None

    @property
    def GraphControlsXAxis(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GraphControlsXAxis"]:
        """
        Gets or sets the GraphControlsXAxis.
        """
        return None

    @property
    def DisplayOption(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.ResultAveragingType"]:
        """
        Gets or sets the DisplayOption.
        """
        return None

    @property
    def DpfEvaluation(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.DpfEvaluationType"]:
        """
        Gets or sets the DpfEvaluation.
        """
        return None

    @property
    def By(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.SetDriverStyle"]:
        """
        Gets or sets the By.
        """
        return None

    @property
    def ItemType(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.ResultFileItemType"]:
        """
        Gets or sets the ItemType.
        """
        return None

    @property
    def CalculateTimeHistory(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the CalculateTimeHistory.
        """
        return None

    @property
    def Suppressed(self) -> typing.Optional["System.Boolean"]:
        """
        Gets or sets the Suppressed.
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

    def ClearGeneratedData(self) -> "System.Void":
        """
        Run the ClearGeneratedData action.
        """
        pass

    def EvaluateAllResults(self) -> "System.Void":
        """
        Run the EvaluateAllResults action.
        """
        pass

    def FetchRemoteResults(self) -> "System.Void":
        """
        Run the FetchRemoteResult action.
        """
        pass

    def ExportToTextFile(self, filePath: "System.String") -> "System.Void":
        """
        Run the ExportToTextFile action.
        """
        pass

    def ExportAnimation(self, filePath: "System.String", format: "Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat", settings: "Ansys.Mechanical.Graphics.AnimationExportSettings") -> "System.Void":
        """
        Run the ExportAnimation action.
        """
        pass

    def DuplicateWithoutResults(self) -> "Ansys.Mechanical.DataModel.Interfaces.IDataModelObject":
        """
        Run the DuplicateWithoutResults action.
        """
        pass

    def CreateResultsAtAllSets(self) -> "System.Collections.Generic.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]":
        """
        Creates results at all sets for results under a solution.
        """
        pass

    def PromoteToNamedSelection(self) -> "System.Collections.Generic.IEnumerable[Ansys.ACT.Automation.Mechanical.NamedSelection]":
        """
        Run the PromoteToNamedSelection action.
        """
        pass

    def CreateParameter(self, propName: "System.String") -> "Ansys.ACT.Interfaces.Mechanical.IParameter":
        """
        CreateParameter method.
        """
        pass

    def AddAlert(self) -> "Ansys.ACT.Automation.Mechanical.Results.Alert":
        """
        Creates a new Alert
        """
        pass

    def AddConvergence(self) -> "Ansys.ACT.Automation.Mechanical.Results.Convergence":
        """
        Creates a new Convergence
        """
        pass

    def RenameBasedOnDefinition(self) -> "System.Void":
        """
        Run the RenameBasedOnDefinition action.
        """
        pass

    def Delete(self) -> "System.Void":
        """
        Run the Delete action.
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


