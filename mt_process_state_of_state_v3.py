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
import arcpy, os, datetime

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
        arcpy.Select_analysis (featureclass, outShp + fcName + "_" + uniqueValues2[x], query )
        x = x + 1

################################################################################

# Script arguments
inWebCur = "Z:\\Broadband\\BBMT\\Website_Data\\Submission_20130930\\MT_Web_Data_20130930.gdb\\Web_ProviderAndTechnology"

now = datetime.datetime.now()
outLoc = "Z:\\Broadband\\BBND\\Operational_Data\\Reports\\BB_State_of_the_State\\" + now.strftime("%Y_%m_%d")
if not os.path.exists(outLoc): os.makedirs(outLoc)
outShp = "Z:\\Broadband\\BBND\\Operational_Data\\Reports\\BB_State_of_the_State\\" + now.strftime("%Y_%m_%d") + "\\Shapefiles\\"
if not os.path.exists(outShp): os.makedirs(outShp)

# Local variables:
JoinTable = "Z:\\Broadband\\BBMT\\Provider_Update\\mt_provider_table.csv"
fcWebCur1 = "temp_web_prov_tot_dice.shp"
fcWebCur2 = "fc_web_prov_tot.shp"
tblFinal = "tbl_mt_state_of_state"
fieldName = "PKEY"

# Process: Feature Class to Feature Class
arcpy.env.workspace = outLoc
arcpy.Dice_management(inWebCur, fcWebCur1, "10000")

arcpy.Dissolve_management (fcWebCur1, fcWebCur2, ["PROVNAME", "TRANSTECH", "SPECTRUM"], "", "MULTI_PART")

arcpy.TableToTable_conversion (JoinTable, outLoc, "temp_tbl_mt_provider")

arcpy.JoinField_management (fcWebCur2, "PROVNAME", "temp_tbl_mt_provider", "PROVNAME", ["PKEY"])

arcpy.Statistics_analysis (fcWebCur2, tblFinal,[["PROVNAME", "FIRST"]] ,["PROVNAME", "TRANSTECH", "SPECTRUM", "PKEY"] )

arcpy.AddField_management (tblFinal, "PkeyTotSpec", "TEXT", "", "", 100)

arcpy.CalculateField_management (tblFinal, "PkeyTotSpec", "!PROVNAME! + \"_\" + str(!TRANSTECH!) +\"_\" + str(!SPECTRUM!)", "PYTHON")
parseFC (fcWebCur2, fieldName)