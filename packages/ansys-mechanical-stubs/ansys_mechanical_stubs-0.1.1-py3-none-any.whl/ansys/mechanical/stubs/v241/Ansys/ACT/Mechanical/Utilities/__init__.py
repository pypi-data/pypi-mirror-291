"""Utilities subpackage."""
import typing

class GeometryImportPreferences(object):
    """
    
             
    """

    @property
    def ProcessSolids(self) -> typing.Optional["System.Boolean"]:
        """
        
            Import solid bodies.
            
        """
        return None

    @property
    def ProcessSurfaces(self) -> typing.Optional["System.Boolean"]:
        """
        
            Import surface bodies.
            
        """
        return None

    @property
    def ProcessLines(self) -> typing.Optional["System.Boolean"]:
        """
        
            Import lines bodies.
            
        """
        return None

    @property
    def ProcessAttributes(self) -> typing.Optional["System.Boolean"]:
        """
        
            Import CAD system attributes.
            
        """
        return None

    @property
    def AttributeKey(self) -> typing.Optional["System.String"]:
        """
        
            If `ProcessAttributes` is `true`, import only those attributes with this prefix.
            Multiple semicolon-delimited filters may be specified. An empty string matches
            everything.
            
        """
        return None

    @property
    def ProcessNamedSelections(self) -> typing.Optional["System.Boolean"]:
        """
        
            Import/create named selections.
            
        """
        return None

    @property
    def NamedSelectionKey(self) -> typing.Optional["System.String"]:
        """
        
            If `ProcessNamedSelections` is `true`, import only those named selections with this
            prefix. Multiple semicolon-delimited filters may be specified.
            
        """
        return None

    @property
    def ProcessMaterialProperties(self) -> typing.Optional["System.Boolean"]:
        """
        
            Import primary material data defined in the CAD source.
            
        """
        return None

    @property
    def AnalysisType(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.AnalysisType"]:
        """
        
            Specify the analysis type to target during import.
            
        """
        return None

    @property
    def CADAssociativity(self) -> typing.Optional["System.Boolean"]:
        """
        
            Allow associativity.
            
        """
        return None

    @property
    def ProcessCoordinateSystems(self) -> typing.Optional["System.Boolean"]:
        """
        
            Import coordinate systems defined in the CAD source.
            
        """
        return None

    @property
    def CoordinateSystemKey(self) -> typing.Optional["System.String"]:
        """
        
            If `ProcessCoordinateSystems` is `true`, import only those coordinate systems with this
            prefix. Multiple semicolon-delimited filters may be specified. An empty string matches
            everything.
            
        """
        return None

    @property
    def ProcessWorkPoints(self) -> typing.Optional["System.Boolean"]:
        """
        
            Import work points.
            
        """
        return None

    @property
    def ReaderSaveFile(self) -> typing.Optional["System.Boolean"]:
        """
        
            Save the part file of a model after the import.
            
        """
        return None

    @property
    def ProcessInstances(self) -> typing.Optional["System.Boolean"]:
        """
        
            Honor part instance specifications.
            
        """
        return None

    @property
    def DoSmartUpdate(self) -> typing.Optional["System.Boolean"]:
        """
        
            Speed up refreshes for models with unmodified components. Causes changes to other import
            preferences to be ignored during refresh.
            
        """
        return None

    @property
    def ComparePartsOnUpdate(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.ComparePartsOnUpdate"]:
        """
        
            Enable mesh preservation on refresh for unmodified entities.
            
        """
        return None

    @property
    def ComparePartsTolerance(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.ComparePartsTolerance"]:
        """
        
            Specifies the tolerance to use when comparing parts.
            
        """
        return None

    @property
    def EnclosureSymmetryProcessing(self) -> typing.Optional["System.Boolean"]:
        """
        
            Enable the processing of enclosure and symmetry named selections.
            
        """
        return None

    @property
    def DecomposeDisjointGeometry(self) -> typing.Optional["System.Boolean"]:
        """
        
            Enable the decomposition of disjoint geometries for the following associative geometry
            interfaces:
            bullet
            
        """
        return None

    @property
    def MixedImportResolution(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.MixedImportResolution"]:
        """
        
            Allows mixed-dimension parts to be imported as assembly components with parts of
            different dimensions.
            
        """
        return None

    @property
    def Clean(self) -> typing.Optional["System.Boolean"]:
        """
        
            Clean unwanted features when importing geometry.
            
        """
        return None

    @property
    def StitchType(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.StitchSurfacesOnImport"]:
        """
        
            Specifies how surfaces should be stitched together.
            
        """
        return None

    @property
    def StitchTolerance(self) -> typing.Optional["System.Double"]:
        """
        
            If `StitchType` is `User`, specifies the tolerance to use for stitching detection.
            
        """
        return None

    @property
    def FacetQuality(self) -> typing.Optional["Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.FacetQuality"]:
        """
        
            Specifies what facet quality should be used for the import. 
            The default value is Source meaning that the facets as represented in the CAD 
            system or use a Normal option for those that do not have display. 
            The others are relative settings compared to "normal" facet quality. 
            Typically, better facet quality requires more memory and may take additional time to import/update.
            
        """
        return None


