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
PathFGDB = "Z:\\Broadband\\BBMT\\Operational_Data\\Comptetition\\"
NameFGDB = "MTCompetition_Wireless" + now.strftime("%Y%m%d") + ".gdb"
OutFGDB = PathFGDB + NameFGDB + "\\"
fieldName = "PKEY"
JoinTable = "Z:\\Broadband\\BBMT\\Provider_Update\\mt_provider_table.csv"
LayerName = "tempFeatureLayer"

# Create a new output file geodatabase
arcpy.CreateFileGDB_management (PathFGDB, NameFGDB)
arcpy.env.workspace = OutFGDB

# Create a copy of the input FeatureClass
arcpy.Copy_management(InWebProvTot, OutFGDB + InFileName,"")

# Create a new PKEY field and calculate from Master Provider Table
arcpy.TableToTable_conversion (JoinTable, OutFGDB, "temp_tbl_mt_provider")
arcpy.JoinField_management (OutFGDB + InFileName, "PROVNAME", "temp_tbl_mt_provider", "PROVNAME", ["PKEY"])

# Select only the Wired Provider Coverages
arcpy.MakeFeatureLayer_management (OutFGDB + InFileName, LayerName)
arcpy.Select_analysis (LayerName, OutFGDB + InFileName + "_wireless", "\"TRANSTECH\" = 80")

# Dissolve the Wired Provider Coverages by PKEY
arcpy.Dissolve_management (OutFGDB + InFileName + "_wireless", OutFGDB + InFileName + "_wireless_dz", ["PKEY"], "", "MULTI_PART", "")

# Add a new Value field and Calculate with a Value of 1
arcpy.AddField_management (OutFGDB + InFileName + "_wireless_dz", "VALUE", "SHORT", "", "", "", "", "", "", "")
arcpy.CalculateField_management (OutFGDB + InFileName + "_wireless_dz", "VALUE", "1", "PYTHON")


# Self Union of the Wired Providers Feature Class
arcpy.Union_analysis (OutFGDB + InFileName + "_wireless_dz", OutFGDB + InFileName + "_wireless_01_union", "ALL", "", "")

# Add and Calculate the X and Y Coordinate (centroid) for each feature
arcpy.AddField_management (OutFGDB + InFileName +"_wireless_01_union", "XCOORD", "DOUBLE")
arcpy.AddField_management (OutFGDB + InFileName +"_wireless_01_union", "YCOORD", "DOUBLE")
arcpy.CalculateField_management (OutFGDB + InFileName + "_wireless_01_union", "XCOORD", "!SHAPE.CENTROID!.split()[0]", "PYTHON")
arcpy.CalculateField_management (OutFGDB + InFileName + "_wireless_01_union", "YCOORD", "!SHAPE.CENTROID!.split()[1]", "PYTHON")

# Dissolve the Wired Providers Feature Class on the XCoord, YCoord, and Area then Sum the Value Field
arcpy.Dissolve_management (OutFGDB + InFileName + "_wireless_01_union", OutFGDB + InFileName + "_wireless_02_dissolve", ["XCOORD", "YCOORD", "Shape_Area"], "VALUE SUM", "MULTI_PART", "")

# Select the areas of Competition (Sum_Value >=2) and No Competition (Sum_Value <2)
arcpy.Select_analysis (OutFGDB + InFileName + "_wireless_02_dissolve", OutFGDB + "fc_mt_final_wireless_competition_" + now.strftime("%Y%m%d"), "\"SUM_VALUE\" >= 2" )
arcpy.Select_analysis (OutFGDB + InFileName + "_wireless_02_dissolve", OutFGDB + "fc_mt_final_wireless_no_competition_" + now.strftime("%Y%m%d"), "\"SUM_VALUE\" < 2" )

arcpy.Clip_analysis (OutFGDB + InFileName + "_wired_dz", OutFGDB + "fc_mt_final_wireless_no_competition_" + now.strftime("%Y%m%d"), OutFGDB + "fc_mt_final_wireless_no_competition_prov" + now.strftime("%Y%m%d"))