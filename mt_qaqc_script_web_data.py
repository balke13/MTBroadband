#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      KBalke
#
# Created:     04/10/2013
# Copyright:   (c) KBalke 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Import system modules
import arcpy, os, sys, string
arcpy.env.overwriteOutput = True

################################################################################
def createSumTbl (table):
    # Calculate the Attribute Fields for the Cloned DCN Data
    arcpy.Statistics_analysis(table, table + "_area_v1", [["Shape_Area", "SUM", ]], "SUMAREA")
    arcpy.Statistics_analysis(table, table + "_provtot_v1", [["SUMPROV", "FIRST", ]], "SUMPROV")
    arcpy.AddField_management (table + "_area_v1", "VERSION", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management (table + "_area_v1", "AREADBL", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(table + "_area_v1", "AREADBL", "round(!SUM_Shape_Area!/1000000, 0)", "PYTHON", "")
    arcpy.CalculateField_management (table + "_area_v1", "SUMAREA", calcSumFldArea, "PYTHON", "")
    arcpy.AddField_management (table + "_provtot_v1", "VERSION", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
    if tblName == "tbl_temp_web_prov_tot_cur":
        arcpy.TableToTable_conversion (table + "_area_v1", outFolder, tblFinalSum )
        arcpy.CalculateField_management (table + "_area_v1", "VERSION", "'" + "CURRENT" + "'", "PYTHON")
        arcpy.CalculateField_management (table + "_provtot_v1", "VERSION", "'" + "CURRENT" + "'", "PYTHON")

    elif tblName == "tbl_temp_web_prov_tot_prev":
        arcpy.CalculateField_management (table + "_area_v1", "VERSION", "'" + "PREVIOUS" + "'", "PYTHON")
        arcpy.CalculateField_management (table + "_provtot_v1", "VERSION", "'" + "PREVIOUS" + "'", "PYTHON")
################################################################################

# Script arguments
inWebCur = arcpy.GetParameterAsText(0)
inWebPrev = arcpy.GetParameterAsText(1)
outGDB = arcpy.GetParameterAsText(2)
outFolder = arcpy.GetParameterAsText (3)

# Local variables:
tblWebCur = "tbl_temp_web_prov_tot_cur"
tblWebPrev = "tbl_temp_web_prov_tot_prev"
calcFldProvTotSpd = "!PROVNAME! + \"_\" + !FRN! + \"_\" + str(!TRANSTECH!) + \"_\" + str(!SPECTRUM!) + \"_\" + !MAXADDOWN! + \"_\" + !MAXADUP!"
calcSumFldArea = "!SUMAREA! + \"_\" + str(!AREADBL!)"
calcSumFldProv = "!PROVNAME! + \"_\" + !FRN! + \"_\" + str(!TRANSTECH!) + \"_\" + str(!SPECTRUM!)"
whereClause = '"FREQUENCY" = 1'

tblFinalSum = "tbl_final_WEB_current_summary.dbf"
tblTempArea1 = outGDB + os.path.sep + "tbl_temp_web_prov_tot_area_merge"
tblTempArea2 = outGDB + os.path.sep + "tbl_temp_web_prov_tot_area_merge_summary"
tblTempArea3 = outGDB + os.path.sep + "tbl_temp_web_prov_tot_area_merge_summary_sort"
tblTempArea4 = outGDB + os.path.sep + "tbl_temp_web_prov_tot_area_merge_summary_sort_view"
tblFinalChgArea = outFolder + os.path.sep + "tbl_final_WEB_change_detection_prov_tot_speed_area.dbf"
tempTblProv1 = outGDB + os.path.sep + "tbl_temp_web_prov_tot_merge"
tempTblProv2 = outGDB + os.path.sep + "tbl_temp_web_prov_tot_merge_summary"
tempTblProv3 = outGDB + os.path.sep + "tbl_temp_web_prov_tot_merge_summary_view"
tblFinalChgProvTot = outFolder + os.path.sep + "tbl_final_WEB_change_detection_prov_tot.dbf"

#Create a Table of the current and previous Web_ProviderAndTechnology Layers
arcpy.TableToTable_conversion (inWebCur, outGDB, tblWebCur)
arcpy.TableToTable_conversion (inWebPrev, outGDB, tblWebPrev)

arcpy.env.workspace = outGDB
tblWebList = arcpy.ListTables ("tbl_temp_web_prov_tot_*", "")
for tbl in tblWebList:
    desc = arcpy.Describe(tbl)
    tblName = desc.name
    arcpy.AddField_management (tbl, "SUMAREA", "TEXT", "", "", "200", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management (tbl, "SUMAREA", calcFldProvTotSpd, "PYTHON", "")
    arcpy.AddField_management (tbl, "SUMPROV", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management (tbl, "SUMPROV", calcSumFldProv, "PYTHON", "")
    createSumTbl (tbl)

#Create the final web change detection table by Provider TOT Speed Area
arcpy.Merge_management (["tbl_temp_web_prov_tot_cur_area_v1", "tbl_temp_web_prov_tot_prev_area_v1"], tblTempArea1)
arcpy.Statistics_analysis(tblTempArea1, tblTempArea2, [["VERSION", "FIRST"]], "SUMAREA")
arcpy.AddField_management (tblTempArea2, "Sort", "TEXT", "", "", "200", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management (tblTempArea2, "SORT", "!SUMAREA!.rpartition(\"_\")[0] + \"_\" + !FIRST_VERSION!", "PYTHON", "")
arcpy.Sort_management (tblTempArea2, tblTempArea3, [["SORT", "ASCENDING"]])
arcpy.MakeTableView_management (tblTempArea3, tblTempArea4, whereClause, "", "")
arcpy.CopyRows_management(tblTempArea4, tblFinalChgArea)

#Create the final web change detection table by Provider TOT
arcpy.Merge_management (["tbl_temp_web_prov_tot_cur_provtot_v1", "tbl_temp_web_prov_tot_prev_provtot_v1"], tempTblProv1)
arcpy.Statistics_analysis(tempTblProv1, tempTblProv2, [["VERSION", "FIRST"]], "SUMPROV")
arcpy.MakeTableView_management (tempTblProv2, tempTblProv3, whereClause, "", "")
arcpy.CopyRows_management(tempTblProv3, tblFinalChgProvTot)

# Delete the temporary tables
tblTemp = arcpy.ListTables("tbl_temp*", "")
for tblTempDel in tblTemp:
    arcpy.Delete_management (tblTempDel, "")

fcTemp = arcpy.ListFeatureClasses ("fc_temp*", "")
for fcTempDel in fcTemp:
    arcpy.Delete_management (fcTempDel, "")