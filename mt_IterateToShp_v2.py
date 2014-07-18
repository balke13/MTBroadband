# ---------------------------------------------------------------------------
# IterateToShp.py
# Created on: 2012-04-24 10:40:13.00000
# Created by: Kyle Balke - Senior GIS Analyst
# Description: This script takes a provider's coverage feature class and prepares it for use on the Broadband Editing App.  The input feature class is re-project to WGS84 (required by the editing app),
#              calculates a temporary field (TOTMaxAddDownTemp field), and then loops through each unique TOTMaxAddDownTemp value which is exported to shapefile.  The final shapefiles are compress into individual zip files.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy, os, sys, string, zipfile, zlib
arcpy.env.overwriteOutput = True

# Local variables:
InputDataset = arcpy.GetParameterAsText(0)
DataPath = r"Z:\Broadband\BBMT\Provider_Update\201409"
fieldName = "TOTMaxAddDownTemp"
outCS = arcpy.SpatialReference(4326)

# Process: Get the InputDataset File Name
InputFileName = os.path.basename(InputDataset).rstrip(os.path.splitext(InputDataset)[1])
OutputProject = DataPath + "\\Scratch.gdb\\" + InputFileName + "_Project"
OutputShapefile = DataPath + os.path.sep + "Shapefiles" + os.path.sep
OutputZipFiles = DataPath + os.path.sep + "ZipFiles" + os.path.sep
OutputFCLocation = DataPath + "\\MTUpdate20140930.gdb\\Provider_Coverage\\"
OutTable = DataPath + "\\MTUpdate20140930.gdb\\" + "tbl_CheckGeo_" + InputFileName

# Create a copy of the input FeatureClass
arcpy.FeatureClassToFeatureClass_conversion(InputDataset, OutputFCLocation, InputFileName,"")

# Process: Project the Input Dataset to WGS84
arcpy.Project_management(InputDataset, OutputProject, outCS, "WGS_1984_(ITRF00)_To_NAD_1983")

#Check Geometry
arcpy.CheckGeometry_management(OutputProject, OutTable)

#Repair Geometry
arcpy.RepairGeometry_management (OutputProject)

values = [row[0] for row in arcpy.da.SearchCursor(OutputProject, (fieldName))]
uniqueValues = set(values)
uniqueValues2 = list (uniqueValues)

x = 0
for value in uniqueValues2:

    #Create the query
    query = fieldName + " = '" + uniqueValues2[x] + "'"

    #Execute the Select tool
    arcpy.Select_analysis (OutputProject, OutputShapefile + InputFileName + "_" + uniqueValues2[x], query )

    #Create a new zip file using the original input coverage feature class file name and the value from TOTMaxAddDownTemp field (i.e., 10_4) and write the contents of the shapefile to it
    zip = zipfile.ZipFile (OutputZipFiles + InputFileName + "_" + uniqueValues2[x] + ".zip", 'w', zlib.DEFLATED)
    zip.write (OutputShapefile + InputFileName + "_" + uniqueValues2[x] + ".dbf", InputFileName + "_" + uniqueValues2[x] + ".dbf")
    zip.write (OutputShapefile + InputFileName + "_" + uniqueValues2[x] + ".prj", InputFileName + "_" + uniqueValues2[x] + ".prj")
    zip.write (OutputShapefile + InputFileName + "_" + uniqueValues2[x] + ".sbn", InputFileName + "_" + uniqueValues2[x] + ".sbn")
    zip.write (OutputShapefile + InputFileName + "_" + uniqueValues2[x] + ".sbx", InputFileName + "_" + uniqueValues2[x] + ".sbx")
    zip.write (OutputShapefile + InputFileName + "_" + uniqueValues2[x] + ".shp", InputFileName + "_" + uniqueValues2[x] + ".shp")
    zip.write (OutputShapefile + InputFileName + "_" + uniqueValues2[x] + ".shp.xml",InputFileName + "_" + uniqueValues2[x] + ".shp.xml")
    zip.write (OutputShapefile + InputFileName + "_" + uniqueValues2[x] + ".shx", InputFileName + "_" + uniqueValues2[x] + ".shx")
    x = x + 1
