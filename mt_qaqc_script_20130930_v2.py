#-------------------------------------------------------------------------------
# Name:        nd_qaqc_script
# Purpose:
#
# Author:      KBalke
#
# Created:     05/07/2012
# Copyright:   (c) KBalke 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Import system modules
import arcpy, os, sys, string

# Script arguments
inNTIACur = arcpy.GetParameterAsText(0)

inNTIAPrev = arcpy.GetParameterAsText(1)

outGDB = arcpy.GetParameterAsText(2)


# Local variables:

calcSumFldFreq = "[PROVNAME] & \"_\" & [DBANAME] & \"_\" & [FRN] & \"_\" & [TRANSTECH] & \"_\" & [SPECTRUM] & \"_\" & [MAXADDOWN] & \"_\" & [MAXADUP] & \"_\" & [FREQUENCY]"
calcSumFldProv = "[PROVNAME] & \"_\" & [DBANAME] & \"_\" & [FRN] & \"_\" & [TRANSTECH] & \"_\" & [SPECTRUM] & \"_\" & [FREQUENCY]"
tblMergCur = outGDB + "\\tbl_temp_merge_cur_wired_wireless"
tblMergPrev = outGDB + "\\tbl_temp_merge_prev_wired_wireless"
tblSumMergCur1 = outGDB + "\\tbl_temp_sum_merge_cur_wired_wireless_freq"
tblSumMergCur2 = outGDB + "\\tbl_temp_sum_merge_cur_wired_wireless_prov"
tblSumMergPrev1 = outGDB + "\\tbl_temp_sum_merge_prev_wired_wireless_freq"
tblSumMergPrev2 = outGDB + "\\tbl_temp_sum_merge_prev_wired_wireless_prov"
tblMergCurPrev1 = outGDB + "\\tbl_temp_merge_cur_prev_wired_wireless_freq"
tblMergCurPrev2 = outGDB + "\\tbl_temp_merge_cur_prev_wired_wireless_prov"
tblSumMergCurPrev1 = outGDB + "\\tbl_temp_sum_merge_cur_prev_wired_wireless_freq"
tblSumMergCurPrev2 = outGDB + "\\tbl_temp_sum_merge_cur_prev_wired_wireless_prov"
tblChgNTIAFeat = outGDB + "\\tbl_final_NTIA_change_detection_feat_cnt"
tblChgNTIAFeatProv = outGDB + "\\tbl_final_NTIA_change_detection_provider_tot"
tblSumProvTot = outGDB + "\\tbl_final_NTIA_summary_provider_transtech"
tblView1 = outGDB + "\\tbl_temp_merge_cur_prev_wired_wireless_freq_view"
tblView2 = outGDB + "\\tbl_temp_merge_cur_prev_wired_wireless_prov_view"
tblChkGeoFinal = outGDB + "\\tbl_final_NTIA_chk_geo"
tblTempIden = outGDB + "\\tbl_temp_findIdentical"
tblTempIdenSum = outGDB + "\\tbl_temp_findIdentical_sum"
statFields = [["PROVNAME", "FIRST"]]
caseFldFreq = ["PROVNAME", "DBANAME", "FRN", "TRANSTECH", "SPECTRUM", "MAXADDOWN", "MAXADUP", "FILENAME", "VERSION", "SUMFREQ" ]
caseFldProv = ["PROVNAME", "DBANAME", "FRN", "TRANSTECH", "SPECTRUM", "FILENAME", "VERSION", "SUMPROV" ]
whereClause = '"FREQUENCY" = 1'

### List the Feature Classes in the Current NTIA Deliverable and create tempoarary tables in the QAQC file geodatabase
arcpy.env.workspace = inNTIACur
fcListCur = arcpy.ListFeatureClasses ("","", "NATL_Broadband_Map")
for f in fcListCur:
    desc = arcpy.Describe(f)
    fcName = desc.name
##    if fcName == "BB_Service_CensusBlock":
##        arcpy.FindIdentical_management (f, tblTempIden + f, ["PROVNAME", "FULLFIPSID", "TRANSTECH"])
##        arcpy.Statistics_analysis (tblTempIden + f, tblTempIdenSum + f, "IN_FID FIRST;IN_FID LAST", "FEAT_SEQ")
##        arcpy.TableSelect_analysis(tblTempIdenSum + f, outGDB + "tbl_final_NTIA_duplicates_census_block", "\"FREQUENCY\" >= 2")
##    elif fcName == "BB_Service_RoadSegment":
##        arcpy.FindIdentical_management (f, tblTempIden + f, ["Shape", "PROVNAME", "TRANSTECH"])
##        arcpy.Statistics_analysis (tblTempIden + f, tblTempIdenSum + f, "IN_FID FIRST;IN_FID LAST", "FEAT_SEQ")
##        arcpy.TableSelect_analysis(tblTempIdenSum + f, outGDB + "tbl_final_NTIA_duplicates_roadseg", "\"FREQUENCY\" >= 2")
##    elif fcName == "BB_Service_Wireless":
##        arcpy.FindIdentical_management (f, tblTempIden + f, ["Shape", "PROVNAME", "TRANSTECH","SPECTRUM"] )
##        arcpy.Statistics_analysis (tblTempIden + f , tblTempIdenSum + f, "IN_FID FIRST;IN_FID LAST", "FEAT_SEQ")
##        arcpy.TableSelect_analysis(tblTempIdenSum + f, outGDB + "tbl_final_NTIA_duplicates_wireless", "\"FREQUENCY\" >= 2")
##    elif fcName == "BB_Service_CAInstitutions":
##        arcpy.FindIdentical_management (f, tblTempIden + f, ["ANCHORNAME", "LATITUDE", "LONGITUDE"] )
##        arcpy.Statistics_analysis (tblTempIden + f , tblTempIdenSum + f, "IN_FID FIRST;IN_FID LAST", "FEAT_SEQ")
##        arcpy.TableSelect_analysis(tblTempIdenSum + f, outGDB + "tbl_final_NTIA_duplicates_cai", "\"FREQUENCY\" >= 2")
##    elif fcName == "BB_ConnectionPoint_MiddleMile":
##        arcpy.FindIdentical_management (f, tblTempIden + f, ["PROVNAME", "LATITUDE", "LONGITUDE"] )
##        arcpy.Statistics_analysis (tblTempIden + f , tblTempIdenSum + f, "IN_FID FIRST;IN_FID LAST", "FEAT_SEQ")
##        arcpy.TableSelect_analysis(tblTempIdenSum + f, outGDB + "tbl_final_NTIA_duplicates_middle_mile", "\"FREQUENCY\" >= 2")
##
    arcpy.MakeTableView_management (f, "temp_current_" + f,"","","")
    arcpy.CopyRows_management ("temp_current_" + f, outGDB + "\\tbl_view_current_" + f)
##    arcpy.CheckGeometry_management (f, outGDB + "tbl_temp_chk_geo" + f)

# List the Feature Classes in the Previous NTIA Deliverable and create tempoarary tables in the QAQC file geodatabase
arcpy.env.workspace = inNTIAPrev
fcListPrev = arcpy.ListFeatureClasses ("","", "NATL_Broadband_Map")
for fc in fcListPrev:
    arcpy.MakeTableView_management (fc, "temp_previous_" + fc,"","","")
    arcpy.CopyRows_management ("temp_previous_" + fc, outGDB + "\\tbl_view_previous_" + fc)

# Set the Environment Workspace to the QAQC File Geodatabase
arcpy.env.workspace = outGDB

### Merge the check geometry tables into a single file
##tblListChkGeo = arcpy.ListTables("tbl_temp_chk_geo*", "")
##for tblChkGeo in tblListChkGeo:
##    tblNameChkGeo = tblChkGeo.split("tbl_temp_chk_geo_").pop()
##    arcpy.AddField_management (tblChkGeo, "FILENAME", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
##    arcpy.CalculateField_management (tblChkGeo, "FILENAME", "'" + tblNameChkGeo + "'", "PYTHON")
##mergChkGeo = arcpy.Merge_management(tblListChkGeo, tblChkGeoFinal)

# List the tables from the CURRENT NTIA deliverable in the QAQC File Geodatabase then add and caluclate the summary, filename, and version fields
tblListCur = arcpy.ListTables ("tbl_view_current*", "")
for tbl in tblListCur:
    tblName = tbl.split("tbl_view_current_").pop()
    arcpy.AddField_management (tbl, "SUMFREQ", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management (tbl, "SUMPROV", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management (tbl, "FILENAME", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management (tbl, "VERSION", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management (tbl, "FILENAME", "'" + tblName + "'", "PYTHON")
    arcpy.CalculateField_management (tbl, "VERSION", "'" + "CURRENT" + "'", "PYTHON")

# List the tables from the PREVIOUS NTIA deliverable in the QAQC File Geodatabase then add and caluclate the summary, filename, and version fields
tblListPrev = arcpy.ListTables ("tbl_view_previous*", "")
for tblPrev in tblListPrev:
    tblNamePrev = tblPrev.split("tbl_view_previous_").pop()
    arcpy.AddField_management (tblPrev, "SUMFREQ", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management (tblPrev, "SUMPROV", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management (tblPrev, "FILENAME", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management (tblPrev, "VERSION", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management (tblPrev, "FILENAME", "'" + tblNamePrev + "'", "PYTHON")
    arcpy.CalculateField_management (tblPrev, "VERSION", "'" + "PREVIOUS" + "'", "PYTHON")

# Add the census block, road segment, and wireless tables to a list
tblServiceCur = ["tbl_view_current_BB_Service_CensusBlock", "tbl_view_current_BB_Service_RoadSegment", "tbl_view_current_BB_Service_Wireless"]
tblServicePrev = ["tbl_view_previous_BB_Service_CensusBlock", "tbl_view_previous_BB_Service_RoadSegment", "tbl_view_previous_BB_Service_Wireless"]

# Merge the wired and wireless tables, run summary statistics, and calculate the summary field for the CURRENT NTIA deliverable
arcpy.Merge_management (tblServiceCur, tblMergCur, "")
arcpy.Statistics_analysis (tblMergCur, tblSumMergCur1, statFields, caseFldFreq)
arcpy.Statistics_analysis (tblMergCur, tblSumMergCur2, statFields, caseFldProv)
arcpy.CalculateField_management (tblSumMergCur1, "SUMFREQ", calcSumFldFreq)
arcpy.CalculateField_management (tblSumMergCur2, "SUMPROV", calcSumFldProv)

# Merge the wired and wireless tables, run summary statistics, and calculate the summary field for the PREVIOUS NTIA deliverable
arcpy.Merge_management (tblServicePrev, tblMergPrev, "")
arcpy.Statistics_analysis (tblMergPrev, tblSumMergPrev1, statFields, caseFldFreq)
arcpy.Statistics_analysis (tblMergPrev, tblSumMergPrev2, statFields, caseFldProv)
arcpy.CalculateField_management (tblSumMergPrev1, "SUMFREQ", calcSumFldFreq)
arcpy.CalculateField_management (tblSumMergPrev2, "SUMPROV", calcSumFldProv)

# Merge the current and previous summary tables for feature count, run summary statistics
arcpy.Merge_management ([tblSumMergCur1, tblSumMergPrev1], tblMergCurPrev1)
arcpy.Statistics_analysis(tblMergCurPrev1, tblSumMergCurPrev1, [["VERSION", "FIRST"], ["FILENAME", "FIRST"]], ["SUMFREQ"])
arcpy.MakeTableView_management (tblSumMergCurPrev1, tblView1, whereClause, "", "")
arcpy.CopyRows_management(tblView1, tblChgNTIAFeat)

# Merge the current and previous summary tables for Provider Tot, run summary statistics
arcpy.Merge_management ([tblSumMergCur2, tblSumMergPrev2], tblMergCurPrev2)
arcpy.Statistics_analysis(tblMergCurPrev2, tblSumMergCurPrev2, [["VERSION", "FIRST"], ["FILENAME", "FIRST"]], ["SUMPROV"])
arcpy.MakeTableView_management (tblSumMergCurPrev2, tblView2, whereClause, "", "")
arcpy.CopyRows_management(tblView2, tblChgNTIAFeatProv)

# Run summary statistics for Provider Name and Technology of Transmission of the current dataset
arcpy.Statistics_analysis(tblMergCur, tblSumProvTot, statFields, ["PROVNAME", "DBANAME", "FRN", "TRANSTECH", "SPECTRUM"])

# Delete the temporary tables
tblTemp = arcpy.ListTables("tbl_temp*", "")
for tblTempDel in tblTemp:
    arcpy.Delete_management (tblTempDel, "")

tblView = arcpy.ListTables ("tbl_view*", "")
for tblViewDel in tblView:
    arcpy.Delete_management (tblViewDel, "")