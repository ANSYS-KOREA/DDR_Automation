import os
import clr
import re
import time
import shutil
import traceback
import sub_ScriptEnv
import sub_AEDT
import sub_DB
import GUI_subforms

clr.AddReference('Microsoft.Office.Interop.Excel')

import System.Drawing
import System.Windows.Forms

from sub_functions import *
from System.Drawing import *
from System.Windows.Forms import *
from Microsoft.Office.Interop import Excel

def HighLight(key, TextBox):
	# Creat List from TextBox	
	temp_text = TextBox.Text.split("\n")

	# Initialize : Set all color black
	for i in range(0, len(temp_text)):
		TextBox.Select(TextBox.GetFirstCharIndexFromLine(i), len(temp_text[i]))
		if temp_text[i].find("#") != -1:		
			TextBox.SelectionColor = Color.Green
		else:
			TextBox.SelectionColor = Color.Black
		TextBox.SelectionFont = Font("Arial", 9)

	# Find the position(line number) = iter
	iter = 0
	for line in temp_text:
		if line.find(key[0]) != -1:
			del key[0]
			if key==[]:
				break
		iter += 1
	
	TextBox.Select(TextBox.GetFirstCharIndexFromLine(iter), len(temp_text[iter]))
	TextBox.Focus()
	TextBox.SelectionColor = Color.Blue
	TextBox.SelectionFont = Font("Arial", 10, FontStyle.Bold)

def Load_env(File):
	# Open *.cenv or *.uenv File
	temp_DB = {}	
	#level = 0
	with open(File) as fp:
		# Load Input File
		for line in fp:			
			# not blank and comment
			#temp_list = []
			if line.strip() != "" and line.lstrip()[0] != "#":
				# find parent node symbol : []				
				key = ""
				if line.find("[") != -1:
					str_parent = "[" + line.split("[")[1].split("]")[0] + "]"
					str_child = ""
					str_grandchild = ""
					# find data symbol : =
					temp_list = []
					if line.find("=") != -1:
						# back up the data
						line = line.strip().replace(" ","")
						key = str_parent
						for cell in list(filter(None, line.strip().split("=")[-1].split(","))):
							temp_list.append(cell)
				# find child node symbol : <>
				elif line.find("<") != -1:
					str_child = "<" + line.split("<")[1].split(">")[0] + ">"
					str_grandchild = ""
					# find data symbol : =
					temp_list = []
					if line.find("=") != -1:
						# back up the data
						line = line.strip().replace(" ","")
						key = str_child + str_parent
						for cell in list(filter(None, line.strip().split("=")[-1].split(","))):
							temp_list.append(cell)

				# find grandchild node symbol : ()
				elif line.find("(") != -1:
					str_grandchild = "(" + line.split("(")[1].split(")")[0] + ")"
					# find data symbol : =
					temp_list = []
					if line.find("=") != -1:
						# back up the data
						line = line.strip().replace(" ","")						
						key = str_grandchild + str_child + str_parent
						for cell in list(filter(None, line.strip().split("=")[-1].split(","))):						
							temp_list.append(cell)

				# find grandchild node symbol : ()				
				elif line.find("=") != -1:
					# back up the data
					#line = line.strip().replace(" ","")
					line = line.strip()
					key = str_grandchild + str_child + str_parent
					for cell in list(filter(None, line.strip().split("=")[-1].strip().split(","))):
						temp_list.append(cell.strip())

				if key:
					temp_DB[key] = temp_list

	fp.close()

	return temp_DB

def Net_Identify(name, Cenv):
	Group = 7 # OTHER
	Match = ""

	for key in Cenv:
		if "<Ignore>" in key:
			name = name.replace(Cenv[key][0], "")

	for keyword in Cenv["<DM>[Net Identification]"]:
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I) # re.I (or re.IGNORECASE) = No distinction between upper and lower case letters.
		if m:
			Match = m.group()
			Group = 0 # "DM"
			break

	for keyword in Cenv["<CLK_P>[Net Identification]"]:
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I)
		if m:
			Match = m.group()
			Group = 4 # CLK
			break

	for keyword in Cenv["<CLK_N>[Net Identification]"]:
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I)
		if m:
			Match = m.group()
			Group = 5 # CLK#
			break

	for keyword in Cenv["<ADDR>[Net Identification]"]:		
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I)
		if m:
			Match = m.group()
			Group = 6 # ADDR
			break

	for keyword in Cenv["<DQS_P>[Net Identification]"]:
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I)
		if m:
			Match = m.group()
			Group = 2 # DQS
			break

	for keyword in Cenv["<DQS_N>[Net Identification]"]:
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I)
		if m:
			Match = m.group()
			Group = 3 # DQS#
			break

	for keyword in Cenv["<DQ>[Net Identification]"]:
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I)
		if m:
			Match = m.group()
			Group = 1 # DQ
			break

	return Group, Match

def Plot_Eye(Report_Name, PlotList, vmin, vmax, Eye_Measure_Results, Bitmap_Flag):
	try:
		oProject = sub_DB.AEDT["Project"]
		oDesign = sub_DB.AEDT["Design"]
		if "Module" in sub_DB.AEDT.keys():
			oModule = sub_DB.AEDT["Module"]
		else:
			oModule = oDesign.GetModule("ReportSetup")
		Log("		(AEDT Setup) = Done")

		Report_names = oModule.GetAllReportNames()
		if Report_Name in Report_names:
			oModule.DeleteReports([Report_Name])
		Log("		(Delete Duplicate Reports) = Done")

		# Create Variable List
		Var_list = []
		Var_list.append("Time:=")
		Var_list.append(["All"])
		Sim_type = oDesign.GetDesignType()			
		if Sim_type == "Circuit Netlist":
			pass
		else:
			Global_Varlist = oProject.GetVariables()
			Local_Varlist = oDesign.GetVariables()					
			for var in Global_Varlist:
				Var_list.append(var + ":=")
				Var_list.append(["All"])
		Log("		(Create Variable List) = Done")

		# Plot Eye
		oModule.CreateReport(Report_Name, "Eye Diagram", "Rectangular Plot", sub_DB.Eye_Form._ComboBox_SolutionName.Text, 
		[
			"NAME:Context",
			"SimValueContext:="	, [1,0,2,0,False,False,-1,1,0,1,1,"",0,0,"DE",False,"0","DP",False,"500000000","DT",False,"0.001","NUMLEVELS",False,"0","WE",False,sub_DB.total_waveform_length,"WM",False,sub_DB.total_waveform_length,"WN",False,"0ps","WS",False,"0ps"]
		], 
		Var_list, 
		[
			"Component:="		, PlotList
		], 
		[
			"Unit Interval:="	, str(1/(float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000))+"s",
			"Offset:="		, str(sub_DB.Option_Form._TextBox_EyeOffset.Text) + "ns",
			"Auto Delay:="		, True,
			"Manual Delay:="	, "0ps",
			"AutoCompCrossAmplitude:=", True,
			"CrossingAmplitude:="	, "0mV",
			"AutoCompEyeMeasurementPoint:=", True,
			"EyeMeasurementPoint:="	, (1/(float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000))/2
		])
		Log("		(Plot Eye) = Done")

		Log("		(Change Property)")
		for eyename in PlotList:			
			if sub_DB.var_string == "":
				oModule.ChangeProperty(["NAME:AllTabs",
											["NAME:Eye",
												["NAME:PropServers", Report_Name + ":EyeDisplayTypeProperty"],
												["NAME:ChangedProps",
													["NAME:Rectangular Plot", "Value:=", False]
												]
											],
											["NAME:Attributes",
												["NAME:PropServers", Report_Name + ":" + eyename + ":Curve1:Eye"],
												["NAME:ChangedProps",
													["NAME:View Type", "Value:=", "Line"],
													["NAME:Line Color", "R:=", 0, "G:=", 0, "B:=", 255],
													["NAME:Line Width", "Value:=", "2"]
												]
											],
											["NAME:Legend",
												["NAME:PropServers", Report_Name + ":Legend"],
												["NAME:ChangedProps",
													["NAME:Show Trace Name", "Value:=", False],
													["NAME:Show Variation Key", "Value:=", False],
													["NAME:Show Solution Name", "Value:=", True]
												]
											],
											["NAME:Axis",
												["NAME:PropServers", Report_Name + ":AxisY1"],
												["NAME:ChangedProps",
													["NAME:Display Name", "Value:=", False]
												]
											],
											["NAME:Scaling",
												["NAME:PropServers", Report_Name + ":AxisY1"],
												["NAME:ChangedProps",
													["NAME:Specify Min", "Value:=", True],
													["NAME:Specify Max", "Value:=", True],
													["NAME:Min", "Value:=", str(vmin) + "mV"],
													["NAME:Max", "Value:=", str(vmax) + "mV"]
												]
											]
										])
			else:
				oModule.ChangeProperty(["NAME:AllTabs",
						  ["NAME:Eye", ["NAME:PropServers", Report_Name + ":EyeDisplayTypeProperty"], ["NAME:ChangedProps"
							, ["NAME:Rectangular Plot", "Value:=", False]]],
						  ["NAME:Attributes", ["NAME:PropServers", Report_Name + ":" + eyename + ":" + sub_DB.var_string + " [Curve1]:Eye"], ["NAME:ChangedProps"
							, ["NAME:View Type", "Value:=", "Line"]
							, ["NAME:Line Color", "R:=", 0, "G:=", 0, "B:=", 255]
							, ["NAME:Line Width", "Value:=", "2"]]],
						  ["NAME:Legend", ["NAME:PropServers", Report_Name + ":Legend"], ["NAME:ChangedProps"
							, ["NAME:Show Trace Name", "Value:=", False]
							, ["NAME:Show Variation Key", "Value:=", False]
							, ["NAME:Show Solution Name", "Value:=", True]]],
						  ["NAME:Axis", ["NAME:PropServers", Report_Name + ":AxisY1"], ["NAME:ChangedProps"
							, ["NAME:Display Name", "Value:=", False]]],
						  ["NAME:Scaling", ["NAME:PropServers", Report_Name + ":AxisY1"], ["NAME:ChangedProps"
							, ["NAME:Specify Min", "Value:=", True]
							, ["NAME:Specify Max", "Value:=", True]
							, ["NAME:Min", "Value:=", str(vmin) + "mV"]
							, ["NAME:Max", "Value:=", str(vmax) + "mV"]]]])
		Log("			= Report Name Changed, %s" % Report_Name)
		Log("			= Line Width Changed, 2")
		Log("			= Line Color Changed, R:0, G:0, B:255")
		Log("			= Y Axis Changed, Max.:%s[mV] Min.:%s[mV]" % (str(vmax), str(vmin)))
	
		oModule.ChangeProperty(["NAME:AllTabs",
			["NAME:Axis", ["NAME:PropServers", Report_Name + ":AxisX"], ["NAME:ChangedProps", ["NAME:Display Name", "Value:=", False]]],
			["NAME:Scaling", ["NAME:PropServers", Report_Name + ":AxisX"], ["NAME:ChangedProps", ["NAME:Specify Max", "Value:=", True],
			["NAME:Max", "Value:=", str(2/(float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000)) + "s"]]]])
		Log("			= X Axis Changed")

		oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
				["NAME:ChangedProps",["NAME:Show Trace Name","Value:=", False]]]])
		Log("			= Show Trace Name, False")

		oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
				["NAME:ChangedProps",["NAME:Show Solution Name","Value:=", False]]]])
		Log("			= Show Solution Name, False")

		oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
				["NAME:ChangedProps",["NAME:Show Variation Key","Value:=", False]]]])
		Log("			= Show Variation Key, False")
	
		#oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
		#		["NAME:ChangedProps",["NAME:DockMode","Value:=", "Dock Left"]]]])
		#Log("			= Legend Location (Dock Left)")	

		# for New Eye
		if sub_DB.Eyeflag:
			Vref = float(sub_DB.Eye_Form._TextBox_VcentDQ.Text)
			V_high = Vref + float(sub_DB.Eye_Form._TextBox_VdIVW.Text)/2
			V_low = Vref - float(sub_DB.Eye_Form._TextBox_VdIVW.Text)/2
			T_left = round(1/float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000) - Eye_Measure_Results[PlotList[0]][0]/float(2)
			T_right = round(1/float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000) + Eye_Measure_Results[PlotList[0]][0]/float(2)
	
			oModule.ChangeProperty(["NAME:AllTabs", ["NAME:Mask", ["NAME:PropServers",
					  Report_Name + ":EyeDisplayTypeProperty"], ["NAME:ChangedProps", ["NAME:Mask", "Version:=",
					  1, "ShowLimits:=", False, "UpperLimit:=", 1, "LowerLimit:=", 0, "XUnits:=", "ps", "YUnits:=",
					  "mV", ["NAME:MaskPoints",T_left, V_high,T_left, V_low,T_right, V_low,T_right, V_high]]]]])
			Log("			= Create Eye Mask")

			#noteh = (vmax - Vref) / (vmax - vmin) * 9500
			#oModule.AddNote(Report_Name, ["NAME:NoteDataSource", ["NAME:NoteDataSource", "SourceName:=",
			#				"Note1", "HaveDefaultPos:=", True, "DefaultXPos:=", 4500, "DefaultYPos:=",
			#				noteh, "String:=", str(Eye_Measure_Results[PlotList[0]][0]) + " / " + str(round(sub_DB.Jitter_RMS[PlotList[0]],1))]])
			#Log("			= Add Note, Width:%s[ps] Jitter(RMS):%s[ps]" % (str(Eye_Measure_Results[PlotList[0]][0]), str(round(sub_DB.Jitter_RMS[PlotList[0]],1))))

		# for Old Eye
		else:
			Vref = float(sub_DB.Eye_Form._TextBox_Vref.Text)

			V_IHAC_DQ = Vref + float(sub_DB.Eye_Form._ComboBox_AC_DQ.Text)
			V_ILAC_DQ = Vref - float(sub_DB.Eye_Form._ComboBox_AC_DQ.Text)		
			V_IHAC_ADDR = Vref + float(sub_DB.Eye_Form._ComboBox_AC_ADDR.Text)
			V_ILAC_ADDR = Vref - float(sub_DB.Eye_Form._ComboBox_AC_ADDR.Text)
			V_IHDC_DQ = Vref + float(sub_DB.Eye_Form._TextBox_DC_DQ.Text)
			V_ILDC_DQ = Vref - float(sub_DB.Eye_Form._TextBox_DC_DQ.Text)		
			V_IHDC_ADDR = Vref + float(sub_DB.Eye_Form._TextBox_DC_ADDR.Text)
			V_ILDC_ADDR = Vref - float(sub_DB.Eye_Form._TextBox_DC_ADDR.Text)

			T_left = round(1/float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000) - Eye_Measure_Results[PlotList[0]][0]/float(2)
			T_right = round(1/float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000) + Eye_Measure_Results[PlotList[0]][0]/float(2)

			oModule.ChangeProperty(["NAME:AllTabs", ["NAME:Mask", ["NAME:PropServers",
					  Report_Name + ":EyeDisplayTypeProperty"], ["NAME:ChangedProps", ["NAME:Mask", "Version:=",
					  1, "ShowLimits:=", False, "UpperLimit:=", 1, "LowerLimit:=", 0, "XUnits:=", "ps", "YUnits:=",
					  "mV", ["NAME:MaskPoints",T_left, V_IHAC_DQ, T_left, V_ILAC_DQ, T_right, V_ILDC_DQ, T_right, V_IHDC_DQ]]]]])
			Log("			= Create Eye Mask")

		noteh = (vmax - Vref) / (vmax - vmin) * 9500
		oModule.AddNote(Report_Name, ["NAME:NoteDataSource", ["NAME:NoteDataSource", "SourceName:=",
						"Note1", "HaveDefaultPos:=", True, "DefaultXPos:=", 4500, "DefaultYPos:=",
						noteh, "String:=", str(Eye_Measure_Results[PlotList[0]][0])]])
		Log("			= Add Note, Width:%s[ps]" % str(Eye_Measure_Results[PlotList[0]][0]))


		oModule.ChangeProperty(["NAME:AllTabs",
						["NAME:Note", ["NAME:PropServers", Report_Name + ":Note1"], ["NAME:ChangedProps"
						, ["NAME:Background Visibility", "Value:=", False]
						, ["NAME:Border Visibility", "Value:=", False]
						, ["NAME:Note Font", "Height:=", -17, "Width:=",
						0, "Escapement:=", 0, "Orientation:=", 0, "Weight:=", 700, "Italic:=", 0, "Underline:=",
						0, "StrikeOut:=", 0, "CharSet:=", 0, "OutPrecision:=", 3, "ClipPrecision:=", 2, "Quality:=",
						1, "PitchAndFamily:=", 34, "FaceName:=", "Arial", "R:=", 0, "G:=", 0, "B:=", 0]]]])

		if Bitmap_Flag:		
			imgw = int(sub_DB.Option_Form._TextBox_ImageWidth.Text)
			imgh = imgw / 5 * 4
			img_path = sub_DB.result_dir
			#img_path = img_path.replace("\\"+img_path.split("\\")[-1],"")
			oModule.ExportImageToFile(Report_Name, img_path + "\\" + Report_Name + ".gif", imgw * 2, imgh * 2)
			sub_DB.Excel_Img_File.append(img_path + "\\" + Report_Name + ".gif")
			Log("			= Save Image File, %s" % img_path + "\\" + Report_Name + ".gif")

	except Exception as e:		
		Log("	<Eye Plot> = Failed")
		Log(traceback.format_exc())
		print traceback.format_exc()
		MessageBox.Show("Fail to plot eye","Warning")						
		EXIT()

def Plot_Eye_Import(Report_Name, Import_file, PlotList, vmin, vmax, Eye_Measure_Results, Bitmap_Flag):
	try:
		oProject = sub_DB.AEDT["Project"]
		oDesign = sub_DB.AEDT["Design"]
		oModule = sub_DB.AEDT["Module"]
		Log("		(AEDT Setup) = Done")

		# Delete duplicate reports
		Report_names = oModule.GetAllReportNames()
		if Report_Name in Report_names:
			oModule.DeleteReports([Report_Name])
		Log("		(Delete Duplicate Reports) = Done")

		# Create Variable List
		Global_Varlist = oProject.GetVariables()
		Local_Varlist = oDesign.GetVariables()
		Var_list = []
		Var_list.append("Time:=")
		Var_list.append(["All"])
		for var in Global_Varlist:
			Var_list.append(var + ":=")
			Var_list.append(["All"])
		Log("		(Create Variable List) = Done")

		oModule.CreateReport(Report_Name, "Eye Diagram", "Rectangular Plot", "NexximTransient", 
		[
			"NAME:Context",
			"SimValueContext:="	, [1,0,2,0,False,False,-1,1,0,1,1,"",0,0,"DE",False,"0","DP",False,"500000000","DT",False,"0.001","NUMLEVELS",False,"1","WE",False,"10ns","WM",False,"10ns","WN",False,"0ns","WS",False,"0ns"]
		], 
		Var_list, 
		[
			"Component:="		, ["V(net_1)"]
		], 
		[
			"Unit Interval:="	, str(1/(float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000))+"s",
			"Offset:="		, str(sub_DB.Option_Form._TextBox_EyeOffset.Text) + "ns",
			"Auto Delay:="		, True,
			"Manual Delay:="	, "0ps",
			"AutoCompCrossAmplitude:=", True,
			"CrossingAmplitude:="	, "0mV",
			"AutoCompEyeMeasurementPoint:=", True,
			"EyeMeasurementPoint:="	, (1/(float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000))/2
		])
		oModule.ImportIntoReport(Report_Name, Import_file)

		oModule.DeleteTraces(["%s:=" % Report_Name, ["V(net_1)"]])
		Log("		(Plot Eye) = Done")
		Log("		(Change Property)")

		for eyename in PlotList:		
			oModule.ChangeProperty(["NAME:AllTabs",
					  ["NAME:Eye", ["NAME:PropServers", Report_Name + ":EyeDisplayTypeProperty"], ["NAME:ChangedProps"
						, ["NAME:Rectangular Plot", "Value:=", False]]],
					  ["NAME:Attributes", ["NAME:PropServers", Report_Name + ":" + eyename + ":Curve1:Eye"], ["NAME:ChangedProps"
						, ["NAME:View Type", "Value:=", "Line"]
						, ["NAME:Line Color", "R:=", 0, "G:=", 0, "B:=", 255]
						, ["NAME:Line Width", "Value:=", "2"]]],
					  ["NAME:Legend", ["NAME:PropServers", Report_Name + ":Legend"], ["NAME:ChangedProps"
						, ["NAME:Show Trace Name", "Value:=", False]
						, ["NAME:Show Variation Key", "Value:=", False]
						, ["NAME:Show Solution Name", "Value:=", True]]],
					  ["NAME:Axis", ["NAME:PropServers", Report_Name + ":AxisY1"], ["NAME:ChangedProps"
						, ["NAME:Display Name", "Value:=", False]]],
					  ["NAME:Scaling", ["NAME:PropServers", Report_Name + ":AxisY1"], ["NAME:ChangedProps"
						, ["NAME:Specify Min", "Value:=", True]
						, ["NAME:Specify Max", "Value:=", True]
						, ["NAME:Min", "Value:=", str(vmin) + "mV"]
						, ["NAME:Max", "Value:=", str(vmax) + "mV"]]]])
		Log("			= Report Name Changed, %s" % Report_Name)
		Log("			= Line Width Changed, 2")
		Log("			= Line Color Changed, R:0, G:0, B:255")
		Log("			= Y Axis Changed, Max.:%s[mV] Min.:%s[mV]" % (str(vmax), str(vmin)))

		oModule.ChangeProperty(["NAME:AllTabs",
			["NAME:Axis", ["NAME:PropServers", Report_Name + ":AxisX"], ["NAME:ChangedProps", ["NAME:Display Name", "Value:=", False]]],
			["NAME:Scaling", ["NAME:PropServers", Report_Name + ":AxisX"], ["NAME:ChangedProps", ["NAME:Specify Max", "Value:=", True],
			["NAME:Max", "Value:=", str(2/(float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000)) + "s"]]]])
		Log("			= X Axis Changed")

		oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
				["NAME:ChangedProps",["NAME:Show Trace Name","Value:=", False]]]])
		Log("			= Show Trace Name, False")

		oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
				["NAME:ChangedProps",["NAME:Show Solution Name","Value:=", False]]]])
		Log("			= Show Solution Name, False")

		oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
				["NAME:ChangedProps",["NAME:Show Variation Key","Value:=", False]]]])
		Log("			= Show Variation Key, False")
	
		#oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
		#		["NAME:ChangedProps",["NAME:DockMode","Value:=", "Dock Left"]]]])
		#Log("			= Legend Location (Dock Left)")

		# for New Eye
		if sub_DB.Eyeflag:	
			Vref = float(sub_DB.Eye_Form._TextBox_VcentDQ.Text)
			V_high = Vref + float(sub_DB.Eye_Form._TextBox_VdIVW.Text)/2
			V_low = Vref - float(sub_DB.Eye_Form._TextBox_VdIVW.Text)/2
			T_left = round(1/float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000) - Eye_Measure_Results[PlotList[0]][0]/float(2)
			T_right = round(1/float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000) + Eye_Measure_Results[PlotList[0]][0]/float(2)
	
			oModule.ChangeProperty(["NAME:AllTabs", ["NAME:Mask", ["NAME:PropServers",
					  Report_Name + ":EyeDisplayTypeProperty"], ["NAME:ChangedProps", ["NAME:Mask", "Version:=",
					  1, "ShowLimits:=", False, "UpperLimit:=", 1, "LowerLimit:=", 0, "XUnits:=", "ps", "YUnits:=",
					  "mV", ["NAME:MaskPoints",T_left, V_high,T_left, V_low,T_right, V_low,T_right, V_high]]]]])
			Log("			= Create Eye Mask")

		# for Old Eye
		else:
			Vref = float(sub_DB.Eye_Form._TextBox_Vref.Text)

			V_IHAC_DQ = Vref + float(sub_DB.Eye_Form._ComboBox_AC_DQ.Text)
			V_ILAC_DQ = Vref - float(sub_DB.Eye_Form._ComboBox_AC_DQ.Text)		
			V_IHAC_ADDR = Vref + float(sub_DB.Eye_Form._ComboBox_AC_ADDR.Text)
			V_ILAC_ADDR = Vref - float(sub_DB.Eye_Form._ComboBox_AC_ADDR.Text)
			V_IHDC_DQ = Vref + float(sub_DB.Eye_Form._TextBox_DC_DQ.Text)
			V_ILDC_DQ = Vref - float(sub_DB.Eye_Form._TextBox_DC_DQ.Text)		
			V_IHDC_ADDR = Vref + float(sub_DB.Eye_Form._TextBox_DC_ADDR.Text)
			V_ILDC_ADDR = Vref - float(sub_DB.Eye_Form._TextBox_DC_ADDR.Text)

			T_left = round(1/float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000) - Eye_Measure_Results[PlotList[0]][0]/float(2)
			T_right = round(1/float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000) + Eye_Measure_Results[PlotList[0]][0]/float(2)

			oModule.ChangeProperty(["NAME:AllTabs", ["NAME:Mask", ["NAME:PropServers",
					  Report_Name + ":EyeDisplayTypeProperty"], ["NAME:ChangedProps", ["NAME:Mask", "Version:=",
					  1, "ShowLimits:=", False, "UpperLimit:=", 1, "LowerLimit:=", 0, "XUnits:=", "ps", "YUnits:=",
					  "mV", ["NAME:MaskPoints",T_left, V_IHAC_DQ, T_left, V_ILAC_DQ, T_right, V_ILDC_DQ, T_right, V_IHDC_DQ]]]]])
			Log("			= Create Eye Mask")

		noteh = (vmax - Vref) / (vmax - vmin) * 9500
		oModule.AddNote(Report_Name, ["NAME:NoteDataSource", ["NAME:NoteDataSource", "SourceName:=",
						"Note1", "HaveDefaultPos:=", True, "DefaultXPos:=", 4500, "DefaultYPos:=",
						noteh, "String:=", str(Eye_Measure_Results[PlotList[0]][0])]])
		Log("			= Add Note, Width:%s[ps]" % str(Eye_Measure_Results[PlotList[0]][0]))

		oModule.ChangeProperty(["NAME:AllTabs",
					  ["NAME:Note", ["NAME:PropServers", Report_Name + ":Note1"], ["NAME:ChangedProps"
					  , ["NAME:Background Visibility", "Value:=", False]
					  , ["NAME:Border Visibility", "Value:=", False]
					  , ["NAME:Note Font", "Height:=", -17, "Width:=",
						0, "Escapement:=", 0, "Orientation:=", 0, "Weight:=", 700, "Italic:=", 0, "Underline:=",
						0, "StrikeOut:=", 0, "CharSet:=", 0, "OutPrecision:=", 3, "ClipPrecision:=", 2, "Quality:=",
						1, "PitchAndFamily:=", 34, "FaceName:=", "Arial", "R:=", 0, "G:=", 0, "B:=", 0]]]])

		if Bitmap_Flag:
			imgw = int(sub_DB.Option_Form._TextBox_ImageWidth.Text)
			imgh = imgw / 5 * 4
			img_path = sub_DB.result_dir
			#img_path = img_path.replace("\\"+img_path.split("\\")[-1],"")
			oModule.ExportImageToFile(Report_Name, img_path + "\\" + Report_Name + ".gif", imgw * 2, imgh * 2)
			sub_DB.Excel_Img_File.append(img_path + "\\" + Report_Name + ".gif")
			Log("			= Save Image File, %s" % img_path + "\\" + Report_Name + ".gif")

	except Exception as e:		
		Log("	<Eye Plot> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to plot eye","Warning")						
		EXIT()

def Interpolate_1st(x1,y1,x2,y2,y3):
	x = abs(y3-y1)*(x2-x1)/abs(y2-y1)+x1
	return int(round(x))

def Gen_waveform_file(Input_File, Plot_list, Group_flag):
	try:
		Log("		(Get Waveform)")
		Save_File = sub_DB.result_dir + "\\temp.csv"

		shutil.copy(Input_File, Save_File)
		Log("			= Copy File Done")

		xlApp = Excel.ApplicationClass()
		xlApp.Visible = False
		xlApp.DisplayAlerts = False
		xlbook = xlApp.Workbooks.Open(Save_File)
		xlsheet = xlbook.Worksheets.Item[1]

		if Group_flag:
			for i in range(0, len(Plot_list)):
				# Replace not allowed symbol for trace name
				xlsheet.Cells[1, i+2].Value2 = xlsheet.Cells[1, i+2].Value2.replace("-","_")
		else:	
			col_idx = 2
			while(xlsheet.Cells[1, col_idx].Value2 != None):			
				keyword = xlsheet.Cells[1, col_idx].Value2.split("[")[0].strip().replace("-","_")
				if not keyword in Plot_list:
					xlsheet.Columns(col_idx).Delete()
				else:
					col_idx += 1
			# Replace not allowed symbol for trace name
			xlsheet.Cells[1, 2].Value2 = xlsheet.Cells[1, 2].Value2.replace("-","_")

		xlbook.SaveAs(Save_File)

		xlbook.Close()
		xlApp.Quit()

		ReleaseObject(xlsheet)
		ReleaseObject(xlbook)
		ReleaseObject(xlApp)

		Log("			= Save File Done")
		return Save_File

	except Exception as e:		
		Log("	<Eye Plot> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to plot eye","Warning")						
		EXIT()

def Check_Input(self):
	flag = True
	show_msg_flag = False
	msg = ""
	###############
	# Check Blank #
	###############
	if self._TextBox_InputFile.Text == "":
		#self._TextBox_InputFile.BackColor = System.Drawing.Color.Moccasin
		msg += "   * Input File\n"
		flag = False
		show_msg_flag = True

	if self._ComboBox_Design.Text == "":
		#self._ComboBox_Design.BackColor = System.Drawing.Color.Moccasin
		msg += "   * Deseign\n"
		flag = False
		show_msg_flag = True
	
	if len(self._CheckedListBox_ReportName.CheckedItems) == 0:
		#self._CheckedListBox_ReportName.BackColor = System.Drawing.Color.Moccasin
		msg += "   * Report Name - No reports checked\n"
		flag = False
		show_msg_flag = True

	if self._ComboBox_SolutionName.Text == "":
		msg += "   * Setup Name\n"
		flag = False
		show_msg_flag = True

	if self._ComboBox_DDRGen.Text == "":
		msg += "   * DDR Generation\n"
		flag = False
		show_msg_flag = True

	if self._ComboBox_DataRate.Text == "":
		msg += "   * Data Rate\n"
		flag = False
		show_msg_flag = True

	if self._TextBox_Offset.Text == "":
		msg += "   * Eye Offset\n"
		flag = False
		show_msg_flag = True

	else:
		Offset_list = list(self._TextBox_Offset.Text)
		num_flag = True
		for item in Offset_list:
			# "."
			if not ord(item) == 46:
				if not 47 < ord(item) <58:
					num_flag = False
					break

		if num_flag:
			if float(self._TextBox_Offset.Text) > 10:
				MessageBox.Show("The maximum eye offset is 10[ns].\nCheck the entered value for eye offset.\n\n" + "Entered Value : %s[ns]" % self._TextBox_Offset.Text)
				flag = False
				show_msg_flag = False
			
		else:
			MessageBox.Show("Only numbers can be entered for eye offset.\n\n" + "You entered : %s" % self._TextBox_Offset.Text)
			flag = False
			show_msg_flag = False

	# New Eye
	if sub_DB.Eyeflag:
		# for VdIVW
		###############
		# Check Blank #
		###############
		if self._TextBox_VdIVW.Text == "":
			msg += "   * VdIW - Voltage Spec\n"
			flag = False
			show_msg_flag = True
		
		else:
			################
			# Check Number #
			################
			VdIVW_list = list(self._TextBox_VdIVW.Text)
			num_flag = True
			for item in VdIVW_list:
				# "."
				if not ord(item) == 46:
					if not 47 < ord(item) <58:
						num_flag = False
						break

			##############
			# Check unit #
			##############
			if num_flag:
				if float(self._TextBox_VdIVW.Text) < 3:
					MessageBox.Show("The unit of VdIVW is [mV]. Check the entered value for VdIVW.\n\n" + "Entered Value : %s" % self._TextBox_VdIVW.Text)					
					flag = False
					show_msg_flag = False
			
			else:
				MessageBox.Show("Only numbers can be entered for VdIVW.\n\n" + "You entered : %s" % self._TextBox_VdIVW.Text)
				flag = False
				show_msg_flag = False

		# for TdIVW
		###############
		# Check Blank #
		###############
		if self._TextBox_TdIVW.Text == "":
			msg += "   * TdIVW - Timing Spec\n"
			flag = False
			show_msg_flag = True
		
		else:
			################
			# Check Number #
			################
			TdIVW_list = list(self._TextBox_TdIVW.Text)
			num_flag = True
			for item in TdIVW_list:
				# "."
				if not ord(item) == 46:
					if not 47 < ord(item) <58:
						num_flag = False
						break

			##############
			# Check unit #
			##############
			if num_flag:
				if float(self._TextBox_TdIVW.Text) > 1:
					MessageBox.Show("The unit of TdIVW is [UI]. Check the entered value for TdIVW.\n\n" + "Entered Value : %s" % self._TextBox_TdIVW.Text)					
					flag = False
					show_msg_flag = False
			
			else:
				MessageBox.Show("Only numbers can be entered for TdIVW.\n\n" + "You entered : %s" % self._TextBox_TdIVW.Text)
				flag = False
				show_msg_flag = False

		# for Vcent_DQ		
		if not self._TextBox_VcentDQ.Text == "Auto":
			###############
			# Check Blank #
			###############
			if self._TextBox_VcentDQ.Text == "":
				msg += "   * Vcent_DQ\n"
				flag = False
				show_msg_flag = True
		
			else:
				################
				# Check Number #
				################
				Vref_list = list(self._TextBox_VcentDQ.Text)
				num_flag = True
				for item in Vref_list:
					# "."
					if not ord(item) == 46:
						if not 47 < ord(item) <58:
							num_flag = False
							break

				##############
				# Check unit #
				##############
				if num_flag:
					if float(self._TextBox_VcentDQ.Text) < 1.5:
						MessageBox.Show("The unit of Vcent_DQ is [mV]. Check the entered value for Vcent_DQ.\n\n" + "Entered Value : %s" % self._TextBox_VcentDQ.Text)
						flag = False
						show_msg_flag = False
			
				else:
					MessageBox.Show("Only numbers and \"Auto\"can be entered for Vcent_DQ.\n\n" + "You entered : %s" % self._TextBox_VcentDQ.Text)
					flag = False
					show_msg_flag = False

	# Old Eye
	else:
		# for Vref
		###############
		# Check Blank #
		###############
		if not self._TextBox_Vref.Text == "Auto":
			if self._TextBox_Vref.Text == "":
				msg += "   * Vref\n"
				flag = False
				show_msg_flag = True
		
			else:
				################
				# Check Number #
				################
				Vref_list = list(self._TextBox_Vref.Text)
				num_flag = True
				for item in Vref_list:
					# "."
					if not ord(item) == 46:
						if not 47 < ord(item) <58:
							num_flag = False
							break

				##############
				# Check unit #
				##############
				if num_flag:
					if float(self._TextBox_Vref.Text) < 2:
						MessageBox.Show("The unit of Vref is [mV]. Check the entered value for Vref.\n\n" + "Entered Value : %s" % self._TextBox_Vref.Text)
						flag = False
						show_msg_flag = False
			
				else:
					MessageBox.Show("Only numbers can be entered for Vref.\n\n" + "You entered : %s" % self._TextBox_Vref.Text)
					flag = False
					show_msg_flag = False

		# for DQ Setup Time
		###############
		# Check Blank #
		###############
		if self._TextBox_DQSetup.Text == "":
			msg += "   * DQ Setup Time\n"
			flag = False
			show_msg_flag = True
		
		else:
			################
			# Check Number #
			################
			DQSetup_list = list(self._TextBox_DQSetup.Text)
			num_flag = True
			for item in DQSetup_list:
				# "."
				if not ord(item) == 46:
					if not 47 < ord(item) <58:
						num_flag = False
						break

			##############
			# Check unit #
			##############
			if num_flag:
				if float(self._TextBox_DQSetup.Text) < 1:
					MessageBox.Show("The unit of DQ setup time is [ps]. Check the entered value for DQ setup time.\n\n" + "Entered Value : %s" % self._TextBox_DQSetup.Text)
					flag = False
					show_msg_flag = False
			
			else:
				MessageBox.Show("Only numbers can be entered for DQ setup time.\n\n" + "You entered : %s" % self._TextBox_DQSetup.Text)
				flag = False
				show_msg_flag = False

		# for DQ Hold Time
		###############
		# Check Blank #
		###############
		if self._TextBox_DQHold.Text == "":
			msg += "   * DQ Hold Time\n"
			flag = False
			show_msg_flag = True
		
		else:
			################
			# Check Number #
			################
			DQHold_list = list(self._TextBox_DQHold.Text)
			num_flag = True
			for item in DQHold_list:
				# "."
				if not ord(item) == 46:
					if not 47 < ord(item) <58:
						num_flag = False
						break

			##############
			# Check unit #
			##############
			if num_flag:
				if float(self._TextBox_DQHold.Text) < 1:
					MessageBox.Show("The unit of DQ hold time is [ps]. Check the entered value for DQ hold time.\n\n" + "Entered Value : %s" % self._TextBox_DQHold.Text)
					flag = False
					show_msg_flag = False
			
			else:
				MessageBox.Show("Only numbers can be entered for DQ hold time.\n\n" + "You entered : %s" % self._TextBox_DQHold.Text)
				flag = False
				show_msg_flag = False

		# for ADDR Setup Time
		###############
		# Check Blank #
		###############
		if self._TextBox_ADDRSetup.Text == "":
			msg += "   * Address Setup Time\n"
			flag = False
			show_msg_flag = True
		
		else:
			################
			# Check Number #
			################
			ADDRSetup_list = list(self._TextBox_ADDRSetup.Text)
			num_flag = True
			for item in ADDRSetup_list:
				# "."
				if not ord(item) == 46:
					if not 47 < ord(item) <58:
						num_flag = False
						break

			##############
			# Check unit #
			##############
			if num_flag:
				if float(self._TextBox_ADDRSetup.Text) < 1:
					MessageBox.Show("The unit of address setup time is [ps]. Check the entered value for address setup time.\n\n" + "Entered Value : %s" % self._TextBox_ADDRSetup.Text)
					flag = False
					show_msg_flag = False
			
			else:
				MessageBox.Show("Only numbers can be entered for address setup time.\n\n" + "You entered : %s" % self._TextBox_ADDRSetup.Text)
				flag = False
				show_msg_flag = False

		# for ADDR Hold Time
		###############
		# Check Blank #
		###############
		if self._TextBox_ADDRHold.Text == "":
			msg += "   * Address Hold Time\n"
			flag = False
			show_msg_flag = True
		
		else:
			################
			# Check Number #
			################
			ADDRHold_list = list(self._TextBox_ADDRHold.Text)
			num_flag = True
			for item in ADDRHold_list:
				# "."
				if not ord(item) == 46:
					if not 47 < ord(item) <58:
						num_flag = False
						break

			##############
			# Check unit #
			##############
			if num_flag:
				if float(self._TextBox_ADDRHold.Text) < 1:
					MessageBox.Show("The unit of address hold time is [ps]. Check the entered value for address hold time.\n\n" + "Entered Value : %s" % self._TextBox_ADDRHold.Text)
					flag = False
					show_msg_flag = False
			
			else:
				MessageBox.Show("Only numbers can be entered for address hold time.\n\n" + "You entered : %s" % self._TextBox_ADDRHold.Text)
				flag = False
				show_msg_flag = False

		# for VDC_DQ
		###############
		# Check Blank #
		###############
		if self._TextBox_DC_DQ.Text == "":
			msg += "   * Vdc for DQ\n"
			flag = False
			show_msg_flag = True
		
		else:
			################
			# Check Number #
			################
			VDC_DQ_list = list(self._TextBox_DC_DQ.Text)
			num_flag = True
			for item in VDC_DQ_list:
				# "."
				if not ord(item) == 46:
					if not 47 < ord(item) <58:
						num_flag = False
						break

			##############
			# Check unit #
			##############
			if num_flag:
				if float(self._TextBox_DC_DQ.Text) < 2:
					MessageBox.Show("The unit of Vdc DQ is [mV]. Check the entered value for Vdc DQ.\n\n" + "Entered Value : %s" % self._TextBox_DC_DQ.Text)
					flag = False
					show_msg_flag = False
			
			else:
				MessageBox.Show("Only numbers can be entered for Vdc DQ.\n\n" + "You entered : %s" % self._TextBox_DC_DQ.Text)
				flag = False
				show_msg_flag = False

		# for VDC_ADDR
		###############
		# Check Blank #
		###############
		if self._TextBox_DC_ADDR.Text == "":
			msg += "   * Vdc for Address\n"
			flag = False
			show_msg_flag = True
		
		else:
			################
			# Check Number #
			################
			VDC_ADDR_list = list(self._TextBox_DC_ADDR.Text)
			num_flag = True
			for item in VDC_ADDR_list:
				# "."
				if not ord(item) == 46:
					if not 47 < ord(item) <58:
						num_flag = False
						break

			##############
			# Check unit #
			##############
			if num_flag:
				if float(self._TextBox_DC_ADDR.Text) < 2:
					MessageBox.Show("The unit of Vdc address is [mV]. Check the entered value for Vdc address.\n\n" + "Entered Value : %s" % self._TextBox_DC_ADDR.Text)
					flag = False
					show_msg_flag = False
			
			else:
				MessageBox.Show("Only numbers can be entered for Vdc address.\n\n" + "You entered : %s" % self._TextBox_DC_ADDR.Text)
				flag = False
				show_msg_flag = False

	return flag, show_msg_flag, msg

def Log(msg):

	sub_DB.Log += "\n" + time.strftime('%H:%M:%S') + "\t" + msg

def LogSave(iter, File=None):
	try:
		if not sub_DB.Eye_Form._TextBox_InputFile.Text == "":
			if File == None:
				if iter <= 1:
					f = open(sub_DB.result_dir + '\\ddr_' + time.strftime('%Y%m%d_%H%M%S') + '.log', 'w')
					f.write(sub_DB.Log)	
					f.close()
					sub_DB.Log_File = sub_DB.result_dir + '\\ddr_' + time.strftime('%Y%m%d_%H%M%S') + '.log'
				else:
					f = open(sub_DB.Log_File, 'w')
					f.write(sub_DB.Log)	
					f.close()
			else:
				f = open(File, 'w')
				f.write(sub_DB.Log)	
				f.close()
	except Exception as e:				
		print traceback.format_exc()
		
def CnfSave(File):	
	#################
	# Create Header #
	#################
	try:
		Log("	<Save Cnf>" )
		Log("		= %s" % File)
		cnf_log = ""
		cnf_log += "############################################################"
		cnf_log += "\n" + "#	Ansys DDR Wizard %s Configuration File" % sub_DB.Version
		cnf_log += "\n" + "#		Input File : " +  sub_DB.Input_File
		cnf_log += "\n" + "#		Start : " +  sub_DB.start_time
		cnf_log += "\n" + "#		End   : " +  time.strftime('%Y.%m.%d, %H:%M:%S')
		cnf_log += "\n" + "############################################################"

	except Exception as e:		
		Log("	<Save Cnf - Header> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to create Cnf header","Warning")						
		EXIT()

	###########
	# Version #
	###########	
	cnf_log += "\n\n" + "[Version] = %s" % sub_DB.Version

	####################
	# For EM Extractor #
	####################
	try:
		Log("	<Save Cnf - EM Extractor>")
		cnf_log += "\n\n" + "[EM]"

	except Exception as e:		
		Log("	<Save Cnf - EM Extractor> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to save Cnf - EM Extractor","Warning")						
		EXIT()

	#########################
	# For Circuit Simulator #
	#########################
	try:
		Log("	<Save Cnf - Circuit Simulator>")
		cnf_log += "\n\n" + "[Tran]"

	except Exception as e:		
		Log("	<Save Cnf - Circuit Simulator> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to save Cnf - Circuit Simulator","Warning")						
		EXIT()

	####################
	# For Eye Analyzer #
	####################
	try:
		Log("	<Save Cnf - Eye Analyzer>")
		cnf_log += "\n\n" + "[Eye]"
		# --------- Setup----------------
		cnf_log += "\n\t" + "<Setup>"
		#	 Input File
		cnf_log += "\n\t\t" + "(Input File)"
		if not sub_DB.Eye_Form._TextBox_InputFile.Text == "":
			cnf_log += " = %s, %d" % (sub_DB.Eye_Form._TextBox_InputFile.Text, sub_DB.InputFile_Flag)

		#	 Design
		cnf_log += "\n\t\t" + "(Design)"
		if not sub_DB.Eye_Form._ComboBox_Design.Text == "":
			cnf_log += " = %s" % sub_DB.Eye_Form._ComboBox_Design.Text

		#	 Report Name
		cnf_log += "\n\t\t" + "(Report Name)"		
		for item in sub_DB.Eye_Form._CheckedListBox_ReportName.Items:
			if item in sub_DB.Eye_Form._CheckedListBox_ReportName.CheckedItems:
				cnf_log += "\n\t\t\t" + "= %s!" % item
			else:
				cnf_log += "\n\t\t\t" + "= %s" % item

		#	 Setup Name	
		cnf_log += "\n\t\t" + "(Setup Name)"
		if not sub_DB.Eye_Form._ComboBox_SolutionName.Text == "":
			cnf_log += " = %s" % sub_DB.Eye_Form._ComboBox_SolutionName.Text

		#	 DDR Gen
		cnf_log += "\n\t\t" + "(DDR Gen)"
		if not sub_DB.Eye_Form._ComboBox_DDRGen.Text == "":
			cnf_log += " = %s" % sub_DB.Eye_Form._ComboBox_DDRGen.Text

		#	 Data-rate
		cnf_log += "\n\t\t" + "(Data-rate)"
		if not sub_DB.Eye_Form._ComboBox_DataRate.Text == "":
			cnf_log += " = %s" % sub_DB.Eye_Form._ComboBox_DataRate.Text

		# --------- Eye Specifications ----------------
		cnf_log += "\n\n\t" + "<Eye Specifications>"
		#	 New Eye
		if sub_DB.Eyeflag:
			#	 Eyeflag for New Eye
			cnf_log += "\n\t\t" + "(Eye_Type) = Ture"

			#	 VdIVW
			cnf_log += "\n\t\t" + "(VdIVW)"
			if not sub_DB.Eye_Form._TextBox_VdIVW.Text == "":
				cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_VdIVW.Text

			#	 TdIVW
			cnf_log += "\n\t\t" + "(TdIVW)"
			if not sub_DB.Eye_Form._TextBox_TdIVW.Text == "":
				cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_TdIVW.Text

			#	 Vcent_DQ
			if sub_DB.Eye_Form._CheckBox_EditEnable_NewEye.Checked:
				cnf_log += "\n\t\t" + "(Vcent_DQ)"
				if not sub_DB.Eye_Form._TextBox_VcentDQ.Text == "":
					cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_VcentDQ.Text

		#	 Old Eye
		else:
			#	 Eyeflag for Old Eye
			cnf_log += "\n\t\t" + "(Eye_Type) = False"

			#	 AC_DQ
			cnf_log += "\n\t\t" + "(AC_DQ)"
			if sub_DB.Eye_Form._ComboBox_AC_DQ.Visible:				
				if not sub_DB.Eye_Form._ComboBox_AC_DQ.Text == "":
					cnf_log += " = %d, %s" % (sub_DB.Eye_Form._ComboBox_AC_DQ.SelectedIndex, sub_DB.Eye_Form._ComboBox_AC_DQ.Text)
			else:
				if not sub_DB.Eye_Form._TextBox_AC_DQ.Text == "":
					cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_AC_DQ.Text

			#	 AC_ADDR
			cnf_log += "\n\t\t" + "(AC_ADDR)"
			if sub_DB.Eye_Form._ComboBox_AC_ADDR.Visible:				
				if not sub_DB.Eye_Form._ComboBox_AC_ADDR.Text == "":
					cnf_log += " = %d, %s" % (sub_DB.Eye_Form._ComboBox_AC_ADDR.SelectedIndex, sub_DB.Eye_Form._ComboBox_AC_ADDR.Text)
			else:
				if not sub_DB.Eye_Form._TextBox_AC_ADDR.Text == "":
					cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_AC_ADDR.Text

			#	 DC_DQ
			cnf_log += "\n\t\t" + "(DQ_DC)"
			if not sub_DB.Eye_Form._TextBox_DC_DQ.Text == "":
				cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_DC_DQ.Text

			#	 DC_ADDR
			cnf_log += "\n\t\t" + "(DQ_ADDR)"
			if not sub_DB.Eye_Form._TextBox_DC_ADDR.Text == "":
				cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_DC_ADDR.Text

			#	 Vref
			cnf_log += "\n\t\t" + "(Vref)"
			if not sub_DB.Eye_Form._TextBox_Vref.Text == "":
				cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_Vref.Text

			#	 DQ_Setup
			cnf_log += "\n\t\t" + "(DQ_Setup)"
			if not sub_DB.Eye_Form._TextBox_DQSetup.Text == "":
				cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_DQSetup.Text

			#	 DQ_Hold
			cnf_log += "\n\t\t" + "(DQ_Hold)"
			if not sub_DB.Eye_Form._TextBox_DQHold.Text == "":
				cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_DQHold.Text

			#	 ADDR_Setup
			cnf_log += "\n\t\t" + "(ADDR_Setup)"
			if not sub_DB.Eye_Form._TextBox_ADDRSetup.Text == "":
				cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_ADDRSetup.Text

			#	 ADDR_Hold
			cnf_log += "\n\t\t" + "(ADDR_Hold)"
			if not sub_DB.Eye_Form._TextBox_ADDRHold.Text == "":
				cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_ADDRHold.Text

		# --------- Net Classification ----------------
		cnf_log += "\n\n\t" + "<Net Classification>"
		iter = 0
		for row in sub_DB.Net_Form._DataGridView.Rows:
			cnf_log += "\n\t\t" + " (%d) = %s, %s, %s, %s, %s" % (iter, str(row.Cells[0].Value), row.Cells[1].Value, row.Cells[2].Value, row.Cells[3].Value, row.Cells[4].Value)
			iter += 1

		# --------- Analyze Option ----------------
		cnf_log += "\n\n\t" + "<Analyze Option>"
		#	 Resources Folder
		cnf_log += "\n\t\t" + "(Resources Folder) = %s" % sub_DB.resource_dir

		#	 Definition File
		cnf_log += "\n\t\t" + "(Definition File) = %s" % sub_DB.Cenv["File"]

		#	 Configuration File
		cnf_log += "\n\t\t" + "(Configuration File) = %s" % sub_DB.Uenv["File"]

		#	 Eye Offset
		cnf_log += "\n\t\t" + "(Eye Offset)"
		if not sub_DB.Option_Form._TextBox_EyeOffset.Text == "":
			cnf_log += " = %s ns" % sub_DB.Option_Form._TextBox_EyeOffset.Text

		#	 Vref Method
		cnf_log += "\n\t\t" + "(Vref Method) = %d, %s" % (sub_DB.Option_Form._ComboBox_Vref.SelectedIndex, sub_DB.Option_Form._ComboBox_Vref.Text)
		if sub_DB.Option_Form._ComboBox_Vref.SelectedIndex == 1:
			cnf_log += "\n\t\t" + "(Manual Vref) = %s" % sub_DB.Option_Form._TextBox_Vref.Text


		#	 Analyze Method
		cnf_log += "\n\t\t" + "(Analyze Method) = %d, %s" % (sub_DB.Option_Form._ComboBox_Analyze.SelectedIndex, sub_DB.Option_Form._ComboBox_Analyze.Text)
	
		#	 Export Excel Report
		cnf_log += "\n\t\t" + "(Export Excel Report) = %s" % sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked
	
		#	 Image Width
		if sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked:
			if sub_DB.Option_Form._CheckBox_PlotEye.Checked:
				cnf_log += "\n\t\t" + "(Image Width)"
				cnf_log += " = %s pixel" % sub_DB.Option_Form._TextBox_ImageWidth.Text

		#	 Report Format
		if sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked:
			cnf_log += "\n\t\t" + "(Report Format) = %d, %s" % (sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex, sub_DB.Option_Form._ComboBox_ReportFormat.Text)

		#	 Plot Eye with Mask
		cnf_log += "\n\t\t" + "(Plot Eye with Mask) = %s" % sub_DB.Option_Form._CheckBox_PlotEye.Checked

		#	 Check DDR Compliance
		cnf_log += "\n\t\t" + "(Check DDR Compliance) = %s" % sub_DB.Option_Form._CheckBox_Compiance.Checked

		# --------- DDR Compliance ----------------
		if sub_DB.Option_Form._CheckBox_Compiance.Visible:
			#TODO : Save Cnf for DDR Compliance
			cnf_log += "\n\n\t" + "<DDR Compliance>"

	except Exception as e:
		Log("	<Save Cnf - Eye Analyzer> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to save Cnf - Eye Analyzer","Warning")						
		EXIT()

	#################
	# Save Cnf File #
	#################
	try:
		Log("	<Save Cnf File>")
		f = open(File, 'w')
		f.write(cnf_log)	
		f.close()

	except Exception as e:		
		Log("	<Save Cnf File> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to save Cnf file","Warning")						
		EXIT()

def CnfLoad(self, File):
	Initial()
	self._TextBox_InputFile.Text = ""
	self._ComboBox_Design.Items.Clear()
	self._CheckedListBox_ReportName.Items.Clear()
	self._ComboBox_SolutionName.Items.Clear()

	Uenv = Load_env(File)
	Uenv["File"] = File
	sub_DB.Uenv = Uenv	
	Log("	<Load the Latest Cnf - %s>" % File)

	version_check_flag = False
	#####################
	# Check Cnf Version #
	#####################
	for key in Uenv:		
		if "[Version]" in key:			
			cnf_version = Uenv[key][0]
			if Uenv[key][0] == sub_DB.Version:
				version_check_flag = True				
				break

	# Pass Version Check
	if version_check_flag:
		##################
		# Check Eye Flag #
		##################
		flag = True
		for key in Uenv:		
			if "(Eye_Type)" in key:				
				if Uenv[key][0] == "False":
					flag = False
					break

		#################
		# Load Eye Spec #
		#################
		for key in Uenv:
			#############################
			# Load Cnf for EM Extractor #
			#############################
			if "[EM]" in key:
				try:
					Log("		(Load EM)")
					pass

				except Exception as e:		
					Log("		(Load EM) : Failed")
					Log(traceback.format_exc())					
					MessageBox.Show("Fail to Load Cnf for EM Extractor","Warning")						
					EXIT()
				
			##################################
			# Load Cnf for Circuit Simulator #
			##################################
			elif "[Tran]" in key:
				try:
					Log("		(Load Tran)")
					pass

				except Exception as e:		
					Log("		(Load Tran) : Failed")
					Log(traceback.format_exc())
					MessageBox.Show("Fail to Load Cnf for Circuit Simulator","Warning")						
					EXIT()
			
			#############################
			# Load Cnf for Eye Analyzer #
			#############################
			elif "[Eye]" in key:				
				try:
					# --------- Setup----------------
					if "<Setup>" in key:
						# Input File
						if "(Input File)" in key:
							self._TextBox_InputFile.Text = Uenv[key][0]
							sub_DB.InputFile_Flag = int(Uenv[key][1])							
							self._TextBox_InputFile.BackColor = System.Drawing.Color.White
							result_dir = Uenv[key][0].split(".")[0] + "_DDR_Results"				
							sub_DB.result_dir = result_dir
							Log("		(Load Eye - Input File) = %s" % Uenv[key][0])

						# Design
						elif "(Design)" in key:
							self._ComboBox_Design.Text = Uenv[key][0]
							Log("		(Load Eye - Design) = %s" % Uenv[key][0])

						# Report Name
						elif "(Report Name)" in key:
							for i in range(0, len(Uenv[key])):
								self.Init_Flag = True
								if "!" in Uenv[key][i]:
									self._CheckedListBox_ReportName.Items.Add(Uenv[key][i].replace("!",""))
									self._CheckedListBox_ReportName.SetItemChecked(i, True)
									Log("		(Load Eye - Report Name) = True, %s" % Uenv[key][i])
								else:
									self._CheckedListBox_ReportName.Items.Add(Uenv[key][i])
									self._CheckedListBox_ReportName.SetItemChecked(i, False)
									Log("		(Load Eye - Report Name) = False, %s" % Uenv[key][i])

						# Setup Name
						elif "(Setup Name)" in key:				
							self._ComboBox_SolutionName.Text = Uenv[key][0]
							Log("		(Load Eye - Setup Name) = %s" % Uenv[key][0])

						# DDR Gen
						elif "(DDR Gen)" in key:
							self._ComboBox_DDRGen.Enabled = True
							self._ComboBox_DDRGen.Text = Uenv[key][0]
							Log("		(Load Eye - DDR Gen) = %s" % Uenv[key][0])

						# Data-rate
						elif "(Data-rate)" in key:
							self._ComboBox_DataRate.Enabled = True
							self._ComboBox_DataRate.BackColor = System.Drawing.Color.White
							self._ComboBox_DataRate.Text = Uenv[key][0]
							Log("		(Load Eye - Data-rate) = %s" % Uenv[key][0])

					# --------- Eye Specifications ----------------
					elif "<Eye Specifications>" in key:						
						# New Eye
						if flag:
							# VdIVW
							if "(VdIVW)" in key:				
								self._TextBox_VdIVW.Text = Uenv[key][0]
								Log("		(Load Eye - VdIVW) = %s" % Uenv[key][0])

							# TdIVW
							elif "(TdIVW)" in key:				
								self._TextBox_TdIVW.Text = Uenv[key][0]
								Log("		(Load Eye - TdIVW) = %s" % Uenv[key][0])

							# Vcent_DQ
							elif "(Vcent_DQ)" in key:				
								self._TextBox_VcentDQ.Text = Uenv[key][0]
								Log("		(Load Eye - Vcent_DQ) = %s" % Uenv[key][0])

						# Old Eye
						else:
							# AC_DQ
							if "(AC_DQ)" in key:
								if self._ComboBox_AC_DQ.Visible:									
									self._ComboBox_AC_DQ.SelectedIndex = int(Uenv[key][0])
									Log("		(Load Eye - AC_DQ) = %s" % Uenv[key][1])										
								else:
									self._TextBox_AC_DQ.Text == Uenv[key][0]
									Log("		(Load Eye - AC_DQ) = %s" % Uenv[key][0])

							# AC_ADDR
							elif "(AC_ADDR)" in key:
								if self._ComboBox_AC_ADDR.Visible:									
									self._ComboBox_AC_ADDR.SelectedIndex = int(Uenv[key][0])									
									Log("		(Load Eye - AC_ADDR) = %s" % Uenv[key][1])										
								else:
									self._TextBox_AC_ADDR.Text == Uenv[key][0]
									Log("		(Load Eye - AC_ADDR) = %s" % Uenv[key][0])

							# DC_DQ
							elif "(DC_DQ)" in key:				
								self._TextBox_DC_DQ.Text = Uenv[key][0]
								Log("		(Load Eye - DC_DQ) = %s" % Uenv[key][0])

							# DC_ADDR
							elif "(DC_ADDR)" in key:				
								self._TextBox_DC_ADDR.Text = Uenv[key][0]
								Log("		(Load Eye - DC_ADDR) = %s" % Uenv[key][0])

							# Vref
							elif "(Vref)" in key:				
								self._TextBox_Vref.Text = Uenv[key][0]
								Log("		(Load Eye - Vref) = %s" % Uenv[key][0])

							# DQ_Setup
							elif "(DQ_Setup)" in key:				
								self._TextBox_DQSetup.Text = Uenv[key][0]
								Log("		(Load Eye - DQ_Setup) = %s" % Uenv[key][0])

							# DQ_Hold
							elif "(DQ_Hold)" in key:				
								self._TextBox_DQHold.Text = Uenv[key][0]
								Log("		(Load Eye - DQ_Hold) = %s" % Uenv[key][0])

							# ADDR_Setup
							elif "(ADDR_Setup)" in key:				
								self._TextBox_ADDRSetup.Text = Uenv[key][0]
								Log("		(Load Eye - ADDR_Setup) = %s" % Uenv[key][0])

							# ADDR_Hold
							elif "(ADDR_Hold)" in key:				
								self._TextBox_ADDRHold.Text = Uenv[key][0]
								Log("		(Load Eye - ADDR_Hold) = %s" % Uenv[key][0])

					# --------- Net Classification ----------------
					elif "<Net Classification>" in key:						
						sub_DB.Net_Form._DataGridView.Rows.Add(Uenv[key][0], Uenv[key][1], Uenv[key][2], Uenv[key][3], Uenv[key][4])
						pass

					# --------- Analyze Option ----------------
					elif "<Analyze Option>" in key:
						# Resources Folder
						if "(Resources Folder)" in key:
							sub_DB.Option_Form._TextBox_Resource.Text = Uenv[key][0]
							Log("		(Load Eye - Resources Folder) = %s" % Uenv[key][0])

						# Definition File
						elif "(Definition File)" in key:
							sub_DB.Option_Form._TextBox_Def.Text = Uenv[key][0]
							Log("		(Load Eye - Definition File) = %s" % Uenv[key][0])

						# Configuration File
						elif "(Configuration File)" in key:
							sub_DB.Option_Form._TextBox_Conf.Text = Uenv[key][0]
							Log("		(Load Eye - Configuration File) = %s" % Uenv[key][0])

						# Eye Offset
						elif "(Eye Offset)" in key:
							sub_DB.Option_Form._TextBox_EyeOffset.Text = Uenv[key][0].replace("ns","").strip()
							Log("		(Load Eye - Eye Offset) = %s" % Uenv[key][0])

						# Vref Method
						elif "(Vref Method)" in key:							
							sub_DB.Option_Form._ComboBox_Vref.SelectedIndex = int(Uenv[key][0])							
							Log("		(Load Eye - Vref Method) = %s" % Uenv[key][1])

						# Analyze Method
						elif "(Analyze Method)" in key:
							sub_DB.Option_Form._ComboBox_Analyze.SelectedIndex = int(Uenv[key][0])
							Log("		(Load Eye - Analyze Method) = %s" % Uenv[key][1])

						# Export Excel Report
						elif "(Export Excel Report)" in key:							
							if Uenv[key][0] == "True":
								sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked = True
							else:
								sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked = False
							Log("		(Load Eye - Export Excel Report) = %s" % Uenv[key][0])

						# Image Width
						elif "(Image Width)" in key:
							sub_DB.Option_Form._TextBox_ImageWidth.Text = Uenv[key][0].replace("pixel","").strip()
							Log("		(Load Eye - Image Width) = %s" % Uenv[key][0])

						# Report Format
						elif "(Report Format)" in key:
							sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex = int(Uenv[key][0])
							Log("		(Load Eye - Report Format) = %s" % Uenv[key][1])

						# Plot Eye with Mask
						elif "(Plot Eye with Mask)" in key:							
							if Uenv[key][0] == "True":
								sub_DB.Option_Form._CheckBox_PlotEye.Checked = True
							else:
								sub_DB.Option_Form._CheckBox_PlotEye.Checked = False
							Log("		(Load Eye - Plot Eye with Mask) = %s" % Uenv[key][0])

						# Check DDR Compliance
						elif "(Check DDR Compliance)" in key:
							if Uenv[key][0] == "True":
								sub_DB.Option_Form._CheckBox_Compiance.Checked = True
							else:
								sub_DB.Option_Form._CheckBox_Compiance.Checked = False
							Log("		(Load Eye - Check DDR Compliance) = %s" % Uenv[key][0])

					# --------- DDR Compliance ----------------
					elif "<DDR Compliance>" in key:
						pass

				except Exception as e:		
					Log("		(Load Eye) : Failed")
					Log(traceback.format_exc())
					print traceback.format_exc() 
					MessageBox.Show("Fail to Load Cnf for Eye Analyzer","Warning")						
					EXIT()

		sub_DB.Option_Form._ComboBox_Vref.SelectedIndex = int(Uenv["(Vref Method)<Analyze Option>[Eye]"][0])
		if flag:
			if sub_DB.Option_Form._ComboBox_Vref.SelectedIndex==0:
				self._CheckBox_VcentDQ.Checked = True
			else:
				self._CheckBox_VcentDQ.Checked = False
				self._TextBox_VcentDQ.Text = Uenv["(Manual Vref)<Analyze Option>[Eye]"][0]
		else:
			if sub_DB.Option_Form._ComboBox_Vref.SelectedIndex==0:			
				self._CheckBox_Vref.Checked = True
			else:
				self._CheckBox_Vref.Checked = False
				self._TextBox_Vref.Text = Uenv["(Manual Vref)<Analyze Option>[Eye]"][0]

	# Fail Version Check
	else:

		MessageBox.Show("Version of Eye Analyzer(%s) and Cnf(%s) File do not match.\nFail to load auto saved cnf file." % (sub_DB.Version, cnf_version), "Warning")

def Check_Setup(self):
	flag = True
	if self._TextBox_InputFile.Text == "":
		flag = False

	if self._ComboBox_Design.Text == "":
		flag = False
		
	if len(self._CheckedListBox_ReportName.CheckedItems) == 0:
		flag = False

	if self._ComboBox_SolutionName.Text == "":
		flag = False

	if self._ComboBox_DDRGen.Text == "":
		flag = False

	if self._ComboBox_DataRate.Text == "":
		flag = False

	return flag

def CnfAutoSave():
	#################
	# Create Header #
	#################
	try:
		Log("	<Auto Saved Cnf - Header>")
		cnf_log = ""
		cnf_log += "############################################################"
		cnf_log += "\n" + "#	Ansys DDR Wizard %s Auto Saved Configuration File" % sub_DB.Version
		cnf_log += "\n" + "#		Input File : " +  sub_DB.Input_File
		cnf_log += "\n" + "#		Start : " +  sub_DB.start_time
		cnf_log += "\n" + "#		End   : " +  time.strftime('%Y.%m.%d, %H:%M:%S')
		cnf_log += "\n" + "############################################################"

	except Exception as e:		
		Log("	<Auto Saved Cnf - Header> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to create auto saved Cnf header","Warning")						
		EXIT()

	###########
	# Version #
	###########	
	cnf_log += "\n\n" + "[Version] = %s" % sub_DB.Version

	####################
	# For EM Extractor #
	####################
	try:
		Log("	<Auto Saved Cnf - EM Extractor>")
		cnf_log += "\n\n" + "[EM]"

	except Exception as e:		
		Log("	<Auto Saved Cnf - EM Extractor> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to create auto saved Cnf - EM Extractor","Warning")						
		EXIT()

	#########################
	# For Circuit Simulator #
	#########################
	try:
		Log("	<Auto Saved Cnf - Circuit Simulator>")
		cnf_log += "\n\n" + "[Tran]"

	except Exception as e:		
		Log("	<Auto Saved Cnf - Circuit Simulator> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to create auto saved Cnf - Circuit Simulator","Warning")						
		EXIT()

	####################
	# For Eye Analyzer #
	####################
	try:
		Log("	<Auto Saved Cnf - Eye Analyzer>")
		cnf_log += "\n\n" + "[Eye]"
		# --------- Setup----------------
		cnf_log += "\n\t" + "<Setup>"
		##	 Input File
		#cnf_log += "\n\t\t" + "(Input File)"
		#if not sub_DB.Eye_Form._TextBox_InputFile.Text == "":
		#	cnf_log += " = %s, %d" % (sub_DB.Eye_Form._TextBox_InputFile.Text, sub_DB.InputFile_Flag)

		##	 Design
		#cnf_log += "\n\t\t" + "(Design)"
		#if not sub_DB.Eye_Form._ComboBox_Design.Text == "":
		#	cnf_log += " = %s" % sub_DB.Eye_Form._ComboBox_Design.Text

		##	 Report Name
		#cnf_log += "\n\t\t" + "(Report Name)"		
		#for item in sub_DB.Eye_Form._CheckedListBox_ReportName.Items:
		#	if item in sub_DB.Eye_Form._CheckedListBox_ReportName.CheckedItems:
		#		cnf_log += "\n\t\t\t" + "= %s!" % item
		#	else:
		#		cnf_log += "\n\t\t\t" + "= %s" % item

		##	 Setup Name	
		#cnf_log += "\n\t\t" + "(Setup Name)"
		#if not sub_DB.Eye_Form._ComboBox_SolutionName.Text == "":
		#	cnf_log += " = %s" % sub_DB.Eye_Form._ComboBox_SolutionName.Text

		#	 DDR Gen
		cnf_log += "\n\t\t" + "(DDR Gen)"
		if not sub_DB.Eye_Form._ComboBox_DDRGen.Text == "":
			cnf_log += " = %s" % sub_DB.Eye_Form._ComboBox_DDRGen.Text

		#	 Data-rate
		cnf_log += "\n\t\t" + "(Data-rate)"
		if not sub_DB.Eye_Form._ComboBox_DataRate.Text == "":
			cnf_log += " = %s" % sub_DB.Eye_Form._ComboBox_DataRate.Text

		## --------- Eye Specifications ----------------
		#cnf_log += "\n\n\t" + "<Eye Specifications>"
		##	 New Eye
		#if sub_DB.Eyeflag:
		#	#	 Eyeflag for New Eye
		#	cnf_log += "\n\t\t" + "(Eye_Type) = Ture"

		#	#	 VdIVW
		#	cnf_log += "\n\t\t" + "(VdIVW)"
		#	if not sub_DB.Eye_Form._TextBox_VdIVW.Text == "":
		#		cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_VdIVW.Text

		#	#	 TdIVW
		#	cnf_log += "\n\t\t" + "(TdIVW)"
		#	if not sub_DB.Eye_Form._TextBox_TdIVW.Text == "":
		#		cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_TdIVW.Text

		#	#	 Vcent_DQ
		#	if sub_DB.Eye_Form._CheckBox_EditEnable_NewEye.Checked:
		#		cnf_log += "\n\t\t" + "(Vcent_DQ)"
		#		if not sub_DB.Eye_Form._TextBox_VcentDQ.Text == "":
		#			cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_VcentDQ.Text

		##	 Old Eye
		#else:
		#	#	 Eyeflag for Old Eye
		#	cnf_log += "\n\t\t" + "(Eye_Type) = False"
			
		#	#	 AC_DQ
		#	cnf_log += "\n\t\t" + "(AC_DQ)"
		#	if sub_DB.Eye_Form._ComboBox_AC_DQ.Visible:				
		#		if not sub_DB.Eye_Form._ComboBox_AC_DQ.Text == "":
		#			cnf_log += " = %d, %s" % (sub_DB.Eye_Form._ComboBox_AC_DQ.SelectedIndex, sub_DB.Eye_Form._ComboBox_AC_DQ.Text)
		#	else:
		#		if not sub_DB.Eye_Form._TextBox_AC_DQ.Text == "":
		#			cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_AC_DQ.Text

		#	#	 AC_ADDR
		#	cnf_log += "\n\t\t" + "(AC_ADDR)"
		#	if sub_DB.Eye_Form._ComboBox_AC_ADDR.Visible:				
		#		if not sub_DB.Eye_Form._ComboBox_AC_ADDR.Text == "":
		#			cnf_log += " = %d, %s" % (sub_DB.Eye_Form._ComboBox_AC_ADDR.SelectedIndex, sub_DB.Eye_Form._ComboBox_AC_ADDR.Text)
		#	else:
		#		if not sub_DB.Eye_Form._TextBox_AC_ADDR.Text == "":
		#			cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_AC_ADDR.Text

		#	#	 DC_DQ
		#	cnf_log += "\n\t\t" + "(DQ_DC)"
		#	if not sub_DB.Eye_Form._TextBox_DC_DQ.Text == "":
		#		cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_DC_DQ.Text

		#	#	 DC_ADDR
		#	cnf_log += "\n\t\t" + "(DQ_ADDR)"
		#	if not sub_DB.Eye_Form._TextBox_DC_ADDR.Text == "":
		#		cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_DC_ADDR.Text

		#	#	 Vref
		#	cnf_log += "\n\t\t" + "(Vref)"
		#	if not sub_DB.Eye_Form._TextBox_Vref.Text == "":
		#		cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_Vref.Text

		#	#	 DQ_Setup
		#	cnf_log += "\n\t\t" + "(DQ_Setup)"
		#	if not sub_DB.Eye_Form._TextBox_DQSetup.Text == "":
		#		cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_DQSetup.Text

		#	#	 DQ_Hold
		#	cnf_log += "\n\t\t" + "(DQ_Hold)"
		#	if not sub_DB.Eye_Form._TextBox_DQHold.Text == "":
		#		cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_DQHold.Text

		#	#	 ADDR_Setup
		#	cnf_log += "\n\t\t" + "(ADDR_Setup)"
		#	if not sub_DB.Eye_Form._TextBox_ADDRSetup.Text == "":
		#		cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_ADDRSetup.Text

		#	#	 ADDR_Hold
		#	cnf_log += "\n\t\t" + "(ADDR_Hold)"
		#	if not sub_DB.Eye_Form._TextBox_ADDRHold.Text == "":
		#		cnf_log += " = %s" % sub_DB.Eye_Form._TextBox_ADDRHold.Text
		
		## --------- Net Classification ----------------
		#cnf_log += "\n\n\t" + "<Net Classification>"
		#iter = 0
		#for row in sub_DB.Net_Form._DataGridView.Rows:
		#	cnf_log += "\n\t\t" + " (%d) = %s, %s, %s, %s, %s" % (iter, str(row.Cells[0].Value), row.Cells[1].Value, row.Cells[2].Value, row.Cells[3].Value, row.Cells[4].Value)
		#	iter += 1

		## --------- Analyze Option ----------------
		#cnf_log += "\n\n\t" + "<Analyze Option>"
		##	 Resources Folder
		#cnf_log += "\n\t\t" + "(Resources Folder) = %s" % sub_DB.resource_dir

		##	 Definition File
		#cnf_log += "\n\t\t" + "(Definition File) = %s" % sub_DB.Cenv["File"]

		##	 Configuration File
		#cnf_log += "\n\t\t" + "(Configuration File) = %s" % sub_DB.Uenv["File"]

		##	 Eye Offset
		#cnf_log += "\n\t\t" + "(Eye Offset)"
		#if not sub_DB.Option_Form._TextBox_EyeOffset.Text == "":
		#	cnf_log += " = %s ns" % sub_DB.Option_Form._TextBox_EyeOffset.Text

		##	 Vref Method
		#cnf_log += "\n\t\t" + "(Vref Method) = %d, %s" % (sub_DB.Option_Form._ComboBox_Vref.SelectedIndex, sub_DB.Option_Form._ComboBox_Vref.Text)

		##	 Analyze Method
		#cnf_log += "\n\t\t" + "(Analyze Method) = %d, %s" % (sub_DB.Option_Form._ComboBox_Analyze.SelectedIndex, sub_DB.Option_Form._ComboBox_Analyze.Text)
	
		##	 Export Excel Report
		#cnf_log += "\n\t\t" + "(Export Excel Report) = %s" % sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked
	
		##	 Image Width
		#if sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked:
		#	if sub_DB.Option_Form._CheckBox_PlotEye.Checked:
		#		cnf_log += "\n\t\t" + "(Image Width)"
		#		cnf_log += " = %s pixel" % sub_DB.Option_Form._TextBox_ImageWidth.Text

		##	 Report Format
		#if sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked:
		#	cnf_log += "\n\t\t" + "(Report Format) = %d, %s" % (sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex, sub_DB.Option_Form._ComboBox_ReportFormat.Text)

		##	 Plot Eye with Mask
		#cnf_log += "\n\t\t" + "(Plot Eye with Mask) = %s" % sub_DB.Option_Form._CheckBox_PlotEye.Checked

		##	 Check DDR Compliance
		#cnf_log += "\n\t\t" + "(Check DDR Compliance) = %s" % sub_DB.Option_Form._CheckBox_Compiance.Checked

		## --------- DDR Compliance ----------------
		#if sub_DB.Option_Form._CheckBox_Compiance.Visible:
		#	#TODO : Save Cnf for DDR Compliance
		#	cnf_log += "\n\n\t" + "<DDR Compliance>"
		pass

	except Exception as e:
		Log("	<Auto Saved Cnf - Eye Analyzer> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to create auto saved Cnf - Eye Analyzer","Warning")						
		EXIT()

	#################
	# Save Cnf File #
	#################
	try:
		Log("	<Auto Save Cnf File>")
		f = open(sub_DB.user_dir + r'\latest.cnf', 'w')
		f.write(cnf_log)
		f.close()		

	except Exception as e:		
		Log("	<Auto Save Cnf File> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to auto save Cnf file","Warning")						
		EXIT()

def CnfAutoLoad(self):
	sub_DB.TBD_flag = False	
	File = sub_DB.user_dir + r'\latest.cnf'		
	Uenv = Load_env(File)
	#Uenv["File"] = File		
	#sub_DB.Uenv = Uenv
	Log("	<Load the Auto Saved Cnf - %s>" % File)

	version_check_flag = False	
	for key in Uenv:
		#################
		# Check Version #
		#################
		if "[Version]" in key:			
			cnf_version = Uenv[key][0]
			if Uenv[key][0] == sub_DB.Version:
				version_check_flag = True				
				break

	if version_check_flag:
		for key in Uenv:
			##################################
			# Load Auto Cnf for EM Extractor #
			##################################
			if "[EM]" in key:
				try:
					Log("		(Auto Load EM)")
					pass

				except Exception as e:		
					Log("		(Auto Load EM) : Failed")
					Log(traceback.format_exc())
					MessageBox.Show("Fail to Load Auto Saved Cnf for EM Extractor","Warning")
					EXIT()
				
			#######################################
			# Load Auto Cnf for Circuit Simulator #
			#######################################
			elif "[Tran]" in key:
				try:
					Log("		(Auto Load Tran)")
					pass

				except Exception as e:		
					Log("		(Auto Load Tran) : Failed")
					Log(traceback.format_exc())
					MessageBox.Show("Fail to Load Auto Saved Cnf for Circuit Simulator","Warning")						
					EXIT()
			
			##################################################################
			# Load Auto Cnf for Eye Analyzer                                 #
			#    - Read only settings that are independent of the input file #
			#		`DDR type & data-rate                                    #			
			##################################################################
			elif "[Eye]" in key:
				try:
					if "<Setup>" in key:
						# DDR Gen
						if "(DDR Gen)" in key:
							self._ComboBox_DDRGen.Enabled = True
							self._ComboBox_DDRGen.Text = Uenv[key][0]
							Log("		(Auto Load Eye - DDR Gen) = %s" % Uenv[key][0])

						# Data-rate
						elif "(Data-rate)" in key:
							self._ComboBox_DataRate.Enabled = True
							self._ComboBox_DataRate.BackColor = System.Drawing.Color.White
							self._ComboBox_DataRate.Text = Uenv[key][0]
							Log("		(Auto Load Eye - Data-rate) = %s" % Uenv[key][0])

				except Exception as e:		
					Log("		(Auto Load Eye) : Failed")
					Log(traceback.format_exc())
					MessageBox.Show("Fail to Load Auto Saved Cnf for Eye Analyzer","Warning")						
					EXIT()

	else:
		MessageBox.Show("Version of Eye Analyzer(%s) and Cnf(%s) File do not match.\nFail to load auto saved cnf file." % (sub_DB.Version, cnf_version), "Warning")

def EXIT():	
	sub_DB.exit_iter += 1	
	LogSave(sub_DB.exit_iter)	
	sub_ScriptEnv.Release()	

def ReleaseObject(obj):	
	System.Runtime.InteropServices.Marshal.ReleaseComObject(obj)
	System.GC.Collect()

def Initial():
	Log("\n\n")
	sub_DB.TBD_flag = True
	sub_DB.CSV_flag = True
	sub_ScriptEnv.Release()
	sub_DB.AEDT = {}
	sub_DB.Eye_Form._TextBox_VcentDQ.Text = "Auto"	
	sub_DB.Eye_Form._ComboBox_Design.Items.Clear()
	
	sub_DB.Eye_Form._ComboBox_Design.BackColor = System.Drawing.SystemColors.Window
	sub_DB.Eye_Form._ComboBox_DataRate.BackColor = System.Drawing.SystemColors.Info
	sub_DB.Eye_Form._Button_ViewNet.BackColor = System.Drawing.SystemColors.Control

	sub_DB.Net_Form = ""	
	sub_DB.Net_Form = GUI_subforms.NetForm()

	sub_DB.Option_Form = ""
	sub_DB.Option_Form = GUI_subforms.OptionForm(2)

	sub_DB.Result_Flag = False
	sub_DB.Eye_Analyze_Flag = True
	
	sub_DB.Eye_Form._Button_Analyze.Enabled = False
	sub_DB.Eye_Form._Button_Analyze.BackColor = System.Drawing.SystemColors.Control

	sub_DB.Eye_Form._Button_ViewResult.Enabled = False
	sub_DB.Eye_Form._Button_ViewResult.BackColor = System.Drawing.SystemColors.Control\

	sub_DB.Eye_Form._CheckBox_VcentDQ.Checked = True
	sub_DB.Eye_Form._CheckBox_Vref.Checked = True

def temp_get_waveform(self):
	Waveform = {}
	with open(sub_DB.Waveform_File) as fp:
		# Get Netlist and Create Waveform Dictionary keys
		temp_data = fp.readline().replace("\"","").replace(" ","").strip().split(",")

		# Delete global & local variable data
		iter = 0
		while(1):
			if not "Time" in temp_data[0]:
				del temp_data[0]
				iter += 1
			else:
				break
			
		# Get time and voltage unit
		sub_DB.Unit["Time"] = temp_data[0].split("[")[-1].split("]")[0]
		sub_DB.Unit["Voltage"] = temp_data[1].split("[")[-1].split("]")[0]
			
		# Delete Time Column
		del temp_data[0]

		data = [[0 for col in range(0)] for row in range(len(temp_data))]
		for i in range(0, len(temp_data)):
			data[i].append(temp_data[i])

		# Get Waveform Data				
		for line in fp:
			for i in range(0, len(temp_data)):
				data[i].append(float(line.split(",")[i+1+iter]))
	fp.close()

	for cell in data:
		key = cell[0].split("[")[0]
		del cell[0]
		Waveform[key] = cell
		Log("			= %s" % key)

	# Check time unit - Does not check time unit in AEDT input file process (1ps uniform exported)
	#if sub_DB.Unit["Time"].lower() == "ps":
	#	pass
	#elif sub_DB.Unit["Time"].lower() == "ns":
	#	for i in range(0, len(Time)):
	#		Time[i] = Time[i]*1000
	#else:
	#	MessageBox.Show("The time unit in the input csv file is not supported.","Warning",MessageBoxButtons.OK, MessageBoxIcon.Warning)
	#sub_DB.Time = Time

	# Check voltage unit
	if sub_DB.Unit["Voltage"].lower() == "mv":
		pass
	elif sub_DB.Unit["Voltage"].lower() == "v":
		for key in Waveform:
			for i in range(0, len(Waveform[key])):
				Waveform[key][i] = Waveform[key][i]*1000
	else:
		MessageBox.Show("The voltage unit in the input csv file is not supported.","Warning",MessageBoxButtons.OK, MessageBoxIcon.Warning)
		
	return Waveform
























