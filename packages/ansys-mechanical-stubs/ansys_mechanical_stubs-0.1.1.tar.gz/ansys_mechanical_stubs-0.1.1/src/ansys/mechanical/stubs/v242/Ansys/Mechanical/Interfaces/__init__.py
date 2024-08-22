"""Interfaces subpackage."""
import typing

class IDataSeries(object):
    """
    IDataSeries interface.
    """

    @property
    def DataType(self) -> typing.Optional["System.Type"]:
        return None

    @property
    def Name(self) -> typing.Optional["System.String"]:
        """
        
            Gets or sets the name of the data series.
            
        """
        return None

    @property
    def QuantityName(self) -> typing.Optional["System.String"]:
        """
        
            Gets or sets the quantity name of the data series, e.g., “Length”, “Pressure”, or “Heat Flux”.
            
        """
        return None

    @property
    def Unit(self) -> typing.Optional["System.String"]:
        """
        
            Gets or sets a string representation of the data series units, e.g., “m”,
            “kg m^-1 s^-2”, or “kg m^2 s^-3”.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional["System.Collections.ICollection"]:
        """
        
            Explicitly gets or sets the values of the data series.
            
        """
        return None


class IDataTable(object):
    """
    IDataTable interface.
    """

    @property
    def ColumnNames(self) -> typing.Optional["System.Collections.Generic.IReadOnlyList[System.String]"]:
        return None

    @property
    def Columns(self) -> typing.Optional["System.Collections.Generic.IList[Ansys.Mechanical.Interfaces.IDataSeries]"]:
        """
        
            Explicitly get the columns of the data table.
            
        """
        return None

    @property
    def Count(self) -> typing.Optional["System.Int32"]:
        """
        
            Gets the number of columns in the table.
            
        """
        return None

    @property
    def IsFixedColumnCount(self) -> typing.Optional["System.Boolean"]:
        """
        
            Get whether additional columns can be added or removed from the contained T:Ansys.Mechanical.Interfaces.IDataSeries.
            
        """
        return None

    @property
    def IsFixedRowCount(self) -> typing.Optional["System.Boolean"]:
        """
        
            Get whether additional rows can be added or removed from the contained
            T:Ansys.Mechanical.Interfaces.IDataSeries.
            
        """
        return None

    @property
    def IsReadOnly(self) -> typing.Optional["System.Boolean"]:
        """
        
            Gets whether the data table is read-only.
            
        """
        return None

    @property
    def Item(self) -> typing.Optional["Ansys.Mechanical.Interfaces.IDataSeries"]:
        """
        Item property.
        """
        return None

    @property
    def Metadata(self) -> typing.Optional["System.Collections.Generic.IDictionary[System.String,System.Object]"]:
        """
        
            Gets or set a dictionary with additional information that may be useful to understanding
            the context of data in the table.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional["System.String"]:
        """
        
            Get or set the name of the table.
            
        """
        return None

    @property
    def RowCount(self) -> typing.Optional["System.Int32"]:
        return None

    def Add(self, dataSeries: "Ansys.Mechanical.Interfaces.IDataSeries") -> "System.Void":
        """
        
            Add a new column to the data table.
            
        """
        pass

    def Clear(self) -> "System.Void":
        """
        
            Drops all columns from the data table.
            
        """
        pass

    def Contains(self, name: "System.String") -> "System.Boolean":
        """
        
            Returns whether the data table contains a column with the specified name.
            
        """
        pass

    def GetRow(self, rowIndex: "System.Int32") -> "System.Collections.IEnumerable":
        pass

    def Insert(self, columnIndex: "System.Int32", dataSeries: "Ansys.Mechanical.Interfaces.IDataSeries") -> "System.Void":
        """
        
            Insert a column at the specified index.
            
        """
        pass

    def Remove(self, key: "System.Object") -> "System.Void":
        """
        
            Removes the specified column. If the specifier of the column to remove is an T:System.Int32, it will
            be interpreted as an index. If the specifier of the column to remove is a T:System.String, it will
            be interpreted as a column name.
            
        """
        pass

    def TryInsertRow(self, rowIndex: "System.Int32", values: "System.Collections.IEnumerable") -> "System.Boolean":
        """
        
            Try to insert the values at the specified row index.
            
        """
        pass

    def TryRemoveRow(self, rowIndex: "System.Int32") -> "System.Boolean":
        """
        
            Try to remove the specified row.
            
        """
        pass


class IReadOnlyDataSeries(object):
    """
    IReadOnlyDataSeries interface.
    """

    @property
    def Item(self) -> typing.Optional["System.Object"]:
        """
        Item property.
        """
        return None

    @property
    def Count(self) -> typing.Optional["System.Int32"]:
        """
        
            Gets the number of data points.
            
        """
        return None

    @property
    def DataType(self) -> typing.Optional["System.Type"]:
        """
        
            Gets the type stored by the data series.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional["System.String"]:
        """
        
            Gets the name of the data series.
            
        """
        return None

    @property
    def QuantityName(self) -> typing.Optional["System.String"]:
        """
        
            Gets the quantity name of the data series, e.g., “Length”, “Pressure”, or “Heat Flux”.
            
        """
        return None

    @property
    def Unit(self) -> typing.Optional["System.String"]:
        """
        
            Gets the string representation of the data series units, e.g., “m”, “kg m^-1 s^-2”,
            or “kg m^2 s^-3”.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional["System.Collections.ICollection"]:
        """
        
            Explicitly get the values of the data series.
            
        """
        return None


class IReadOnlyDataTable(object):
    """
    IReadOnlyDataTable interface.
    """

    @property
    def ColumnNames(self) -> typing.Optional["System.Collections.Generic.IReadOnlyList[System.String]"]:
        """
        
            Gets a list of the column names.
            
        """
        return None

    @property
    def Columns(self) -> typing.Optional["System.Collections.Generic.IReadOnlyList[Ansys.Mechanical.Interfaces.IReadOnlyDataSeries]"]:
        """
        
            Explicitly get the columns of the table.
            
        """
        return None

    @property
    def Item(self) -> typing.Optional["Ansys.Mechanical.Interfaces.IReadOnlyDataSeries"]:
        """
        Item property.
        """
        return None

    @property
    def Metadata(self) -> typing.Optional["System.Collections.Generic.IReadOnlyDictionary[System.String,System.Object]"]:
        """
        
            Gets a dictionary with additional information that may be useful to understanding the
            context of data in the table.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional["System.String"]:
        """
        
            Get the name of the table.
            
        """
        return None

    @property
    def RowCount(self) -> typing.Optional["System.Int32"]:
        """
        
            Gets the maximum number of data points (rows) among all columns in the table
            
        """
        return None

    def GetRow(self, rowIndex: "System.Int32") -> "System.Collections.IEnumerable":
        """
        
            Returns an enumerable to iterate over the values in a row.
            
        """
        pass


class ITable(object):
    """
    
            Exposes a table, which is a two-dimensional tabular data structure with labeled columns.
            The columns are usually instances of IVariable but can be any sort of array
            
    """

    @property
    def Independents(self) -> typing.Optional["System.Collections.Generic.IReadOnlyDictionary[System.String,System.Collections.IEnumerable]"]:
        """
        The portion of the table corresponding to independent variables.
        """
        return None

    @property
    def Dependents(self) -> typing.Optional["System.Collections.Generic.IReadOnlyDictionary[System.String,System.Collections.IEnumerable]"]:
        """
        The portion of the table corresponding to dependent variables.
        """
        return None


class IVariable(object):
    """
    Exposes a variable, which is a one dimensional array of real numbers with a unit.
    """

    @property
    def Unit(self) -> typing.Optional["System.String"]:
        """
        The unit of the variable.  For example, this could be "mm".
        """
        return None

    @property
    def QuantityName(self) -> typing.Optional["System.String"]:
        """
        The quantity name of the variable.  For example, this could be "Length".
        """
        return None


