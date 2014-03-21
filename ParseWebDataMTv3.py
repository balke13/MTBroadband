#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      KBalke
#
# Created:     10/12/2012
# Copyright:   (c) KBalke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Import arcpy module
import arcpy, os, sys, string, datetime

now = datetime.datetime.now()

# Local variables:
InWebProvTot = arcpy.GetParameterAsText(0)
InFileName = os.path.basename(InWebProvTot).rstrip(os.path.splitext(InWebProvTot)[1])
PathFGDB = "C:\\Data\\Broadband\\BBMT\\"
NameFGDB = "ParsedWebData_" + now.strftime("%Y%m%d") + ".gdb"
OutFGDB = PathFGDB + NameFGDB + "\\"
fieldName = "PKEYTOT"
JoinTable = "Z:\\Broadband\\BBMT\\Provider_Update\\mt_provider_table.csv"
LayerName = "tempFeatureLayer"

# Create a new output file geodatabase
arcpy.CreateFileGDB_management (PathFGDB, NameFGDB)

# Create a copy of the input FeatureClass
arcpy.Copy_management(InWebProvTot, OutFGDB + InFileName,"")

# Create a copy of the input Provider Table
arcpy.TableToTable_conversion (JoinTable, OutFGDB, "tbl_mt_provider")

# Add a new ProvTot field
arcpy.env.workspace = OutFGDB
arcpy.JoinField_management (OutFGDB + InFileName, "PROVNAME", "tbl_mt_provider", "PROVNAME", ["PKEY"])

# Add a new PKEYTot field
arcpy.AddField_management (OutFGDB + InFileName, "PKEYTOT", "TEXT", "", "", 15, "", "", "", "")

# Caluculate the ProvTot Field
arcpy.CalculateField_management (OutFGDB + InFileName, "PKEYTOT", "!PKEY! + \"_\" + str(!TRANSTECH!)", "PYTHON")

###Set a list variable to hold the unique values from TOTMaxAddDownTemp
##list = []
##
###Open a search cursor on the OutputProject feature class and loop through all the unique values in the TOTMaxAddDownTemp field
##rows = arcpy.SearchCursor (OutFGDB + InFileName)
##row = rows.next()
##
###Use a while loop to cursor through all the records and append unique values to the list variable
##while row:
##    value = row.getValue (fieldName)
##    if value not in list:
##        list.append (value)
##    row = rows.next()
##
###Sort the list variable
##list.sort()
##
###If a value in the list variable is blank, remove it from the list variable
##if ' ' in list:
##    list.remove (' ')
##
###Loop through the list variable
##x = 0
##for item in list:
##
##    #Create the query
##    query = fieldName + " = '" + list[x] + "'"
##
##    #Execute the Select tool
##    arcpy.Select_analysis (OutFGDB + InFileName, OutFGDB + list[x], query )
##    x = x + 1

values = [row[0] for row in arcpy.da.SearchCursor(OutFGDB + InFileName, (fieldName))]
uniqueValues = set(values)
uniqueValues2 = list (uniqueValues)

x = 0
for value in uniqueValues2:

    #Create the query
    query = fieldName + " = '" + uniqueValues2[x] + "'"

    #Execute the Select tool
    arcpy.Select_analysis (OutFGDB + InFileName, OutFGDB + InFileName + "_" + uniqueValues2[x], query )
    x = x + 1
