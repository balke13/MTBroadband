#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      KBalke
#
# Created:     06/09/2013
# Copyright:   (c) KBalke 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Import arcpy module
import arcpy, os, sys, datetime

################################################################################
# Use SearchCursor with list comprehension to return a
#  unique set of values in the specified field
#
def parseFC (featureclass, field):
    fcName = os.path.basename(featureclass).rstrip(os.path.splitext(featureclass)[1]).partition("_") [2]
    values = [row[0] for row in arcpy.da.SearchCursor(featureclass, (field))]
    uniqueValues = set(values)
    uniqueValues2 = list (uniqueValues)

    x = 0
    for value in uniqueValues2:

        #Create the query
        query = field + " = '" + uniqueValues2[x] + "'"

        #Execute the Select tool
        arcpy.Select_analysis (featureclass, OutFGDB + fcName + "_" + uniqueValues2[x], query )
        x = x + 1

################################################################################

# Script arguments
curFCNTIABlks = arcpy.GetParameterAsText(0)
if curFCNTIABlks == '#' or not curFCNTIABlks:
    curFCNTIABlks = "Z:\\Broadband\\BBMT\\NTIA_Deliverables\\Submission_20130930\\MT_SBDD_2013_09_30.gdb\\NATL_Broadband_Map\\BB_Service_CensusBlock" # provide a default value if unspecified

curFCNTIARds = arcpy.GetParameterAsText(1)
if curFCNTIARds == '#' or not curFCNTIARds:
    curFCNTIARds = "Z:\\Broadband\\BBMT\\NTIA_Deliverables\\Submission_20130930\\MT_SBDD_2013_09_30.gdb\\NATL_Broadband_Map\\BB_Service_RoadSegment" # provide a default value if unspecified

curFCNTIAWireless = arcpy.GetParameterAsText(2)
if curFCNTIAWireless == '#' or not curFCNTIAWireless:
    curFCNTIAWireless = "Z:\\Broadband\\BBMT\\NTIA_Deliverables\\Submission_20130930\\MT_SBDD_2013_09_30.gdb\\NATL_Broadband_Map\\BB_Service_Wireless" # provide a default value if unspecified

now = datetime.datetime.now()

# Local variables:
JoinTable = "Z:\\Broadband\\BBMT\\Provider_Update\\mt_provider_table.csv"
PathFGDB = "Z:\\Broadband\\BBMT\\NTIA_Deliverables\\Review\\"
NameFGDB = "ParsedNTIAData_" + now.strftime("%Y%m%d") + ".gdb"
OutFGDB = PathFGDB + NameFGDB + "\\"
fcNTIABlks = OutFGDB + "fc_ntia_blks"
fcNTIARds = OutFGDB + "fc_ntia_rds"
fcNTIAWireless = OutFGDB + "fc_ntia_wireless"
fieldName = "PKEY"

# Create a new output file geodatabase
arcpy.CreateFileGDB_management (PathFGDB, NameFGDB)

# Process: Feature Class to Feature Class
arcpy.Copy_management(curFCNTIABlks, fcNTIABlks,"")
arcpy.Copy_management(curFCNTIARds, fcNTIARds,"")
arcpy.Copy_management(curFCNTIAWireless, fcNTIAWireless,"")

# Create a copy of the input Provider Table
arcpy.TableToTable_conversion (JoinTable, OutFGDB, "tbl_mt_provider")

arcpy.env.workspace = OutFGDB
listFC = arcpy.ListFeatureClasses ("fc_ntia_*", "", "")
for fc in listFC:
    # Add the PKEY Field from the Provider Table
    arcpy.JoinField_management (fc, "PROVNAME", "tbl_mt_provider", "PROVNAME", ["PKEY"])
    parseFC (fc, fieldName)


