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

################################################################################
def createMaxSpeed (featureclass):
    fcName = os.path.basename(featureclass).rstrip(os.path.splitext(featureclass)[1]).partition("_") [2]

    arcpy.AddField_management (featureclass, "Down", "SHORT")
    arcpy.CalculateField_management (featureclass, "Down", "!MAXADDOWN!", "PYTHON")
    arcpy.Union_analysis (featureclass, "temp_union_" + fcName, "ALL")
    arcpy.Sort_management ("temp_union_" + fcName, "temp_union_sort" + fcName, [["Down", "DESCENDING"]])
    arcpy.AddField_management ("temp_union_sort" + fcName, "XCOORD", "DOUBLE")
    arcpy.AddField_management ("temp_union_sort" + fcName, "YCOORD", "DOUBLE")
    arcpy.CalculateField_management ("temp_union_sort" + fcName, "XCOORD", "!SHAPE.CENTROID!.split()[0]", "PYTHON")
    arcpy.CalculateField_management ("temp_union_sort" + fcName, "YCOORD", "!SHAPE.CENTROID!.split()[1]", "PYTHON")
    arcpy.Dissolve_management ("temp_union_sort" + fcName, "temp_union_sort_dz" + fcName, ["XCOORD", "YCOORD", "SHAPE_Area"], "Down FIRST", "MULTI_PART", "")
    arcpy.Dissolve_management ("temp_union_sort_dz" + fcName, "fc_mt_final_" + fcName + "_max_speed", ["Down"], "", "MULTI_PART", "")

################################################################################

# Local variables:
InWebProvTot = arcpy.GetParameterAsText(0)
InFileName = os.path.basename(InWebProvTot).rstrip(os.path.splitext(InWebProvTot)[1])
PathFGDB = "Z:\\Broadband\\BBMT\\Operational_Data\\Comptetition\\"
NameFGDB = "MT_Competition_" + now.strftime("%Y%m%d") + ".gdb"
OutFGDB = PathFGDB + NameFGDB + "\\"
fieldName = "PKEY"
JoinTable = "Z:\\Broadband\\BBMT\\Provider_Update\\mt_provider_table.csv"
fcCopy = "temp_mt_web_provider_technology"
fcWeb = "web_all"
fcWired = "web_wired"

# Create a new output file geodatabase
arcpy.CreateFileGDB_management (PathFGDB, NameFGDB)
arcpy.env.workspace = OutFGDB

# Create a copy of the input FeatureClass
arcpy.Copy_management(InWebProvTot, fcCopy,"")

# Create a new PKEY field and calculate from Master Provider Table
arcpy.TableToTable_conversion (JoinTable, OutFGDB, "temp_tbl_nd_provider")
arcpy.JoinField_management (fcCopy, "PROVNAME", "temp_tbl_nd_provider", "PROVNAME", ["PKEY"])

# Select only the Wired Provider Coverages
arcpy.MakeFeatureLayer_management (fcCopy, fcWeb)
arcpy.Select_analysis (fcWeb, fcWired, "\"TRANSTECH\" <=71")

createMaxSpeed (fcWeb)
createMaxSpeed (fcWired)

### Dissolve the Wired Provider Coverages by PKEY
##arcpy.Dissolve_management (OutFGDB + "temp_wired", OutFGDB + "temp_wired_dz", ["PKEY"], "", "MULTI_PART", "")
##
### Add a new Value field and Calculate with a Value of 1
##arcpy.AddField_management (OutFGDB + "temp_wired_dz", "VALUE", "SHORT", "", "", "", "", "", "", "")
##arcpy.CalculateField_management (OutFGDB + "temp_wired_dz", "VALUE", "1", "PYTHON")
##
##
### Self Union of the Wired Providers Feature Class
##arcpy.Union_analysis (OutFGDB + "temp_wired_dz", OutFGDB + "temp_wired_01_union", "ALL", "", "")
##
### Add and Calculate the X and Y Coordinate (centroid) for each feature
##arcpy.AddField_management (OutFGDB + "temp_wired_01_union", "XCOORD", "DOUBLE")
##arcpy.AddField_management (OutFGDB + "temp_wired_01_union", "YCOORD", "DOUBLE")
##arcpy.CalculateField_management (OutFGDB + "temp_wired_01_union", "XCOORD", "!SHAPE.CENTROID!.split()[0]", "PYTHON")
##arcpy.CalculateField_management (OutFGDB + "temp_wired_01_union", "YCOORD", "!SHAPE.CENTROID!.split()[1]", "PYTHON")
##
### Dissolve the Wired Providers Feature Class on the XCoord, YCoord, and Area then Sum the Value Field
##arcpy.Dissolve_management (OutFGDB + "temp_wired_01_union", OutFGDB + "fc_mt_final_wired_competition_all", ["XCOORD", "YCOORD", "Shape_Area"], "VALUE SUM", "MULTI_PART", "")
##
### Select the areas of Competition (Sum_Value >=2) and No Competition (Sum_Value <2)
##arcpy.Select_analysis (OutFGDB + "fc_mt_final_wired_competition_all", OutFGDB + "fc_mt_final_wired_competition_" + now.strftime("%Y%m%d"), "\"SUM_VALUE\" >= 2" )
##arcpy.Select_analysis (OutFGDB + "fc_mt_final_wired_competition_all", OutFGDB + "fc_mt_final_wired_no_competition_" + now.strftime("%Y%m%d"), "\"SUM_VALUE\" < 2" )
##
##
### Delete the temporary tables
##tblTemp = arcpy.ListFeatureClasses("temp*", "")
##for tblTempDel in tblTemp:
##    arcpy.Delete_management (tblTempDel, "")