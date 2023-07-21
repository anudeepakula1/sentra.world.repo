import pandas as pd
import flask
import xlrd
from abc import ABC, abstractmethod

class IFuelEmissions(ABC):
    @abstractmethod
    def GetFuels():
        pass

    @abstractmethod
    def GetUnitsForFuel(fuelName):
        pass

    @abstractmethod
    def GetEmissionsForFieldByAFU(fuelActivity,fuelName,unitName,conversionCol):
        pass

    def read_merged_cells_to_dataframe(self,file_path, sheet_name, start_row, end_row, start_col, end_col):
        # Open the .xls file
        workbook = xlrd.open_workbook(file_path)

        try:
            # Get the sheet by name
            sheet = workbook.sheet_by_name(sheet_name)
        except xlrd.XLRDError:
            print(f"Sheet with name '{sheet_name}' not found in the workbook.")
            return

        # Ensure the cell range is within the sheet's boundaries
        if (
            start_row < 0 or end_row >= sheet.nrows
            or start_col < 0 or end_col >= sheet.ncols
            or start_row > end_row or start_col > end_col
        ):
            print("Invalid cell range provided.")
            return

        # Read data from the specified cell range and store in a list
        data = []
        columns = []
        for row_idx in range(start_row, end_row + 1):
            row_data = []
            for col_idx in range(start_col, end_col + 1):
                cell_value = sheet.cell_value(row_idx, col_idx)
                if row_idx == start_row:
                    columns.append(cell_value)  # Save first row as column headers
                else:
                    if sheet.merged_cells and (row_idx, col_idx) in sheet.merged_cells:
                        top_left_row, top_left_col, _, _ = sheet.merged_cells[(row_idx, col_idx)]
                        cell_value = sheet.cell_value(top_left_row, top_left_col, formatted=False)
                    row_data.append(cell_value)
            if row_data:
                data.append(row_data)

        # Create a Pandas DataFrame from the data list and set the column headers
        df = pd.DataFrame(data, columns=columns)
        return df

    def preprocess(self,df : pd.DataFrame,colName):
        rowLength = len(df)
        dfMapped = list()
        prev = df[colName][0]
        dfMapped.append(prev)
        for i in range(1,rowLength):
            if(df[colName][i] == ""):
                dfMapped.append(prev)
            else:
                dfMapped.append(df[colName][i])
                prev = df[colName][i]
        return dfMapped
    
    

class GaseousFuel(IFuelEmissions):
    def __init__(self,fileLocation):
        df = self.read_merged_cells_to_dataframe(fileLocation,'Fuels',21,53,1,7)
        print(df)
        dfMappedListFuel = self.preprocess(df,'Fuel')
        dfMappedListActivity = self.preprocess(df,'Activity')
        df['Fuel'] = dfMappedListFuel
        df['Activity'] = dfMappedListActivity
        self.df = df
        self.MeasureColumns = self.df.columns[3:7]   


    def GetFuels(self):
        res =  self.df['Fuel'].unique() 
        return res
    
    def GetUnitsForFuel(self,fuelName):
        return self.df[self.df['Fuel'].isin([fuelName])]['Unit'].values
    
    def GetEmissionsForFieldByAFU(self,fuelName, unitName, conversionCol):
        return self.df[self.df['Fuel'].isin([fuelName]) & self.df['Unit'].isin([unitName])][conversionCol].sum()


class LiquidFuel(IFuelEmissions):
    def __init__(self,fileLocation):
        df = self.read_merged_cells_to_dataframe(fileLocation,'Fuels',57,125,1,7)
        dfMappedListFuel = self.preprocess(df,'Fuel')
        dfMappedListActivity = self.preprocess(df,'Activity')
        df['Fuel'] = dfMappedListFuel
        df['Activity'] = dfMappedListActivity
        self.df = df
        self.MeasureColumns = self.df.columns[3:7]
    
    def GetFuels(self):
        return self.df['Fuel'].unique()
    
    def GetUnitsForFuel(self,fuelName):
        return self.df[self.df['Fuel'].isin([fuelName])]['Unit'].values
    
    def GetEmissionsForFieldByAFU(self,fuelName, unitName, conversionCol):
        return self.df[self.df['Fuel'].isin([fuelName]) & self.df['Unit'].isin([unitName])][conversionCol].sum()


class SolidFuel(IFuelEmissions):
    def __init__(self,fileLocation):
        df = self.read_merged_cells_to_dataframe(fileLocation,'Fuels',129,147,1,7)
        dfMappedListFuel = self.preprocess(df,'Fuel')
        dfMappedListActivity = self.preprocess(df,'Activity')
        df['Fuel'] = dfMappedListFuel
        df['Activity'] = dfMappedListActivity
        self.df = df
        self.MeasureColumns = self.df.columns[3:7]
    
    def GetFuels(self):
        return self.df['Fuel'] 
    
    def GetUnitsForFuel(self,fuelName):
        return self.df[self.df['Fuel'].isin([fuelName])]['Unit'].values
    
    def GetEmissionsForFieldByAFU(self,fuelName, unitName, conversionCol):
        return self.df[self.df['Fuel'].isin([fuelName]) & self.df['Unit'].isin([unitName])][conversionCol].sum()

