import os
import clr
import re
import time
import shutil
import traceback
import sub_ScriptEnv
import sub_AEDT
import sub_DB

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
					line = line.strip().replace(" ","")
					key = str_grandchild + str_child + str_parent
					for cell in list(filter(None, line.strip().split("=")[-1].split(","))):
							temp_list.append(cell)

				if key:
					temp_DB[key] = temp_list

	fp.close()

	return temp_DB

def Net_Identify(name, Uenv):
	Group = 7 # OTHER
	Match = ""

	for key in Uenv:
		if "<Ignore>" in key:
			name = name.replace(Uenv[key][0], "")

	for keyword in Uenv["<DM>[Net Identification]"]:
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I) # re.I (or re.IGNORECASE) = No distinction between upper and lower case letters.
		if m:
			Match = m.group()
			Group = 0 # "DM"
			break

	for keyword in Uenv["<CLK_P>[Net Identification]"]:
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I)
		if m:
			Match = m.group()
			Group = 4 # CLK
			break

	for keyword in Uenv["<CLK_N>[Net Identification]"]:
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I)
		if m:
			Match = m.group()
			Group = 5 # CLK#
			break

	for keyword in Uenv["<ADDR>[Net Identification]"]:		
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I)
		if m:
			Match = m.group()
			Group = 6 # ADDR
			break

	for keyword in Uenv["<DQS_P>[Net Identification]"]:
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I)
		if m:
			Match = m.group()
			Group = 2 # DQS
			break

	for keyword in Uenv["<DQS_N>[Net Identification]"]:
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I)
		if m:
			Match = m.group()
			Group = 3 # DQS#
			break

	for keyword in Uenv["<DQ>[Net Identification]"]:
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

		noteh = (vmax - Vref) / (vmax - vmin) * 9500
		oModule.AddNote(Report_Name, ["NAME:NoteDataSource", ["NAME:NoteDataSource", "SourceName:=",
						"Note1", "HaveDefaultPos:=", True, "DefaultXPos:=", 5500, "DefaultYPos:=",
						noteh, "String:=", str(Eye_Measure_Results[PlotList[0]][0]) + " / " + str(round(sub_DB.Jitter_RMS[PlotList[0]],1))]])
		Log("			= Add Note, Width:%s[ps] Jitter(RMS):%s[ps]" % (str(Eye_Measure_Results[PlotList[0]][0]), str(round(sub_DB.Jitter_RMS[PlotList[0]],1))))

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
			img_path = img_path.replace("\\"+img_path.split("\\")[-1],"")
			oModule.ExportImageToFile(Report_Name, img_path + "\\" + Report_Name + ".gif", imgw * 2, imgh * 2)
			sub_DB.Excel_Img_File.append(img_path + "\\" + Report_Name + ".gif")
			Log("			= Save Image File, %s" % img_path + "\\" + Report_Name + ".gif")

	except Exception as e:		
		Log("	<Eye Plot> = Failed")
		Log(traceback.format_exc())
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

		noteh = (vmax - Vref) / (vmax - vmin) * 9500
		oModule.AddNote(Report_Name, ["NAME:NoteDataSource", ["NAME:NoteDataSource", "SourceName:=",
						"Note1", "HaveDefaultPos:=", True, "DefaultXPos:=", 5500, "DefaultYPos:=",
						noteh, "String:=", str(Eye_Measure_Results[PlotList[0]][0]) + " / " + str(Eye_Measure_Results[PlotList[0]][1])]])
		Log("			= Add Note, Width:%s[ps] Jitter(RMS):%s[ps]" % (str(Eye_Measure_Results[PlotList[0]][0]), str(Eye_Measure_Results[PlotList[0]][1])))

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
			img_path = img_path.replace("\\"+img_path.split("\\")[-1],"")
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

def Check_spec():	
	try:
		Log("	<Check DDR Specification>")
		# for New Eye
		if sub_DB.Eyeflag:
			pass
		else:
			pass
	except Exception as e:		
		Log("	<Check DDR Specification> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to plot eye","Warning")						
		EXIT()

def Log(msg):

	sub_DB.Log += "\n" + time.strftime('%H:%M:%S') + "\t" + msg

def LogSave():		
	f = open(sub_DB.result_dir + '\\ddr_' + time.strftime('%Y%m%d_%H%M%S') + '.log', 'w')
	f.write(sub_DB.Log)	
	f.close()
	

def EXIT():
	sub_DB.exit_iter += 1	
	if sub_DB.exit_iter == 1:		
		LogSave()		
	#if "App" in sub_DB.AEDT.keys():
	#	sub_ScriptEnv.Release()
	sub_ScriptEnv.Release()
	os._exit(0)

def ReleaseObject(obj):	
	System.Runtime.InteropServices.Marshal.ReleaseComObject(obj)
	System.GC.Collect()

def Initial():
	sub_ScriptEnv.Release()
	sub_DB.Eye_Form._ComboBox_Design.Items.Clear()	
	sub_DB.Net_Form.Init_Flag = True

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