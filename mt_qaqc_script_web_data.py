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

# Script arguments
inWebCur = arcpy.GetParameterAsText(0)
if inWebCur == '#' or not curProvTbl:
    inWebCur = "Z:\\Broadband\\BBMT\\Website_Data\\Submission_20130930\\MT_Web_Data_20130930.gdb\\" # provide a default value if unspecified

inWebPrev = arcpy.GetParameterAsText(1)
if inWebPrev == '#' or not curProvTbl:
    inWebPrev = "Z:\\Broadband\\BBMT\\Website_Data\\Submission_20130930\\MT_Web_Data_20130930.gdb\\" # provide a default value if unspecified

outGDB = arcpy.GetParameterAsText(2)
if outGDB == '#' or not curProvTbl:
    outGDB = "Z:\\Broadband\\BBMT\\Provider_Update\\201309\\MT_QAQC_20130930.gdb\\" # provide a default value if unspecified

# Local variables:
calcFldProvTotSpd = "!PROVNAME! + \"_\" + !FRN! + \"_\" + str(!TRANSTECH!) + \"_\" + str(!SPECTRUM!) + \"_\" + !MAXADDOWN! + \"_\" + !MAXADUP!"
calcSumFldArea = "!SUMAREA! + \"_\" + str(!AREADBL!)"
calcSumFldProv = "!PROVNAME! + \"_\" + !FRN! + \"_\" + str(!TRANSTECH!) + \"_\" + str(!SPECTRUM!)"
whereClause = '"FREQUENCY" = 1'

inWebProvTotCur = inWebCur + "Web_ProviderAndTechnology"
inWebProvTotPrev = inWebPrev + "Web_ProviderAndTechnology"

tblWebCurSum = "tbl_final_WEB_current_summary"

tblWebCurPrevAreaMrg = outGDB + "tbl_temp_web_prov_tot_area_merge"
tblWebCurPrevSumArea = outGDB + "tbl_temp_web_prov_tot_area_merge_summary"
tblView1 = outGDB + "tbl_temp_web_prov_tot_area_merge_summary_view"
tblChgWebArea = outGDB + "tbl_final_WEB_change_detection_prov_tot_speed_area"

tblWebCurPrevProvTotMrg = outGDB + "tbl_temp_web_prov_tot_merge"
tblWebCurPrevSumProvTot = outGDB + "tbl_temp_web_prov_tot_merge_summary"
tblView2 = outGDB + "tbl_temp_web_prov_tot_merge_summary_view"
tblChgWebProvTot = outGDB + "tbl_final_WEB_change_detection_prov_tot"

#Create a Table of the current and previous Web_ProviderAndTechnology Layers
arcpy.TableToTable_conversion (inWebProvTotCur, outGDB, "tbl_temp_web_prov_tot_cur")
arcpy.TableToTable_conversion (inWebProvTotPrev, outGDB, "tbl_temp_web_prov_tot_prev")

arcpy.env.workspace = outGDB
tblWebList = arcpy.ListTables ("tbl_temp_web_prov_tot_*", "")
for tbl in tblWebList:
    desc = arcpy.Describe(tbl)
    tblName = desc.name
    arcpy.AddField_management (tbl, "SUMAREA", "TEXT", "", "", "200", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management (tbl, "SUMAREA", calcFldProvTotSpd, "PYTHON", "")
    arcpy.AddField_management (tbl, "SUMPROV", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management (tbl, "SUMPROV", calcSumFldProv, "PYTHON", "")
    if tblName == "tbl_temp_web_prov_tot_cur":
        arcpy.Statistics_analysis(tbl, tbl + "_area_v1", [["Shape_Area", "SUM", ]], "SUMAREA")
        arcpy.TableToTable_conversion (tbl + "_area_v1", outGDB, tblWebCurSum )
        arcpy.Statistics_analysis(tbl, tbl + "_provtot_v1", [["SUMPROV", "FIRST", ]], "SUMPROV")
        arcpy.AddField_management (tbl + "_area_v1", "VERSION", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management (tbl + "_area_v1", "VERSION", "'" + "CURRENT" + "'", "PYTHON")
        arcpy.AddField_management (tbl + "_area_v1", "AREADBL", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(tbl + "_area_v1", "AREADBL", "round(!SUM_Shape_Area!/1000000, 0)", "PYTHON", "")
        arcpy.CalculateField_management (tbl + "_area_v1", "SUMAREA", calcSumFldArea, "PYTHON", "")
        arcpy.AddField_management (tbl + "_provtot_v1", "VERSION", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management (tbl + "_provtot_v1", "VERSION", "'" + "CURRENT" + "'", "PYTHON")

    elif tblName == "tbl_temp_web_prov_tot_prev":
        arcpy.Statistics_analysis(tbl, tbl + "_area_v1", [["Shape_Area", "SUM", ]], "SUMAREA")
        arcpy.Statistics_analysis(tbl, tbl + "_provtot_v1", [["SUMPROV", "FIRST", ]], "SUMPROV")
        arcpy.AddField_management (tbl + "_area_v1", "VERSION", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management (tbl + "_area_v1", "VERSION", "'" + "PREVIOUS" + "'", "PYTHON")
        arcpy.AddField_management (tbl + "_area_v1", "AREADBL", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(tbl + "_area_v1", "AREADBL", "round(!SUM_Shape_Area!/1000000, 0)", "PYTHON", "")
        arcpy.CalculateField_management (tbl + "_area_v1", "SUMAREA", calcSumFldArea, "PYTHON", "")
        arcpy.AddField_management (tbl + "_provtot_v1", "VERSION", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management (tbl + "_provtot_v1", "VERSION", "'" + "PREVIOUS" + "'", "PYTHON")

#Create the final web change detection table by Provider TOT Speed Area
arcpy.Merge_management (["tbl_temp_web_prov_tot_cur_area_v1", "tbl_temp_web_prov_tot_prev_area_v1"], tblWebCurPrevAreaMrg)
arcpy.Statistics_analysis(tblWebCurPrevAreaMrg, tblWebCurPrevSumArea, [["VERSION", "FIRST"]], "SUMAREA")
arcpy.MakeTableView_management (tblWebCurPrevSumArea, tblView1, whereClause, "", "")
arcpy.CopyRows_management(tblView1, tblChgWebArea)

#Create the final web change detection table by Provider TOT
arcpy.Merge_management (["tbl_temp_web_prov_tot_cur_provtot_v1", "tbl_temp_web_prov_tot_prev_provtot_v1"], tblWebCurPrevProvTotMrg)
arcpy.Statistics_analysis(tblWebCurPrevProvTotMrg, tblWebCurPrevSumProvTot, [["VERSION", "FIRST"]], "SUMPROV")
arcpy.MakeTableView_management (tblWebCurPrevSumProvTot, tblView2, whereClause, "", "")
arcpy.CopyRows_management(tblView2, tblChgWebProvTot)

# Delete the temporary tables
tblTemp = arcpy.ListTables("tbl_temp*", "")
for tblTempDel in tblTemp:
    arcpy.Delete_management (tblTempDel, "")

fcTemp = arcpy.ListFeatureClasses ("fc_temp*", "")
for fcTempDel in fcTemp:
    arcpy.Delete_management (fcTempDel, "")